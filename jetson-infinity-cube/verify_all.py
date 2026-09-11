import re, math, collections, sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from verify import parse, draw
path="CE3E3V2_infinity_cube_jetson_allfaces.gcode"
segs,travels,issues,neg=parse(path)
print("issues:",len(issues)); [print("  ",x) for x in issues[:8]]
print("pure-E deltas:",dict(neg.most_common(4)))
# feedrate audit
f=None; fast=0; absolute=True
for ln in open(path):
    if ln.startswith('G91'): absolute=False
    if ln[:2] in ('G0','G1') and absolute:
        m=dict(re.findall(r'([XYEF])(-?[\d.]+)',ln))
        if 'F' in m: f=float(m['F'])
        if ln.startswith('G1') and 'E' in m and ('X' in m or 'Y' in m) and f and f>3000: fast+=1
print("extrusion moves faster than F3000:",fast)
print("rings blocks:",sum(1 for ln in open(path) if ln.startswith(';JETSON rings')))
# elevations: for each plane draw outer-wall runs per layer
def elev(ax,axis,plane,lo,hi,title):
    for L in range(0,100):
        for a,b,t in segs[L]:
            if t!='WALL-OUTER': continue
            if axis=='y' and abs(a[1]-plane)<0.02 and abs(b[1]-plane)<0.02: ax.plot([a[0],b[0]],[0.2*L+0.1]*2,color='#0F1F0D',lw=1.5,solid_capstyle='butt')
            if axis=='x' and abs(a[0]-plane)<0.02 and abs(b[0]-plane)<0.02: ax.plot([a[1],b[1]],[0.2*L+0.1]*2,color='#0F1F0D',lw=1.5,solid_capstyle='butt')
    ax.set_xlim(lo,hi); ax.set_ylim(0,20.5); ax.set_aspect('equal'); ax.set_title(title,fontsize=8); ax.tick_params(labelsize=6)
fig,axs=plt.subplots(4,1,figsize=(14,13),dpi=130)
elev(axs[0],'y',97.5,76,159,"FRONT  y=97.5  (viewed from -Y; +X to the right)")
elev(axs[1],'y',137.5,76,159,"BACK  y=137.5  (viewed from +Y; mirrored here, so text appears reversed)")
elev(axs[2],'y',117.1,76,159,"inner face of front row  y=117.1  (faces +Y; appears reversed here)")
elev(axs[3],'y',117.9,76,159,"inner face of back row  y=117.9  (faces -Y)")
plt.tight_layout(); fig.savefig("all_elev_y.png"); plt.close(fig)
fig,axs=plt.subplots(2,4,figsize=(15,8),dpi=130)
for ax,(p,t) in zip(axs.flat,[(77.1,"LEFT end x=77.1 (faces -X; appears reversed)"),(96.7,"x=96.7 cube0 +X"),(97.5,"x=97.5 cube1 -X (reversed)"),(117.1,"x=117.1 cube1 +X"),(117.9,"x=117.9 cube2 -X (reversed)"),(137.5,"x=137.5 cube2 +X"),(138.3,"x=138.3 cube3 -X (reversed)"),(157.9,"RIGHT end x=157.9 (faces +X)")]):
    elev(ax,'x',p,96,139,t)
plt.tight_layout(); fig.savefig("all_elev_x.png"); plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(16,6),dpi=130)
draw(axs[0],segs,travels,99,(76,158),(96,139),"layer 99 (top)")
draw(axs[1],segs,travels,98,(76,158),(96,139),"layer 98")
plt.tight_layout(); fig.savefig("all_top.png"); plt.close(fig)
print("segs per layer 50/98/99:",len(segs[50]),len(segs[98]),len(segs[99]))
