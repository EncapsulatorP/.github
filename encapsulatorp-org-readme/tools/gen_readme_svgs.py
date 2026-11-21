import math, random, os, sys
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
DEEP='#163b43'; PANEL='#203f47'; ON='#edf4eb'; MUTED='#bfd2c8'; MINT='#b6e0d2'; TEAL='#4fb3a5'; GOLD='#e8c170'; CORAL='#f08a6c'; LINE='#35585f'
SERIF="Georgia,'Times New Roman',serif"; MONO="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"; SANS="-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
facts = {}

def css(extra=''):
    return f"""<style>
.t{{font-family:{SERIF};fill:{ON}}} .m{{font-family:{MONO};fill:{MUTED}}} .s{{font-family:{SANS};fill:{MUTED}}}
.k{{font-family:{MONO};fill:{MINT};letter-spacing:2px}} .g{{fill:{GOLD}}} .c{{fill:{CORAL}}} .w{{fill:{ON}}}
.draw{{stroke-dasharray:1;stroke-dashoffset:1;animation:dr 14s cubic-bezier(.5,0,.3,1) infinite}}
@keyframes dr{{0%{{stroke-dashoffset:1;opacity:1}}25%{{stroke-dashoffset:0}}95%{{stroke-dashoffset:0;opacity:1}}100%{{stroke-dashoffset:0;opacity:0}}}}
.pop{{opacity:.2;animation:pop 14s ease-out infinite}}
@keyframes pop{{0%{{opacity:.2}}6%{{opacity:1}}95%{{opacity:1}}100%{{opacity:.2}}}}
.pulse{{animation:pu 2.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
@keyframes pu{{0%,100%{{transform:scale(1);opacity:1}}50%{{transform:scale(1.9);opacity:.35}}}}
.spin{{animation:sp 80s linear infinite;transform-box:fill-box;transform-origin:center}}
@keyframes sp{{to{{transform:rotate(360deg)}}}}
{extra}</style>"""

def card(w,h,body,label,extra=''):
    grid=''.join(f'<path d="M{x} 0V{h}" stroke="{LINE}" stroke-width="1" opacity=".18"/>' for x in range(40,w,40))
    grid+=''.join(f'<path d="M0 {y}H{w}" stroke="{LINE}" stroke-width="1" opacity=".18"/>' for y in range(40,h,40))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">'
            f'{css(extra)}<rect width="{w}" height="{h}" rx="18" fill="{DEEP}"/><g>{grid}</g>{body}</svg>')

def path(pts): return 'M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
import re as _re
def ghost(svg):
    def f(m):
        tag=m.group(0)
        g=tag.replace(' class="draw"','').replace(' pathLength="1"','').replace(' id="up"','').replace(' id="orb"','')
        g=_re.sub(r' opacity="[^"]*"','',g); g=g[:-2]+' opacity=".22"/>'
        return g+tag
    return _re.sub(r'<(?:path|circle)[^>]*class="draw"[^>]*/>',f,svg)
def save(name,svg):
    svg=ghost(svg)
    open(os.path.join(OUT,name),'w',encoding='utf-8').write(svg); print(name,len(svg))
def head(kicker,title,x=32,y=44,size=30):
    return f'<text x="{x}" y="{y}" class="k" font-size="13">{kicker}</text><text x="{x}" y="{y+38}" class="t" font-size="{size}">{title}</text>'

# ---------- towers ----------
def phases(c):
    L=math.log(c); v=1.0
    for _ in range(4000): v=math.exp(L*math.exp(-L*v))
    return c**(-v), v
W0=lambda x:(lambda f:f(f))(lambda f:None)
def lambertw(x):
    w=0.5
    for _ in range(100): w-= (w*math.exp(w)-x)/(math.exp(w)*(w+1))
    return w
vmax=math.exp(lambertw(1/math.e)); cmax=math.exp(1/vmax)
assert abs(phases(cmax)[1]-vmax)<1e-9
bound=4*math.exp(1/math.e-2)
u111,v111=phases(1.11)
# second base with the same upper phase
lo,hi=cmax,60.0
for _ in range(200):
    mid=(lo+hi)/2
    if phases(mid)[1]>v111: lo=mid
    else: hi=mid
c2=(lo+hi)/2
facts.update(vmax=vmax,cmax=cmax,bound=bound,v111=v111,u111=u111,c2=c2)
def towers():
    w,h=880,400; x0,x1,y0,y1=60,470,340,110
    cs=[math.exp(math.log(1.0005)+(math.log(40)-math.log(1.0005))*i/400) for i in range(401)]
    X=lambda c:x0+(x1-x0)*math.log(c)/math.log(40); Yv=lambda v:y0+(y1-y0)*v/1.4
    up=[(X(c),Yv(phases(c)[1])) for c in cs]; lowr=[(X(c),Yv(phases(c)[0])) for c in cs]
    b=head('TOWERS · EXACT RESULT','A sharp ceiling for sign-flipping towers')
    b+=f'<path d="M{x0} {Yv(1):.1f}H{x1}" stroke="{MUTED}" stroke-dasharray="3 5" opacity=".6"/><text x="{x1+8}" y="{Yv(1)+4:.1f}" class="m" font-size="12">1</text>'
    b+=f'<path d="M{x0} {y0}H{x1}M{x0} {y0}V{y1-10}" stroke="{MUTED}" opacity=".7"/>'
    for c in (1.11,2,4,10,25):
        b+=f'<text x="{X(c):.1f}" y="{y0+20}" class="m" font-size="12" text-anchor="middle">{c}</text><path d="M{X(c):.1f} {y0}v5" stroke="{MUTED}"/>'
    b+=f'<text x="{x1}" y="{y0+40}" class="m" font-size="12" text-anchor="end">base c (log scale)</text>'
    b+=f'<path d="{path(lowr)}" fill="none" stroke="{TEAL}" stroke-width="2.5" pathLength="1" class="draw"/>'
    b+=f'<path id="up" d="{path(up)}" fill="none" stroke="{GOLD}" stroke-width="3" pathLength="1" class="draw"/>'
    b+=f'<circle r="5" fill="{ON}"><animateMotion dur="14s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.25;1" calcMode="linear"><mpath href="#up"/></animateMotion></circle>'
    yb=Yv(v111)
    b+=f'<g class="pop" style="animation-delay:3s"><path d="M{X(1.11):.1f} {yb:.1f}H{X(c2):.1f}" stroke="{CORAL}" stroke-width="1.5" stroke-dasharray="5 4"/><circle cx="{X(1.11):.1f}" cy="{yb:.1f}" r="5" fill="{CORAL}"/><circle cx="{X(c2):.1f}" cy="{yb:.1f}" r="5" fill="{CORAL}"/>'
    b+=f'<text x="{X(5):.1f}" y="{Yv(0.86):.1f}" class="m c" font-size="12" text-anchor="middle">same excess at c = 1.11 and c ≈ {c2:.2f}</text></g>'
    b+=f'<circle cx="{X(cmax):.1f}" cy="{Yv(vmax):.1f}" r="6" fill="{GOLD}" class="pulse"/><text x="{X(cmax):.1f}" y="{Yv(vmax)-16:.1f}" class="m g" font-size="13" text-anchor="middle">v_max ≈ {vmax:.4f}</text>'
    b+=f'<text x="{X(9):.1f}" y="{Yv(1.3):.1f}" class="m g" font-size="12">upper phase v</text><text x="{X(4.5):.1f}" y="{Yv(0.3):.1f}" class="m" font-size="12" style="fill:{TEAL}">lower phase u</text>'
    tx=510
    rows=[('u = c^(−v),  v = c^u',ON,15),('a unique pair of phases for every c &gt; 1',MUTED,13),('',ON,8),
          (f'|F′| ≤ 4·e^(1/e−2) ≈ {bound:.3f} &lt; 1',ON,15),('one contraction bound, all bases',MUTED,13),('',ON,8),
          (f'v_max = exp(W₀(1/e)) ≈ {vmax:.6f}',GOLD,15),(f'reached at c ≈ {cmax:.6f}',MUTED,13),('',ON,8),
          ('Every smaller excess: exactly two bases',CORAL,14),('so matching a constant is tunable',MUTED,13)]
    y=150
    for t,col,fs in rows:
        if t: b+=f'<text x="{tx}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{col}">{t}</text>'
        y+=fs+9 if t else 8
    b+=f'<text x="{tx}" y="{h-28}" class="s" font-size="12">Written proof · Lean check pending</text>'
    save('towers.svg',card(w,h,b,'Sign-flipping power towers: two phases, a sharp maximum and the two-base construction'))

# ---------- logistic ----------
def logistic():
    w,h=600,400; x0,x1,y0,y1=40,400,330,110
    rs=1+math.sqrt(6); segs=[]
    R=lambda r:x0+(x1-x0)*(r-2.8)/(4-2.8); Y=lambda x:y0+(y1-y0)*x
    N=300
    for i in range(N):
        r=2.8+1.2*i/(N-1); x=0.5
        for _ in range(500): x=r*x*(1-x)
        seen=set()
        for _ in range(40 if r>3.4 else 4):
            x=r*x*(1-x); seen.add(round(Y(x),1))
        for yy in seen: segs.append(f'M{R(r):.1f} {yy}h.9')
    b=head('DYNAMICS · EXACT RESULT','The logistic quarter-turn',size=26)
    b+=f'<path d="{"".join(segs)}" stroke="{MINT}" stroke-width="1.1" opacity=".85"/>'
    b+=f'<path d="M{R(rs):.1f} {y1-6}V{y0}" stroke="{GOLD}" stroke-width="1.5" stroke-dasharray="4 4"/><text x="{R(rs):.1f}" y="{y0+22}" class="m g" font-size="13" text-anchor="middle">r* = 1 + √6</text>'
    b+=f'<text x="{x0}" y="{y0+22}" class="m" font-size="12">r = 2.8</text><text x="{x1}" y="{y0+22}" class="m" font-size="12" text-anchor="end">4</text>'
    cx,cy=495,205
    b+=f'<circle cx="{cx}" cy="{cy}" r="62" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>'
    for a in range(4):
        b+=f'<circle cx="{cx+62*math.cos(a*math.pi/2):.1f}" cy="{cy-62*math.sin(a*math.pi/2):.1f}" r="4" fill="{MUTED}"/>'
    b+=(f'<g><path d="M{cx} {cy}H{cx+54}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><circle cx="{cx+54}" cy="{cy}" r="6" fill="{GOLD}"/>'
        f'<animateTransform attributeName="transform" type="rotate" dur="6s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.25;.5;.75;1" keySplines=".7 0 .3 1;.7 0 .3 1;.7 0 .3 1;.7 0 .3 1" values="0 {cx} {cy};-90 {cx} {cy};-180 {cx} {cy};-270 {cx} {cy};-360 {cx} {cy}"/></g>')
    b+=f'<text x="{cx}" y="{cy+98}" font-family="{MONO}" font-size="16" fill="{ON}" text-anchor="middle">C² = −I</text><text x="{cx}" y="{cy+120}" font-family="{MONO}" font-size="16" fill="{ON}" text-anchor="middle">C⁴ = I</text>'
    b+=f'<text x="{cx}" y="{cy-84}" class="s" font-size="12" text-anchor="middle">two-cycle response matrix</text>'
    b+=f'<text x="{x0}" y="{h-14}" class="s" font-size="12">C_r² = (4 + 2r − r²)·I, which equals −I exactly where the two-cycle period-doubles.</text>'
    assert abs(4+2*rs-rs*rs+1)<1e-12
    save('logistic.svg',card(w,h,b,'Logistic map: at r = 1 + sqrt 6 the two-cycle response matrix squares to minus the identity'))

# ---------- goldbach ----------
def isp(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
def goldbach():
    w,h=600,400; N=100; m=N//2; x0,x1,yb=40,560,300
    X=lambda n:x0+(x1-x0)*n/N
    pairs=[(p,N-p) for p in range(2,m+1) if isp(p) and isp(N-p)]
    M=sum(isp(k) for k in range(1,N)); C=sum(1 for k in range(1,N) if isp(k) and isp(N-k)); rho=(M-C)/(2*M)
    facts.update(gpairs=len(pairs),M=M,C=C,rho=rho)
    b=head('PRIME PAIRS · EXACT IDENTITY','One centre. Every prime pair.',size=26)
    b+=f'<path d="M{x0} {yb}H{x1}" stroke="{MUTED}" opacity=".7"/>'
    for n in range(1,N):
        if isp(n): b+=f'<circle cx="{X(n):.1f}" cy="{yb}" r="2.6" fill="{MINT}"/>'
    b+=f'<path d="M{X(m)} {yb-190}V{yb+10}" stroke="{GOLD}" stroke-dasharray="3 5"/><text x="{X(m)}" y="{yb+28}" class="m g" font-size="13" text-anchor="middle">m = 50</text>'
    for i,(p,q) in enumerate(reversed(pairs)):
        r=(X(q)-X(p))/2; d=(q-p)//2
        b+=(f'<g class="pop" style="animation-delay:{0.6+i*0.8:.1f}s"><path d="M{X(p):.1f} {yb}A{r:.1f} {r*0.72:.1f} 0 0 1 {X(q):.1f} {yb}" fill="none" stroke="{GOLD}" stroke-width="2"/>'
            f'<circle cx="{X(p):.1f}" cy="{yb}" r="4.5" fill="{GOLD}"/><circle cx="{X(q):.1f}" cy="{yb}" r="4.5" fill="{GOLD}"/>'
            f'<text x="{X(m)+6}" y="{yb-r*0.72-5:.1f}" class="m" font-size="11" fill="{ON}">{p}+{q}</text></g>')
    b+=f'<text x="{x0}" y="{yb+28}" class="m" font-size="12">0</text><text x="{x1}" y="{yb+28}" class="m" font-size="12" text-anchor="end">N = 100</text>'
    b+=f'<text x="{x0}" y="{h-42}" font-family="{MONO}" font-size="14" fill="{ON}">pq = m² − d²   ·   ρ(N) = (M − C) / 2M</text>'
    b+=f'<text x="{x0}" y="{h-18}" class="s" font-size="12">N = 100: {len(pairs)} pairs, ρ = {rho:.2f}. ρ &lt; ½ exactly when a pair exists. Finite range; no proof of Goldbach.</text>'
    save('goldbach.svg',card(w,h,b,'Goldbach prime pairs of 100 drawn as mirror arcs about the centre 50'))

# ---------- kesten ----------
def kesten():
    w,h=600,400; x0,x1,y0,y1=40,560,300,110
    rnd=random.Random(27); mu=-0.3094; X=0; pts=[]; n=192; vals=[]
    for i in range(n):
        Mi=math.exp(mu+0.75*rnd.gauss(0,1)); X=Mi*X+1; vals.append(X)
    top=max(math.log1p(v) for v in vals)
    pts=[(x0+(x1-x0)*i/(n-1), y0+(y1-y0)*math.log1p(v)/top) for i,v in enumerate(vals)]
    # moment root for the geometric comparison with a=7
    b=head('COLLATZ × KESTEN–GOLDIE · REPORTED','Small steps. Rare bursts.',size=26)
    b+=f'<path d="M{x0} {y0}H{x1}" stroke="{MUTED}" opacity=".7"/>'
    b+=f'<path d="{path(pts)}" fill="none" stroke="{MINT}" stroke-width="2" stroke-linejoin="round" pathLength="1" class="draw"/>'
    i=max(range(n),key=lambda j:vals[j]); 
    b+=f'<circle cx="{pts[i][0]:.1f}" cy="{pts[i][1]:.1f}" r="6" fill="{CORAL}" class="pulse"/><text x="{pts[i][0]+12:.1f}" y="{pts[i][1]+4:.1f}" class="m c" font-size="12">burst</text>'
    b+=f'<text x="{x0}" y="{y0+20}" class="m" font-size="12">X → M·X + 1, 192 updates (seeded teaching model, not a Collatz orbit)</text>'
    bx=x0
    for lab,val,col in (('moment root',0.3429,GOLD),('sample moments',0.3447,MINT),('tail fit',0.3417,TEAL)):
        b+=f'<rect x="{bx}" y="{h-58}" width="160" height="42" rx="8" fill="{PANEL}" stroke="{LINE}"/><text x="{bx+12}" y="{h-41}" class="s" font-size="11">{lab}</text><text x="{bx+12}" y="{h-23}" font-family="{MONO}" font-size="15" fill="{col}">κ = {val}</text>'
        bx+=176
    save('kesten.svg',card(w,h,b,'Kesten-Goldie mechanism: an affine recursion with rare bursts, and three tail-exponent estimates'))

# ---------- recaman ----------
def recaman():
    w,h=600,400; x0,x1,ym=40,560,225; n=66
    a=[0]; seen={0}
    for k in range(1,n):
        c=a[-1]-k
        if c>0 and c not in seen: a.append(c)
        else: a.append(a[-1]+k)
        seen.add(a[-1])
    mx=max(a); X=lambda v:x0+(x1-x0)*v/mx
    d=f'M{X(0):.1f} {ym}'
    for k in range(1,n):
        r=abs(X(a[k])-X(a[k-1]))/2; fwd=a[k]>a[k-1]; sweep=1 if (k%2==1)==fwd else 0
        d+=f'A{r:.1f} {r*0.62:.1f} 0 0 {sweep} {X(a[k]):.1f} {ym}'
    holes=[v for v in range(1,mx) if v not in seen]
    facts.update(rec_n=n,rec_max=mx,rec_holes=len(holes),rec_minhole=holes[0])
    b=head('RECAMÁN · FINITE COMPUTATION','Around the gaps',size=26)
    b+=f'<path d="{d}" fill="none" stroke="{MINT}" stroke-width="1.6" pathLength="1" class="draw"/>'
    b+=f'<path d="M{x0} {ym}H{x1}" stroke="{MUTED}" opacity=".5"/>'
    for v in holes: b+=f'<circle cx="{X(v):.1f}" cy="{ym}" r="1.8" fill="{CORAL}"/>'
    b+=f'<text x="{x0}" y="{h-40}" font-family="{MONO}" font-size="14" fill="{ON}">aₙ = aₙ₋₁ − n if positive and new, else aₙ₋₁ + n</text>'
    b+=f'<text x="{x0}" y="{h-18}" class="s" font-size="12">First {n} terms reach {mx}; <tspan fill="{CORAL}">{len(holes)} integers below the maximum are still unvisited</tspan> (smallest: {holes[0]}).</text>'
    save('recaman.svg',card(w,h,b,'Recaman sequence arcs with the unvisited integers marked'))

# ---------- beta disk ----------
def beta():
    w,h=600,400; cx,cy,R=165,222,120
    G=sum((-1)**k/(2*k+1)**2 for k in range(2000000)); facts.update(G=G)
    b=head('COMPLEX · EXACT COORDINATE CHANGE','Catalan’s constant at the centre',size=26)
    b+=f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{PANEL}" stroke="{GOLD}" stroke-width="2.5" pathLength="1" class="draw"/>'
    for i,sg in enumerate((1,2,4,10)):
        wl=(sg-2)/(sg+1); c0=(1+wl)/2; rr=(1-wl)/2
        b+=f'<circle cx="{cx+R*c0:.1f}" cy="{cy}" r="{R*rr:.1f}" fill="none" stroke="{MINT}" stroke-width="1.3" opacity="{0.9-0.15*i}" class="pop" style="animation-delay:{1.5+i*0.7}s"/>'
    b+=f'<circle cx="{cx}" cy="{cy}" r="6" fill="{GOLD}" class="pulse"/><text x="{cx-12}" y="{cy-14}" class="m g" font-size="13" text-anchor="end">w = 0</text>'
    b+=f'<circle cx="{cx+R}" cy="{cy}" r="4" fill="{ON}"/><text x="{cx+R+8}" y="{cy+24}" class="m" font-size="12">s = ∞</text>'
    b+=f'<g><circle cx="{cx-R}" cy="{cy}" r="5.5" fill="{CORAL}"/><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="14s" repeatCount="indefinite"/></g>'
    tx=350; y=130
    for t,col,fs in (('w = (s − 2)/(s + 1)',ON,14),('F(w) = β((2 + w)/(1 − w))',ON,14),('',ON,6),(f'F(0) = β(2) = G',GOLD,15),(f'≈ {G:.10f}',GOLD,14),('',ON,6),('|w| = 1  ⇔  Re s = 1/2',CORAL,15),('the boundary is the',MUTED,13),('critical line of β',MUTED,13),('',ON,6),('inner circles: Re s = 1, 2, 4, 10',MINT,12)):
        if t: b+=f'<text x="{tx}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{col}">{t}</text>'
        y+=fs+10 if t else 8
    b+=f'<text x="32" y="{h-16}" class="s" font-size="12">A coordinate change, not a zero-location result. Open: which operator lives on this disk.</text>'
    save('beta-disk.svg',card(w,h,b,'Mobius disk for the Dirichlet beta function with Catalan constant at the centre'))

# ---------- prime layers ----------
def layers():
    w,h=600,400; Om=lambertw(1.0); p,q=5,7
    T=lambda P,x:Om*P**(Om-x); F=lambda a,bb,x:T(bb,T(a,x))
    D=lambda u:0.5*(F(p,q,Om+u)-F(q,p,Om+u)); coef=(Om**2/4)*math.log(p)*math.log(q)*math.log(q/p)
    est=D(1e-3)/1e-6; facts.update(Omega=Om,coef=coef,coef_num=est)
    assert abs(est-coef)/coef<5e-3, (est,coef)
    x0,x1,y0=50,550,300; U=0.35; top=max(abs(D(U)),abs(D(-U)),coef*U*U)
    X=lambda u:x0+(x1-x0)*(u+U)/(2*U); Y=lambda d:y0-170*d/top
    ex=[(X(u),Y(D(u))) for u in [ -U+2*U*i/200 for i in range(201)]]
    qd=[(X(u),Y(coef*u*u)) for u in [ -U+2*U*i/200 for i in range(201)]]
    b=head('TOWERS × PRIMES · EXACT RESULT','Order of the layers, second harmonic',size=26)
    b+=f'<path d="M{x0} {y0}H{x1}M{X(0)} {y0+6}V{y0-180}" stroke="{MUTED}" opacity=".6"/>'
    b+=f'<path d="{path(qd)}" fill="none" stroke="{GOLD}" stroke-width="6" opacity=".35"/>'
    b+=f'<path d="{path(ex)}" fill="none" stroke="{MINT}" stroke-width="2.4" pathLength="1" class="draw"/>'
    b+=f'<text x="{X(0)}" y="{y0+22}" class="m" font-size="12" text-anchor="middle">u = 0 (shared fixed point Ω = W(1))</text>'
    b+=f'<text x="{X(0)+14}" y="{y0-170}" class="m" font-size="12" style="fill:{MINT}">— exact ½(F₅₇ − F₇₅)</text><text x="{X(0)+14}" y="{y0-152}" class="m g" font-size="12">— quadratic term only</text>'
    b+=f'<text x="{x0-10}" y="{h-40}" font-family="{MONO}" font-size="13" fill="{ON}">½(F_pq − F_qp)(Ω+u) = (Ω²/4)·ln p·ln q·ln(q/p)·u² + O(u³)</text>'
    b+=f'<text x="{x0-10}" y="{h-18}" class="s" font-size="12">Swapping two layers keeps the slope and changes the curvature. p = 5, q = 7: ≈ {coef:.4f}·u².</text>'
    save('prime-layers.svg',card(w,h,b,'Swapping two prime-indexed layers changes the quadratic response'))

# ---------- hero ----------
def hero():
    w,h=1200,420
    n=27; orb=[n]
    while n!=1: n=n//2 if n%2==0 else 3*n+1; orb.append(n)
    facts.update(c27_steps=len(orb)-1,c27_peak=max(orb))
    pts=[(56+740*i/(len(orb)-1), 386-58*math.log(v)/math.log(max(orb))) for i,v in enumerate(orb)]
    b=f'<path id="orb" d="{path(pts)}" fill="none" stroke="{TEAL}" stroke-width="1.8" opacity=".9" pathLength="1" class="draw"/>'
    b+=f'<circle r="5" fill="{GOLD}"><animateMotion dur="14s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.25;1" calcMode="linear"><mpath href="#orb"/></animateMotion></circle>'
    cx,cy,R=985,205,150; dots=''
    for k in range(210):
        a=2*math.pi*k/210; co=math.gcd(k,210)==1
        dots+=f'<circle cx="{cx+R*math.sin(a):.1f}" cy="{cy-R*math.cos(a):.1f}" r="{4.2 if co else 1.5}" fill="{MINT if co else LINE}"/>'
    spokes=''.join(f'<path d="M{cx} {cy}L{cx+R*math.sin(2*math.pi*k/210):.1f} {cy-R*math.cos(2*math.pi*k/210):.1f}" stroke="{MINT}" stroke-width=".6" opacity=".25"/>' for k in range(210) if math.gcd(k,210)==1)
    b+=f'<g class="spin">{spokes}{dots}</g>'
    b+=f'<circle cx="{cx}" cy="{cy}" r="74" fill="{DEEP}" stroke="{LINE}"/><text x="{cx}" y="{cy-6}" font-family="{SERIF}" font-size="40" fill="{ON}" text-anchor="middle">48</text><text x="{cx}" y="{cy+18}" class="m" font-size="12" text-anchor="middle">lanes mod 210</text>'
    b+=f'<text x="56" y="86" class="k" font-size="15">RESEARCH ATLAS · EXPERIMENTAL NUMBER THEORY</text>'
    b+=f'<text x="52" y="176" font-family="{SERIF}" font-size="92" fill="{ON}" letter-spacing="-2">Encapsulator<tspan fill="{GOLD}">P</tspan></text>'
    b+=f'<text x="56" y="226" font-family="{SERIF}" font-size="30" font-style="italic" fill="{MINT}">Follow the spark. Open the mathematics.</text>'
    bx=56
    for big,small in (('46','atlas entries'),('28','exact results'),('5','families'),('6','evidence labels')):
        ww=44+len(small)*8.2+len(big)*17
        b+=f'<rect x="{bx}" y="262" width="{ww:.0f}" height="46" rx="23" fill="{PANEL}" stroke="{LINE}"/><text x="{bx+20}" y="292" font-family="{SERIF}" font-size="24" fill="{GOLD}">{big}</text><text x="{bx+28+len(big)*15}" y="291" class="s" font-size="14" fill="{ON}">{small}</text>'
        bx+=ww+12
    b+=f'<text x="56" y="406" class="m" font-size="12">trace: the Collatz orbit of 27, {len(orb)-1} steps, peak {max(orb)} (log scale)</text>'
    save('hero.svg',card(w,h,b,'EncapsulatorP research atlas: follow the spark, open the mathematics'))

towers(); logistic(); goldbach(); kesten(); recaman(); beta(); layers(); hero()
for k,v in facts.items(): print(k,v)
