"""Survey every vertical face of every cube: largest clear (flat, hinge-free) rectangle reachable by outer-wall removal."""
import pickle, collections, math
outer,inner=pickle.load(open('walls.pkl','rb'))
PITCH_X=20.2; PITCH_Y=20.0; X0=77.1; Y0=97.5
def cube_box(i,j): return (X0+PITCH_X*i, Y0+PITCH_Y*j, X0+PITCH_X*(i+1), Y0+PITCH_Y*(j+1))
FACES={'-Y':('y','min'),'+Y':('y','max'),'-X':('x','min'),'+X':('x','max')}

def runs_at(L,i,j,face):
    """straight outer-wall runs of cube (i,j) lying on its extreme plane for this face at layer L -> (plane, [(a,b),...])"""
    x0,y0,x1,y1=cube_box(i,j)
    segs=[s for s in outer[L] if x0-0.3<=(s[0]+s[2])/2<=x1+0.3 and y0-0.3<=(s[1]+s[3])/2<=y1+0.3]
    axis,ext=FACES[face]
    if axis=='y':
        straight=[s for s in segs if abs(s[1]-s[3])<0.01]
        if not straight: return None,[]
        plane=(min if ext=='min' else max)(s[1] for s in straight)
        on=[(min(s[0],s[2]),max(s[0],s[2])) for s in straight if abs(s[1]-plane)<0.03]
    else:
        straight=[s for s in segs if abs(s[0]-s[2])<0.01]
        if not straight: return None,[]
        plane=(min if ext=='min' else max)(s[0] for s in straight)
        on=[(min(s[1],s[3]),max(s[1],s[3])) for s in straight if abs(s[0]-plane)<0.03]
    # merge touching runs
    on.sort(); merged=[]
    for a,b in on:
        if merged and a-merged[-1][1]<0.05: merged[-1][1]=max(merged[-1][1],b)
        else: merged.append([a,b])
    return plane,[tuple(m) for m in merged]

def survey(i,j,face):
    x0,y0,x1,y1=cube_box(i,j)
    axis,ext=FACES[face]
    c=(x0+x1)/2 if axis=='y' else (y0+y1)/2      # coordinate along the face
    nominal=None
    per_layer={}
    for L in range(0,100):
        plane,rs=runs_at(L,i,j,face)
        if plane is None: continue
        per_layer[L]=(plane,rs)
    # nominal plane = the extreme value over mid layers (the flat part of the face)
    planes=[per_layer[L][0] for L in range(30,70) if L in per_layer]
    nominal=(min if ext=='min' else max)(planes)
    # per layer: the run on the nominal plane that contains the face centre (else None)
    run_c={}
    for L,(plane,rs) in per_layer.items():
        if abs(plane-nominal)>0.03: continue
        for a,b in rs:
            if a-0.5<=c<=b+0.5: run_c[L]=(a,b)
    # largest rectangle: over all layer bands [La,Lb] with every layer present, width = intersection
    best=(0,None)
    Ls=sorted(run_c)
    for ia,La in enumerate(Ls):
        a,b=run_c[La]
        for Lb in Ls[ia:]:
            if Lb-1 in run_c or Lb==La:
                pass
            if Lb not in run_c: break
            a=max(a,run_c[Lb][0]); b=min(b,run_c[Lb][1])
            if b-a<=0: break
            area=(b-a)*(Lb-La+1)*0.2
            if area>best[0]: best=(area,(a,b,0.2*La,0.2*Lb+0.2))
    # also the mid-height run
    mid=run_c.get(50)
    return nominal,mid,best

print(f"{'cube':6} {'face':4} {'plane':7} {'run @ z10.2':>16}  largest clear rect (w × h mm)   z-range")
for j in range(2):
    for i in range(4):
        for face in ('-Y','+Y','-X','+X'):
            nominal,mid,best=survey(i,j,face)
            area,r=best
            midtxt=f"{mid[1]-mid[0]:.1f}" if mid else "—"
            if r: print(f"({i},{j})  {face:4} {nominal:7.1f} {midtxt:>16}  {r[1]-r[0]:5.1f} × {r[3]-r[2]:4.1f}   z {r[2]:.1f}–{r[3]:.1f}")
            else: print(f"({i},{j})  {face:4} {nominal:7.1f} {midtxt:>16}  none")
