"""Trace the Jetson wordmark PNG into a shapely polygon; helpers for scaling and slab-intersection."""
import numpy as np
from PIL import Image
from skimage import measure
from shapely.geometry import Polygon, box, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity

LOGO="/root/.claude/skills/synced/9c17e0d4-c47c-4cae-8f32-2f15db45652d_5bd09ffc-0eb7-4f5b-8fe4-96e5dc307140/jetson-brand/assets/logos/rgb/Jetson-Logo-Black-RGB.png"

def wordmark_unit():
    """Wordmark as a shapely geometry with width 1.0, baseline-up (y up), origin at bbox min."""
    a=np.array(Image.open(LOGO))[...,3].astype(float)/255
    a=np.pad(a,2)
    cs=measure.find_contours(a,0.5)
    geom=None
    for c in cs:
        pts=[(p[1],-p[0]) for p in c]          # col→x, row→-y (flip so y is up)
        pg=Polygon(pts).buffer(0)
        if pg.is_empty or pg.area<4: continue
        geom=pg if geom is None else geom.symmetric_difference(pg)
    geom=geom.simplify(0.4)
    minx,miny,maxx,maxy=geom.bounds
    geom=affinity.translate(geom,-minx,-miny)
    geom=affinity.scale(geom,1/(maxx-minx),1/(maxx-minx),origin=(0,0))
    return geom

def wordmark_mm(width, bold=0.0):
    g=affinity.scale(wordmark_unit(),width,width,origin=(0,0))
    if bold: g=g.buffer(bold,join_style=1).buffer(0)
    return g.simplify(0.02)

def slab_intervals(g, zlo, zhi, minw=0.5, mingap=0.35):
    """x-intervals occupied by geometry g between heights zlo..zhi (local coords)."""
    minx,miny,maxx,maxy=g.bounds
    inter=g.intersection(box(minx-1,zlo,maxx+1,zhi))
    if inter.is_empty: return []
    parts=list(inter.geoms) if hasattr(inter,'geoms') else [inter]
    iv=sorted((p.bounds[0],p.bounds[2]) for p in parts if not p.is_empty and p.area>1e-6)
    # merge close intervals
    merged=[]
    for a,b in iv:
        if merged and a-merged[-1][1]<mingap: merged[-1][1]=max(merged[-1][1],b)
        else: merged.append([a,b])
    out=[]
    for a,b in merged:
        if b-a<minw:
            c=(a+b)/2; a,b=c-minw/2,c+minw/2
        out.append((a,b))
    # re-merge after widening
    final=[]
    for a,b in out:
        if final and a-final[-1][1]<mingap: final[-1][1]=max(final[-1][1],b)
        else: final.append([a,b])
    return [tuple(x) for x in final]

if __name__=="__main__":
    g=wordmark_mm(13.4,bold=0.08)
    print("bounds",[round(v,3) for v in g.bounds],"area",round(g.area,2))
    # estimate stroke width: area / (half perimeter)
    print("approx stroke width mm:", round(2*g.area/g.length,3))
    for z in np.arange(0.0,3.2,0.2):
        print(round(z,1), [(round(a,2),round(b,2)) for a,b in slab_intervals(g,z,z+0.2)])
