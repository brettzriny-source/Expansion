"""
Engrave a checkerboard of Jetson wordmarks and lightning bolts into every reachable face of the
Cura-sliced infinity cube (Ender-3 V2, 0.2 mm layers, single colour).

Per cube: 4 vertical faces (outer-wall bead removed where the design falls, inner wall = recess
floor) + the top face (top two skin layers clipped around the design, perimeter bead added).
Bottom faces are left alone.  Every face gets the largest design its clear rectangle allows,
choosing horizontal / vertical / diagonal for the wordmark.  E values are renumbered throughout.
"""
import re, math, pickle, collections, json
import numpy as np
from shapely.geometry import box, LineString, Polygon, Point
from shapely import affinity
from shapely.ops import unary_union
from logo_geom import wordmark_mm, slab_intervals

SRC = "/root/.claude/uploads/3302de19-8fcd-57a8-a3ab-24f1533cfab6/28c316b1-CE3E3V2_infinity_cube.gcode"
OUT = "CE3E3V2_infinity_cube_jetson_allfaces.gcode"
E_PER_MM = 0.4 * 0.2 / (math.pi * 0.875 ** 2)
RETRACT, F_RETRACT, F_TRAVEL, F_PERIM = 5.0, 2700, 9000, 600
LAYER_H = 0.2
BOLD, MIN_CAV, MIN_GAP, MARGIN = 0.08, 0.5, 0.35, 0.4
WM_ASPECT = 0.2405                       # wordmark height / width (with BOLD)

XB = [77.1, 97.1, 117.5, 137.9, 157.9]   # cube column boundaries (between the 0.8 mm gaps)
YB = [97.5, 117.5, 137.5]
WORD_CUBES = {(0, 0), (2, 0), (1, 1), (3, 1)}          # checkerboard; the rest get bolts
TOP_LAYERS = (98, 99)
TOP_CLEAR = {   # clear skin rectangle on the top face (outer cubes lose the hinge strip)
    (0, 0): (80.8, 101.2, 93.0, 109.3), (3, 0): (142.0, 101.2, 154.2, 109.3),
    (0, 1): (80.8, 125.7, 93.0, 133.8), (3, 1): (142.0, 125.7, 154.2, 133.8),
    (1, 0): (101.2, 101.2, 113.4, 113.4), (1, 1): (101.2, 121.6, 113.4, 133.8),
    (2, 0): (121.6, 101.2, 133.8, 113.4), (2, 1): (121.6, 121.6, 133.8, 133.8),
}
# face -> (axis of the plane, min/max, does +u run against the bed axis when viewed from outside?)
FACES = {'-Y': ('y', 'min', False), '+Y': ('y', 'max', True), '-X': ('x', 'min', True), '+X': ('x', 'max', False)}


def fmt(v):
    s = f"{v:.5f}".rstrip('0').rstrip('.')
    return s if s not in ('', '-0') else '0'


def cube_box(i, j):
    return (XB[i], YB[j], XB[i + 1], YB[j + 1])


# ----------------------------------------------------------------------------- designs
def bolt(h):
    pts = [(0.45, 1), (0.15, 0.45), (0.42, 0.45), (0.28, 0), (0.85, 0.55), (0.55, 0.55), (0.75, 1)]
    g = Polygon([(x * h, y * h) for x, y in pts])
    b = g.bounds
    return affinity.translate(g, -(b[0] + b[2]) / 2, -(b[1] + b[3]) / 2)


def wordmark(W, orient):
    g = wordmark_mm(W, bold=BOLD)
    if orient == 'vertical':
        g = affinity.rotate(g, 90, origin=(0, 0))
    elif orient == 'diagonal':
        g = affinity.rotate(g, 45, origin=(0, 0))
    b = g.bounds
    return affinity.translate(g, -(b[0] + b[2]) / 2, -(b[1] + b[3]) / 2)


def fit_wordmark(w, h):
    w -= MARGIN; h -= MARGIN; r = WM_ASPECT
    cands = [(min(w, h / r), 'horizontal'), (min(h, w / r), 'vertical'),
             (min(w, h) / ((1 + r) / math.sqrt(2)), 'diagonal')]
    return max(cands)


def design_for(key, w, h):
    if key in WORD_CUBES:
        W, o = fit_wordmark(w, h)
        return wordmark(W, o), f"wordmark {o} {W:.1f} mm"
    hb = min(w, h) - 1.6
    return bolt(hb), f"bolt {hb:.1f} mm"


# ----------------------------------------------------------------------------- face survey
def survey_faces(outer):
    faces = {}
    for j in range(2):
        for i in range(4):
            x0, y0, x1, y1 = cube_box(i, j)
            for fname, (axis, ext, mirror) in FACES.items():
                c = (x0 + x1) / 2 if axis == 'y' else (y0 + y1) / 2
                per = {}
                for L in range(0, 100):
                    segs = [s for s in outer.get(L, []) if x0 <= (s[0] + s[2]) / 2 <= x1 and y0 <= (s[1] + s[3]) / 2 <= y1]
                    if axis == 'y':
                        st = [s for s in segs if abs(s[1] - s[3]) < 0.01]
                        if not st: continue
                        plane = (min if ext == 'min' else max)(s[1] for s in st)
                        on = [(min(s[0], s[2]), max(s[0], s[2])) for s in st if abs(s[1] - plane) < 0.03]
                    else:
                        st = [s for s in segs if abs(s[0] - s[2]) < 0.01]
                        if not st: continue
                        plane = (min if ext == 'min' else max)(s[0] for s in st)
                        on = [(min(s[1], s[3]), max(s[1], s[3])) for s in st if abs(s[0] - plane) < 0.03]
                    on.sort(); merged = []
                    for a, b in on:
                        if merged and a - merged[-1][1] < 0.05: merged[-1][1] = max(merged[-1][1], b)
                        else: merged.append([a, b])
                    per[L] = (plane, merged)
                planes = [per[L][0] for L in range(30, 70) if L in per]
                nominal = (min if ext == 'min' else max)(planes)
                run_c = {}
                for L, (plane, rs) in per.items():
                    if abs(plane - nominal) > 0.03: continue
                    for a, b in rs:
                        if a - 0.5 <= c <= b + 0.5: run_c[L] = (a, b)
                best = (0, None)
                Ls = sorted(run_c)
                for ia, La in enumerate(Ls):
                    a, b = run_c[La]
                    for Lb in Ls[ia:]:
                        if Lb not in run_c or (Lb > La and Lb - 1 not in run_c): break
                        a = max(a, run_c[Lb][0]); b = min(b, run_c[Lb][1])
                        if b - a <= 0: break
                        area = (b - a) * (Lb - La + 1) * LAYER_H
                        if area > best[0]: best = (area, (a, b, LAYER_H * La, LAYER_H * Lb + LAYER_H))
                a, b, zlo, zhi = best[1]
                faces[(i, j, fname)] = dict(axis=axis, plane=round(nominal, 3), mirror=mirror, a=a, b=b, zlo=zlo, zhi=zhi)
    return faces


# ----------------------------------------------------------------------------- build
def build():
    outer, inner = pickle.load(open('walls.pkl', 'rb'))
    faces = survey_faces(outer)
    report = []

    # per-layer wall cuts: cuts[L] = list of (axis, plane, run(a,b), [intervals along face axis])
    cuts = collections.defaultdict(list)
    for (i, j, fname), f in faces.items():
        w, h = f['b'] - f['a'], f['zhi'] - f['zlo']
        g, desc = design_for((i, j), w, h)
        u0, zc = (f['a'] + f['b']) / 2, (f['zlo'] + f['zhi']) / 2
        ngaps = 0
        for L in range(0, 100):
            zm = LAYER_H * L + LAYER_H / 2
            if not (f['zlo'] <= zm <= f['zhi']): continue
            iv = slab_intervals(g, zm - zc - 0.005, zm - zc + 0.005, MIN_CAV, MIN_GAP)
            if not iv: continue
            bed = [(u0 - bb, u0 - a) if f['mirror'] else (u0 + a, u0 + bb) for a, bb in iv]
            bed = [(max(a, f['a'] + 0.1), min(bb, f['b'] - 0.1)) for a, bb in bed]
            bed = [(a, bb) for a, bb in bed if bb - a > 0.2]
            if bed:
                cuts[L].append((f['axis'], f['plane'], (f['a'], f['b']), sorted(bed)))
                ngaps += len(bed)
        report.append(f"({i},{j}) {fname:3} plane {f['plane']:6.1f}  clear {w:4.1f} x {h:4.1f} mm  z {f['zlo']:.1f}-{f['zhi']:.1f}  -> {desc}  ({ngaps} gaps)")

    # top designs
    top_excl, top_rings = {}, {}
    for key, (x0, y0, x1, y1) in TOP_CLEAR.items():
        w, h = x1 - x0, y1 - y0
        g, desc = design_for(key, w, h)
        g = affinity.translate(g, (x0 + x1) / 2, (y0 + y1) / 2)
        top_excl[key] = g.buffer(0.4, join_style=1)
        rg = g.buffer(0.2, join_style=1).simplify(0.02)
        rings = []
        for p in (rg.geoms if hasattr(rg, 'geoms') else [rg]):
            rings.append(list(p.exterior.coords))
            rings += [list(r.coords) for r in p.interiors]
        top_rings[key] = rings
        report.append(f"({key[0]},{key[1]}) top  clear {w:4.1f} x {h:4.1f} mm -> {desc}")
    excl_union = unary_union(list(top_excl.values()))

    def cube_of(px, py):
        for j in range(2):
            for i in range(4):
                x0, y0, x1, y1 = cube_box(i, j)
                if x0 - 0.5 <= px <= x1 + 0.5 and y0 - 0.5 <= py <= y1 + 0.5:
                    return (i, j)
        return None

    lines = open(SRC).read().split('\n')
    out = []
    blk_pts = []      # points of the current top-layer skin block, to pick its cube
    layer = None; typ = None
    x = y = None                 # position according to the ORIGINAL file
    phys = None                  # where the nozzle really is (differs after dropped moves)
    last_e = 0.0; e_out = 0.0
    cur_f = None; need_f = False
    in_body = False
    stats = collections.Counter()

    def emit_travel(px, py, force_retract=False):
        nonlocal phys, e_out, need_f
        d = math.hypot(px - phys[0], py - phys[1]) if phys else 99
        if d < 1e-6: return
        if d > 1.5 or force_retract:
            e_out -= RETRACT; out.append(f"G1 F{F_RETRACT} E{fmt(e_out)}")
            out.append(f"G0 F{F_TRAVEL} X{fmt(px)} Y{fmt(py)}")
            e_out += RETRACT; out.append(f"G1 F{F_RETRACT} E{fmt(e_out)}")
            stats['retract_travels'] += 1
        else:
            out.append(f"G0 F{F_TRAVEL} X{fmt(px)} Y{fmt(py)}")
            stats['short_travels'] += 1
        phys = (px, py); need_f = True

    def emit_extrude(px, py, rate, F=None):
        nonlocal phys, e_out, need_f
        d = math.hypot(px - phys[0], py - phys[1])
        if d < 1e-6: return
        e_out += d * rate
        f = F if F is not None else (cur_f if need_f else None)
        out.append(f"G1{(' F' + str(f)) if f is not None else ''} X{fmt(px)} Y{fmt(py)} E{fmt(e_out)}")
        phys = (px, py); need_f = F is not None and str(F) != str(cur_f)

    def pieces_of(ax0, ay0, ax1, ay1, intervals, axis):
        """kept sub-segments of an axis-aligned segment after removing intervals (along-axis coords)"""
        lo_c, hi_c = (ax0, ax1) if axis == 'y' else (ay0, ay1)
        lo, hi = min(lo_c, hi_c), max(lo_c, hi_c)
        keep = []; pos = lo
        for a, b in intervals:
            a, b = max(a, lo), min(b, hi)
            if b <= pos: continue
            if a > pos: keep.append((pos, a))
            pos = max(pos, b)
        if pos < hi: keep.append((pos, hi))
        if hi_c < lo_c: keep = [(b, a) for a, b in reversed(keep)]
        return keep

    def after_skin_extrusion(px, py, idx):
        """called after every extrusion in a top-layer SKIN block; at block end, add the rings"""
        nonlocal need_f
        blk_pts.append((px, py))
        k = idx
        while k < n and (lines[k].startswith('G0') or (lines[k].startswith('G1') and 'X' not in lines[k] and 'Y' not in lines[k])):
            k += 1
        if not (k < n and lines[k][:5] in (';TYPE', ';LAYE', ';MESH', ';TIME')):
            return
        counts = collections.Counter()
        for qx, qy in blk_pts:
            for key, (x0, y0, x1, y1) in TOP_CLEAR.items():
                if x0 - 0.3 <= qx <= x1 + 0.3 and y0 - 0.3 <= qy <= y1 + 0.3:
                    counts[key] += 1
        if not counts:
            return
        key = counts.most_common(1)[0][0]
        if (layer, key) in stats:
            return
        stats[(layer, key)] = 1
        out.append(f";JETSON rings ({key[0]},{key[1]})")
        rem = [r[:] for r in top_rings[key]]
        while rem:
            rem.sort(key=lambda r: min(math.hypot(qx - phys[0], qy - phys[1]) for qx, qy in r[::max(1, len(r) // 12)]))
            r = rem.pop(0)
            i0 = min(range(len(r)), key=lambda q: math.hypot(r[q][0] - phys[0], r[q][1] - phys[1]))
            r = r[i0:] + r[1:i0 + 1]
            emit_travel(*r[0])
            for qx, qy in r[1:]:
                emit_extrude(qx, qy, E_PER_MM, F=F_PERIM)
            stats['rings'] += 1
        need_f = True

    i = 0; n = len(lines)
    while i < n:
        ln = lines[i]; i += 1
        if ln.startswith(';LAYER:0'): in_body = True
        if ln.startswith('M140 S0') and in_body: in_body = False
        if ln.startswith(';LAYER:'): layer = int(ln[7:])
        if ln.startswith(';TYPE:'): typ = ln[6:]; blk_pts = []
        if ln.startswith('G92 E0'):
            last_e = 0.0; e_out = 0.0

        if not (in_body and ln[:2] in ('G0', 'G1')):
            out.append(ln); continue

        m = dict(re.findall(r'([XYZEF])(-?[\d.]+)', ln))
        nx = float(m['X']) if 'X' in m else x
        ny = float(m['Y']) if 'Y' in m else y
        has_xy = 'X' in m or 'Y' in m
        d = None
        if 'E' in m:
            e = float(m['E']); d = e - last_e; last_e = e
        if 'F' in m: cur_f = m['F']

        # ---------------- wall cut on vertical faces
        if (ln.startswith('G1') and typ == 'WALL-OUTER' and d is not None and d > 0 and has_xy
                and x is not None and layer in cuts):
            horiz = abs(ny - y) < 0.001 and abs(nx - x) > 0.001
            vert = abs(nx - x) < 0.001 and abs(ny - y) > 0.001
            hit = None
            for axis, plane, run, ivs in cuts[layer]:
                if axis == 'y' and horiz and abs(y - plane) < 0.02 and min(x, nx) < run[1] and max(x, nx) > run[0]:
                    hit = (axis, ivs); break
                if axis == 'x' and vert and abs(x - plane) < 0.02 and min(y, ny) < run[1] and max(y, ny) > run[0]:
                    hit = (axis, ivs); break
            if hit:
                axis, ivs = hit
                if phys is None or math.hypot(phys[0] - x, phys[1] - y) > 1e-6:
                    emit_travel(x, y)
                seglen = math.hypot(nx - x, ny - y); rate = d / seglen
                for a, b in pieces_of(x, y, nx, ny, ivs, axis):
                    pa = (a, y) if axis == 'y' else (x, a)
                    pb = (b, y) if axis == 'y' else (x, b)
                    if math.hypot(pa[0] - phys[0], pa[1] - phys[1]) > 1e-6:
                        emit_travel(*pa); stats['wall_gaps'] += 1
                    emit_extrude(*pb, rate, F=m.get('F') if need_f or 'F' in m else None)
                # nozzle may be short of the true endpoint (endpoint inside a cavity) - travel there
                if math.hypot(phys[0] - nx, phys[1] - ny) > 1e-6:
                    emit_travel(nx, ny)
                x, y = nx, ny
                continue

        # ---------------- skin clipping on top layers
        if (ln.startswith('G1') and typ == 'SKIN' and layer in TOP_LAYERS and d is not None and d > 0 and has_xy
                and x is not None):
            seg = LineString([(x, y), (nx, ny)])
            if seg.intersects(excl_union):
                if phys is None or math.hypot(phys[0] - x, phys[1] - y) > 1e-6:
                    emit_travel(x, y)
                kept = seg.difference(excl_union)
                parts = [] if kept.is_empty else (list(kept.geoms) if hasattr(kept, 'geoms') else [kept])
                parts = [p for p in parts if p.geom_type == 'LineString' and p.length > 0.15]
                # order pieces along the segment direction
                parts.sort(key=lambda p: seg.project(p.interpolate(0.5, normalized=True)))
                rate = d / seg.length
                for p in parts:
                    c = list(p.coords)
                    if seg.project(Point(c[0])) > seg.project(Point(c[-1])):   # orient along travel direction
                        c = c[::-1]
                    if math.hypot(c[0][0] - phys[0], c[0][1] - phys[1]) > 1e-6:
                        emit_travel(*c[0]); stats['skin_gaps'] += 1
                    emit_extrude(*c[-1], rate, F=m.get('F') if need_f or 'F' in m else None)
                # if the endpoint lies inside the cavity we stay put; the next move resyncs
                x, y = nx, ny
                after_skin_extrusion(nx, ny, i)
                continue

        # ---------------- ordinary line
        # if the logical and physical positions diverged (dropped tail), a plain travel resyncs them;
        # an extrusion must start from the logical point
        if (has_xy and phys is not None and x is not None and math.hypot(phys[0] - x, phys[1] - y) > 1e-6
                and ln.startswith('G1') and d is not None and d > 0):
            emit_travel(x, y)          # a G0 needs nothing: it moves to its own absolute target
        if d is not None:
            e_out += d
            ln = re.sub(r'E-?[\d.]+', f"E{fmt(e_out)}", ln)
        if has_xy:
            if ln.startswith('G1') and d is not None and d > 0 and need_f and 'F' not in m and cur_f:
                ln = ln.replace('G1 ', f'G1 F{cur_f} ', 1)
                need_f = False
            if 'F' in m: need_f = False
            phys = (nx, ny)
        x, y = nx, ny
        out.append(ln)

        if typ == 'SKIN' and layer in TOP_LAYERS and ln.startswith('G1') and d is not None and d > 0 and has_xy:
            after_skin_extrusion(nx, ny, i)

    hdr = next(k for k, l in enumerate(out) if l.startswith(';Generated with'))
    out.insert(hdr + 1, ";Post-processed: Jetson wordmark / bolt checkerboard engraved 0.4 mm into 4 side faces + top of every cube")
    open(OUT, 'w').write('\n'.join(out))
    stats['final_E'] = round(e_out, 3)
    return report, {k: v for k, v in stats.items() if isinstance(k, str)}


if __name__ == '__main__':
    report, stats = build()
    print('\n'.join(report))
    print(stats)
