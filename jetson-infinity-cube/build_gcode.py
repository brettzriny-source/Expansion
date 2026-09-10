"""
Engrave the Jetson wordmark into a Cura-sliced infinity-cube G-code (Ender-3 V2, 0.2 mm layers).

 * Outer cubes (columns 0 and 3): wordmark cut 0.4 mm into the outward-facing long side
   (the hinge-free vertical face) by removing the outer-wall bead where the letters fall.
   The inner wall becomes the recess floor.
 * Middle cubes (columns 1 and 2): their long sides carry hinge clearance slots, so the
   wordmark is cut 0.4 mm into the top face instead by regenerating the top two skin
   layers with the letters as holes (perimeter bead around each letter + hatch fill).

All E values downstream are renumbered so absolute extrusion stays consistent.
"""
import re, sys, math
from shapely.geometry import box, LineString, MultiLineString
from shapely import affinity
from shapely.ops import unary_union
from logo_geom import wordmark_mm, slab_intervals

SRC = "/root/.claude/uploads/3302de19-8fcd-57a8-a3ab-24f1533cfab6/28c316b1-CE3E3V2_infinity_cube.gcode"
E_PER_MM = 0.4 * 0.2 / (math.pi * 0.875 ** 2)   # 0.4 mm line, 0.2 mm layer, 1.75 mm filament
RETRACT = 5.0
F_RETRACT = 2700
F_TRAVEL = 9000
F_PERIM = 600
F_HATCH = 1030
LAYER_H = 0.2
BOLD = 0.08          # widen strokes slightly so every cavity is >= one nozzle width
MIN_CAV = 0.5
MIN_GAP = 0.35

# --- geometry of the print (measured from the G-code) --------------------------------
CUBE_CX = [86.9, 107.3, 127.7, 148.1]
SIDE_FACES = {  # outer cubes: (face y, row, cube x-center, mirrored?)
    (0, 0): dict(y=97.5, cx=86.9, mirror=False),
    (3, 0): dict(y=97.5, cx=148.1, mirror=False),
    (0, 1): dict(y=137.5, cx=86.9, mirror=True),
    (3, 1): dict(y=137.5, cx=148.1, mirror=True),
}
SIDE_RUN_W = 13.8          # flat width of the side face
SIDE_Z_LO, SIDE_Z_HI = 3.4, 17.0
TOP_FACES = {               # middle cubes: skin square (x0,y0,x1,y1) on layers 98/99
    (1, 0): (101.2, 101.2, 113.4, 113.4),
    (1, 1): (101.2, 121.6, 113.4, 133.8),
    (2, 0): (121.6, 101.2, 133.8, 113.4),
    (2, 1): (121.6, 121.6, 133.8, 133.8),
}
TOP_LAYERS = (98, 99)


def fmt(v):
    s = f"{v:.5f}".rstrip('0').rstrip('.')
    return s if s not in ('', '-0') else '0'


def build(orientation, out_path):
    # ---- wordmark geometry -----------------------------------------------------------
    side_w = SIDE_RUN_W - 0.4
    g = wordmark_mm(side_w, bold=BOLD)
    if orientation == 'vertical':
        g = affinity.rotate(g, 90, origin=(0, 0))
    b = g.bounds
    g_side = affinity.translate(g, -(b[0] + b[2]) / 2, -(b[1] + b[3]) / 2)   # centred at (0,0): u across face, v = z
    side_h = g_side.bounds[3] - g_side.bounds[1]
    zc = (SIDE_Z_LO + SIDE_Z_HI) / 2
    # per layer, per side face: list of bed-X intervals to cut out of the outer wall
    side_cuts = {}
    for L in range(0, 100):
        zmid = LAYER_H * L + LAYER_H / 2       # layer L spans (0.2L, 0.2L+0.2]
        v = zmid - zc
        iv = slab_intervals(g_side, v - 0.005, v + 0.005, MIN_CAV, MIN_GAP)
        if not iv:
            continue
        for key, f in SIDE_FACES.items():
            xs = []
            for a, bb in iv:
                if f['mirror']:
                    xs.append((f['cx'] - bb, f['cx'] - a))
                else:
                    xs.append((f['cx'] + a, f['cx'] + bb))
            side_cuts.setdefault(L, {})[key] = sorted(xs)

    top_w = 11.8
    gt = wordmark_mm(top_w, bold=BOLD)
    bt = gt.bounds
    gt = affinity.translate(gt, -(bt[0] + bt[2]) / 2, -(bt[1] + bt[3]) / 2)
    top_letters = {k: affinity.translate(gt, (x0 + x1) / 2, (y0 + y1) / 2) for k, (x0, y0, x1, y1) in TOP_FACES.items()}

    # ---- pass 1: read file, learn skin hatch angle per top layer --------------------
    lines = open(SRC).read().split('\n')
    hatch_angle = {}
    layer = None; typ = None; x = y = None
    for ln in lines:
        if ln.startswith(';LAYER:'): layer = int(ln[7:]); continue
        if ln.startswith(';TYPE:'): typ = ln[6:]; continue
        if ln[:2] in ('G0', 'G1'):
            m = dict(re.findall(r'([XYE])(-?[\d.]+)', ln))
            nx = float(m['X']) if 'X' in m else x; ny = float(m['Y']) if 'Y' in m else y
            if layer in TOP_LAYERS and typ == 'SKIN' and 'E' in m and x is not None and 'X' in m and 'Y' in m:
                dx, dy = nx - x, ny - y
                if math.hypot(dx, dy) > 1.0:
                    ang = math.degrees(math.atan2(dy, dx)) % 180
                    hatch_angle.setdefault(layer, []).append(round(ang))
            x, y = nx, ny
    for L in TOP_LAYERS:
        angs = hatch_angle[L]
        hatch_angle[L] = max(set(angs), key=angs.count)

    # ---- skin generator for a top face -----------------------------------------------
    def gen_top_skin(key, L, start_xy):
        x0, y0, x1, y1 = TOP_FACES[key]
        face = box(x0, y0, x1, y1)
        letters = top_letters[key]
        out = []
        cx, cy = start_xy
        e_total = 0.0

        def travel(px, py):
            nonlocal cx, cy, e_total
            d = math.hypot(px - cx, py - cy)
            if d < 0.01:
                return
            if d > 3.0:
                out.append(('E', -RETRACT, F_RETRACT))
                out.append(('G0', px, py))
                out.append(('E', RETRACT, F_RETRACT))
            else:
                out.append(('G0', px, py))
            cx, cy = px, py

        def extrude(px, py, F):
            nonlocal cx, cy, e_total
            d = math.hypot(px - cx, py - cy)
            if d < 0.02:
                return
            out.append(('G1', px, py, d * E_PER_MM, F))
            e_total += d * E_PER_MM
            cx, cy = px, py

        # 1) perimeter beads hugging each letter cavity (bead centre 0.2 mm outside the letter edge)
        ring_geom = letters.buffer(0.2, join_style=1).simplify(0.02)
        rings = []
        for p in (ring_geom.geoms if hasattr(ring_geom, 'geoms') else [ring_geom]):
            rings.append(list(p.exterior.coords))
            for r in p.interiors:
                rings.append(list(r.coords))
        # order rings greedily by distance
        rem = rings[:]
        while rem:
            rem.sort(key=lambda r: min(math.hypot(px - cx, py - cy) for px, py in r[::max(1, len(r)//12)]))
            r = rem.pop(0)
            # rotate ring to start at the closest vertex
            i0 = min(range(len(r)), key=lambda i: math.hypot(r[i][0] - cx, r[i][1] - cy))
            r = r[i0:] + r[1:i0 + 1]
            travel(*r[0])
            for px, py in r[1:]:
                extrude(px, py, F_PERIM)

        # 2) hatch the rest of the face at Cura's angle for this layer, 0.4 mm pitch
        region = face.difference(letters.buffer(0.4, join_style=1))
        ang = math.radians(hatch_angle[L])
        ux, uy = math.cos(ang), math.sin(ang)          # along-line direction
        nx_, ny_ = -uy, ux                             # normal
        fcx, fcy = (x0 + x1) / 2, (y0 + y1) / 2
        half = math.hypot(x1 - x0, y1 - y0)
        pieces_by_line = []
        k = -half
        while k <= half:
            px, py = fcx + nx_ * k, fcy + ny_ * k
            ls = LineString([(px - ux * half, py - uy * half), (px + ux * half, py + uy * half)])
            inter = ls.intersection(region)
            segs = []
            if not inter.is_empty:
                geoms = inter.geoms if hasattr(inter, 'geoms') else [inter]
                for s in geoms:
                    if s.geom_type == 'LineString' and s.length >= 0.25:
                        c = list(s.coords)
                        segs.append((c[0], c[-1]))
            if segs:
                segs.sort(key=lambda s: (s[0][0] * ux + s[0][1] * uy))
                pieces_by_line.append(segs)
            k += 0.4
        flip = False
        for segs in pieces_by_line:
            if flip:
                segs = [(b_, a_) for a_, b_ in reversed(segs)]
            for a_, b_ in segs:
                travel(*a_)
                extrude(*b_, F_HATCH)
            flip = not flip
        return out, e_total, (cx, cy)

    # ---- pass 2: rewrite -------------------------------------------------------------
    out_lines = []
    layer = None; typ = None; x = y = None
    last_e_orig = 0.0; e_out = 0.0
    cur_f = None
    in_body = False
    removed_e = 0.0
    skin_buf = None      # buffered lines of a skin block being replaced
    skin_key = None
    stats = dict(side_gaps=0, side_layers=set(), top_faces=0)

    def flush_e():
        return fmt(e_out)

    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        i += 1
        if ln.startswith(';LAYER:0'):
            in_body = True
        if ln.startswith('M140 S0') and in_body:
            in_body = False
        if ln.startswith(';LAYER:'):
            layer = int(ln[7:])
        if ln.startswith(';TYPE:'):
            typ = ln[6:]

        # --- top-face skin replacement: detect start of a SKIN block on layers 98/99
        if in_body and ln.startswith(';TYPE:SKIN') and layer in TOP_LAYERS:
            # collect the block
            j = i
            blk = []
            while j < n and not (lines[j].startswith(';TYPE:') or lines[j].startswith(';LAYER:') or lines[j].startswith(';TIME_ELAPSED') or lines[j].startswith(';MESH')):
                blk.append(lines[j]); j += 1
            # which face is this block on?
            xs = []; ys = []
            for bl in blk:
                if bl[:2] in ('G0', 'G1'):
                    m = dict(re.findall(r'([XY])(-?[\d.]+)', bl))
                    if 'X' in m: xs.append(float(m['X']))
                    if 'Y' in m: ys.append(float(m['Y']))
            key = None
            if xs:
                mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
                for k, (x0, y0, x1, y1) in TOP_FACES.items():
                    if x0 - 1 < mx < x1 + 1 and y0 - 1 < my < y1 + 1:
                        key = k
            if key is not None:
                out_lines.append(ln)
                # split block into: leading pure-E lines, moves, trailing G0 travels
                lead = []; core = []; trail = []
                k2 = 0
                while k2 < len(blk) and blk[k2].startswith('G1') and 'X' not in blk[k2] and 'Y' not in blk[k2]:
                    lead.append(blk[k2]); k2 += 1
                core = blk[k2:]
                while core and core[-1].startswith('G0'):
                    trail.insert(0, core.pop())
                # emit lead (retract/unretract) with renumbered E
                for bl in lead:
                    m = dict(re.findall(r'([FE])(-?[\d.]+)', bl))
                    e = float(m['E']); d = e - last_e_orig; last_e_orig = e; e_out += d
                    fpart = f" F{m['F']}" if 'F' in m else ''
                    out_lines.append(f"G1{fpart} E{flush_e()}")
                start_xy = (x, y)
                # account original core extrusion (removed)
                for bl in core:
                    if bl[:2] in ('G0', 'G1'):
                        m = dict(re.findall(r'([XYFE])(-?[\d.]+)', bl))
                        if 'E' in m:
                            e = float(m['E']); d = e - last_e_orig; last_e_orig = e
                            if 'X' in m or 'Y' in m:
                                removed_e += d           # dropped extrusion
                            else:
                                e_out += d                # keep retract/unretract semantics
                                out_lines.append(bl.split(' E')[0] + f" E{flush_e()}")
                        if 'X' in m: x = float(m['X'])
                        if 'Y' in m: y = float(m['Y'])
                        if 'F' in m: cur_f = m['F']
                # generate our skin
                moves, e_add, (x, y) = gen_top_skin(key, layer, start_xy)
                out_lines.append(f";JETSON engraved skin ({key[0]},{key[1]})")
                for mv in moves:
                    if mv[0] == 'G0':
                        out_lines.append(f"G0 F{F_TRAVEL} X{fmt(mv[1])} Y{fmt(mv[2])}")
                    elif mv[0] == 'E':
                        e_out += mv[1]
                        out_lines.append(f"G1 F{mv[2]} E{flush_e()}")
                    else:
                        e_out += mv[3]
                        out_lines.append(f"G1 F{mv[4]} X{fmt(mv[1])} Y{fmt(mv[2])} E{flush_e()}")
                cur_f = str(F_HATCH)
                for bl in trail:
                    out_lines.append(bl)
                    m = dict(re.findall(r'([XY])(-?[\d.]+)', bl))
                    if 'X' in m: x = float(m['X'])
                    if 'Y' in m: y = float(m['Y'])
                stats['top_faces'] += 1
                i = j
                continue

        if ln[:2] in ('G0', 'G1') and in_body:
            m = dict(re.findall(r'([XYZEF])(-?[\d.]+)', ln))
            nx = float(m['X']) if 'X' in m else x
            ny = float(m['Y']) if 'Y' in m else y
            if 'F' in m: cur_f = m['F']
            d = None
            if 'E' in m:
                e = float(m['E']); d = e - last_e_orig; last_e_orig = e

            # --- side-face wall cutting
            cut = None
            if (ln.startswith('G1') and typ == 'WALL-OUTER' and d is not None and d > 0 and x is not None
                    and layer in side_cuts and 'X' in m and abs(ny - y) < 0.001):
                for key, ivs in side_cuts[layer].items():
                    f = SIDE_FACES[key]
                    if abs(y - f['y']) < 0.02 and min(x, nx) <= f['cx'] and max(x, nx) >= f['cx']:
                        cut = (key, ivs)
                        break
            if cut is not None:
                key, ivs = cut
                lo, hi = min(x, nx), max(x, nx)
                # kept pieces along [lo,hi]
                keep = []
                pos = lo
                for a, bb in ivs:
                    a = max(a, lo); bb = min(bb, hi)
                    if bb <= pos: continue
                    if a > pos: keep.append((pos, a))
                    pos = max(pos, bb)
                if pos < hi: keep.append((pos, hi))
                if nx < x:   # travelling leftwards
                    keep = [(bb, a) for a, bb in reversed(keep)]
                cur = x
                first_f = m.get('F')
                for a, bb in keep:
                    if abs(a - cur) > 1e-6:
                        gap = abs(a - cur)
                        if gap > 1.5:
                            e_out -= RETRACT
                            out_lines.append(f"G1 F{F_RETRACT} E{flush_e()}")
                            out_lines.append(f"G0 F{F_TRAVEL} X{fmt(a)} Y{fmt(y)}")
                            e_out += RETRACT
                            out_lines.append(f"G1 F{F_RETRACT} E{flush_e()}")
                        else:
                            out_lines.append(f"G0 F{F_TRAVEL} X{fmt(a)} Y{fmt(y)}")
                        stats['side_gaps'] += 1
                        fpart = f" F{cur_f}" if cur_f else ''
                        e_out += abs(bb - a) * E_PER_MM
                        out_lines.append(f"G1{fpart} X{fmt(bb)} Y{fmt(y)} E{flush_e()}")
                    else:
                        e_out += abs(bb - a) * E_PER_MM
                        fpart = f" F{first_f}" if first_f else ''
                        out_lines.append(f"G1{fpart} X{fmt(bb)} Y{fmt(y)} E{flush_e()}")
                    first_f = None
                    cur = bb
                removed_e += d - (hi - lo) * E_PER_MM + sum(abs(bb - a) for a, bb in keep) * E_PER_MM * 0  # bookkeeping only
                stats['side_layers'].add(layer)
                x, y = nx, ny
                continue

            # --- ordinary line: renumber E
            if d is not None:
                e_out += d
                ln = re.sub(r'E-?[\d.]+', f"E{flush_e()}", ln)
            x, y = nx, ny
            out_lines.append(ln)
            continue

        if ln.startswith('G92 E0'):
            last_e_orig = 0.0; e_out = 0.0
        out_lines.append(ln)

    # header note
    hdr_idx = next(k for k, l in enumerate(out_lines) if l.startswith(';Generated with'))
    out_lines.insert(hdr_idx + 1, f";Post-processed: Jetson wordmark engraved 0.4 mm ({orientation} on side faces of outer cubes, top faces of middle cubes)")
    open(out_path, 'w').write('\n'.join(out_lines))
    stats['side_layers'] = (min(stats['side_layers']), max(stats['side_layers'])) if stats['side_layers'] else None
    stats['final_E'] = round(e_out, 3)
    return stats


if __name__ == '__main__':
    for orient in ('horizontal', 'vertical'):
        out = f"CE3E3V2_infinity_cube_jetson_{orient}.gcode"
        print(orient, build(orient, out))
