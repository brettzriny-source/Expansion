import re, sys, math, collections
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def parse(path):
    layer=None;typ=None;x=y=z=None;lastE=None;segs=collections.defaultdict(list);travels=collections.defaultdict(list)
    issues=[];retracts=0;maxd=0;neg=collections.Counter(); absolute=True
    for i,ln in enumerate(open(path)):
        if ln.startswith(';LAYER:'): layer=int(ln[7:]); continue
        if ln.startswith(';TYPE:'): typ=ln[6:].strip(); continue
        if ln.startswith('G91'): absolute=False
        if ln.startswith('G92 E0'): lastE=0.0
        if ln[:2] in('G0','G1') and absolute:
            m=dict(re.findall(r'([XYZEF])(-?[\d.]+)',ln))
            nx=float(m['X']) if 'X' in m else x; ny=float(m['Y']) if 'Y' in m else y
            if 'Z' in m: z=float(m['Z'])
            if 'E' in m and lastE is not None:
                e=float(m['E']); d=e-lastE
                if 'X' in m or 'Y' in m:
                    L=math.hypot(nx-x,ny-y) if x is not None else 0
                    if d<0: issues.append((i+1,'negative E on move',ln.strip()))
                    elif L>0 and d/L>0.09: issues.append((i+1,f'over-extrusion {d/L:.3f}/mm',ln.strip()))
                    elif L>0 and d/L<0.01 and d>0: issues.append((i+1,f'under-extrusion {d/L:.3f}/mm',ln.strip()))
                    if d>0 and layer is not None: segs[layer].append(((x,y),(nx,ny),typ))
                else:
                    neg[round(d,2)]+=1
                    if abs(d)>5.01: issues.append((i+1,f'pure E move {d:.3f}',ln.strip()))
                lastE=e
            elif ln.startswith('G0') and layer is not None and x is not None:
                travels[layer].append(((x,y),(nx,ny)))
            x,y=nx,ny
    return segs,travels,issues,neg

def draw(ax,segs,travels,L,xlim,ylim,title):
    col={'WALL-OUTER':'#0F1F0D','WALL-INNER':'#3CD567','SKIN':'#666858','FILL':'#ACAA93','SKIRT':'#ccc'}
    lc=LineCollection([[a,b] for a,b,t in segs[L]],colors=[col.get(t,'red') for a,b,t in segs[L]],linewidths=1.6)
    ax.add_collection(lc)
    ax.add_collection(LineCollection([[a,b] for a,b in travels[L]],colors='#e0705a',linewidths=0.4,alpha=0.6))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect('equal'); ax.set_title(title,fontsize=9)

if __name__=='__main__':
    for orient in ('horizontal','vertical'):
        path=f"CE3E3V2_infinity_cube_jetson_{orient}.gcode"
        segs,travels,issues,neg=parse(path)
        print(orient,"issues:",len(issues)); [print("  ",x) for x in issues[:10]]
        print("  pure-E deltas:",dict(neg.most_common(6)))
        print("  seg count per layer 50/98/99:",len(segs[50]),len(segs[98]),len(segs[99]))
        fig,axs=plt.subplots(2,2,figsize=(14,11),dpi=130)
        Lmid=50
        draw(axs[0,0],segs,travels,Lmid,(76,158),(96,139),f"{orient}: layer 50 (z 10.2) whole layout")
        draw(axs[0,1],segs,travels,99,(76,158),(96,139),f"{orient}: layer 99 (top) whole layout")
        draw(axs[1,0],segs,travels,99,(100,115),(100,115),f"{orient}: layer 99 middle cube (1,0) skin")
        draw(axs[1,1],segs,travels,98,(120,135),(120,135),f"{orient}: layer 98 middle cube (2,1) skin")
        fig.savefig(f"verify_{orient}.png"); plt.close(fig)
        # side-face elevation: outer wall gaps on y=97.5 across layers -> plot as rectangles
        fig,ax=plt.subplots(figsize=(14,4),dpi=130)
        for L in range(0,100):
            for a,b,t in segs[L]:
                if t=='WALL-OUTER' and abs(a[1]-97.5)<0.02 and abs(b[1]-97.5)<0.02:
                    ax.plot([a[0],b[0]],[0.2*L+0.1]*2,color='#0F1F0D',lw=2.2,solid_capstyle='butt')
        ax.set_xlim(76,158); ax.set_ylim(0,20.5); ax.set_aspect('equal'); ax.set_title(f"{orient}: front face (y=97.5) outer wall, every layer — gaps are the engraving",fontsize=9)
        fig.savefig(f"verify_{orient}_elev.png"); plt.close(fig)
    # original for comparison
    segs,travels,issues,neg=parse("/root/.claude/uploads/3302de19-8fcd-57a8-a3ab-24f1533cfab6/28c316b1-CE3E3V2_infinity_cube.gcode")
    print("original issues:",len(issues),"pure-E:",dict(neg.most_common(4)),"segs 50/98/99:",len(segs[50]),len(segs[98]),len(segs[99]))
