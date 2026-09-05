# -*- coding: utf-8 -*-
"""
Esame di Disegno Tecnico Industriale per Gestionali - Febbraio 2023 (Prof. D. Russo)
Ricostruzione didattica della tavola d'esame:
  - Vista da destra
  - Sezione A-A
  - Rugosita' generale Ra 2, superficie B Ra 1.5
  - Foro laterale Ø10  Es=+0.009 / Ei=+0.005  (Ø10 +0.009/+0.005)
  - Foro centrale filettato metrico ISO (esempio: M20)
  - Assi di simmetria sistemati, quote ridondanti eliminate

NOTA: le quote numeriche del pezzo sono un esempio coerente (lo screenshot
originale non e' leggibile); sostituire con le quote reali della tavola.
Proiezione: 1° diedro (ISO-E, europea).
"""
import numpy as np
import matplotlib
matplotlib.use("PDF")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, PathPatch, Arc
from matplotlib.path import Path
from matplotlib.lines import Line2D

# ---- stili linea (ISO) ----
LW_THICK = 1.6      # contorni visibili
LW_THIN  = 0.5      # quote, tratteggio sezione, filetto (minore/maggiore)
LW_HID   = 0.8      # linee nascoste
LW_CEN   = 0.6      # assi

def cl():  return dict(color="k")

fig = plt.figure(figsize=(11.69, 8.27))              # A4 orizzontale
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 297); ax.set_ylim(0, 210)
ax.set_aspect("equal"); ax.axis("off")

# ---------- cornice e squadratura ----------
ax.add_patch(Rectangle((5,5), 287, 200, fill=False, lw=1.2))
ax.add_patch(Rectangle((10,10), 277, 190, fill=False, lw=0.8))

def visible(pts, close=False):
    p = np.array(pts, float)
    if close: p = np.vstack([p, p[0]])
    ax.plot(p[:,0], p[:,1], "-", lw=LW_THICK, color="k", solid_capstyle="round")

def hidden(x0,y0,x1,y1):
    ax.plot([x0,x1],[y0,y1], "--", lw=LW_HID, color="k", dashes=(4,2))

def center_h(y, x0, x1):
    ax.plot([x0,x1],[y,y], "-.", lw=LW_CEN, color="k", dashes=(8,2,1,2))
def center_v(x, y0, y1):
    ax.plot([x,x],[y0,y1], "-.", lw=LW_CEN, color="k", dashes=(8,2,1,2))

def circle(cx,cy,d,lw=LW_THICK,ls="-",dashes=None,frac=1.0,start=90):
    r=d/2; a=np.linspace(np.radians(start), np.radians(start+360*frac),200)
    kw=dict(lw=lw,color="k")
    if dashes: kw["dashes"]=dashes; kw["linestyle"]="--"
    else: kw["linestyle"]=ls
    ax.plot(cx+r*np.cos(a), cy+r*np.sin(a), **kw)

def hatch_rect(x0,x1,y0,y1, step=2.2):
    """tratteggio 45° dentro un rettangolo"""
    xs=[];
    d=(x1-x0)+(y1-y0)
    c=x0-(y1-y0)
    while c< x1+ (y1-y0):
        # linea y=x-c ; clip a rettangolo
        p0=None;p1=None
        pts=[]
        # intersezioni
        for (xx) in [x0,x1]:
            yy=xx-c
            if y0-1e-9<=yy<=y1+1e-9: pts.append((xx,yy))
        for (yy) in [y0,y1]:
            xx=yy+c
            if x0-1e-9<=xx<=x1+1e-9: pts.append((xx,yy))
        if len(pts)>=2:
            pts=sorted(pts)
            ax.plot([pts[0][0],pts[-1][0]],[pts[0][1],pts[-1][1]],"-",lw=LW_THIN,color="k")
        c+=step

# ---------- dimensioni ----------
def dim_h(x0,x1,y,text,off=0,tick=1.4):
    ax.annotate("",(x1,y),(x0,y),arrowprops=dict(arrowstyle="<->",lw=LW_THIN,color="k",shrinkA=0,shrinkB=0))
    ax.text((x0+x1)/2, y+1.0, text, ha="center", va="bottom", fontsize=6.5)
def dim_v(y0,y1,x,text):
    ax.annotate("",(x,y1),(x,y0),arrowprops=dict(arrowstyle="<->",lw=LW_THIN,color="k",shrinkA=0,shrinkB=0))
    ax.text(x-1.0,(y0+y1)/2, text, ha="right", va="center", rotation=90, fontsize=6.5)

def ext(x,y0,y1):  ax.plot([x,x],[y0,y1],"-",lw=LW_THIN,color="k")
def exty(y,x0,x1): ax.plot([x0,x1],[y,y],"-",lw=LW_THIN,color="k")

def rough(x,y,val,rot=0):
    """simbolo di rugosita' (triangolo aperto) con valore Ra"""
    s=2.2
    p=[(0,0),(-s*0.6,s*1.1),(-s*1.7,-s*1.1)]  # approx
    # tick semplice a V
    ax.plot([x, x-1.5, x-3.0],[y, y+3.0, y-1.0],"-",lw=0.8,color="k")
    ax.text(x-3.4,y+1.6,val,ha="right",va="bottom",fontsize=6.5)

# ===================================================================
#  Geometria pezzo (mm):
#  flangia Ø60 x sp.10 ; mozzo Ø36 x h12 ; foro centrale filettato M20
#  orecchia a sinistra con foro Ø10 (centro a X=-42), sp.10
#  Superficie B = faccia superiore del mozzo
# ===================================================================
D_FL=60; SP_FL=10; D_BO=36; H_BO=12; D_MAJ=20; D_MIN=17.3
LUG_X=-42; LUG_W=22; D_LUG=10

# --------- VISTA FRONTALE (asse verticale) centro pagina in cx_f ---------
cx_f=150; base_f=95   # Z=0 -> y=base_f
def FX(x): return cx_f+x
def FZ(z): return base_f+z
# contorno flangia + mozzo + orecchia (meta' dx e sx)
visible([(FX(-30),FZ(0)),(FX(30),FZ(0)),(FX(30),FZ(SP_FL)),(FX(18),FZ(SP_FL)),
         (FX(18),FZ(SP_FL+H_BO)),(FX(-18),FZ(SP_FL+H_BO)),(FX(-18),FZ(SP_FL)),
         (FX(-30),FZ(SP_FL)),(FX(-30),FZ(0))])
# orecchia
visible([(FX(-30),FZ(0)),(FX(LUG_X-LUG_W/2),FZ(0)),(FX(LUG_X-LUG_W/2),FZ(SP_FL)),(FX(-30),FZ(SP_FL))])
# foro filettato centrale (nascosto in vista frontale): minore + maggiore
hidden(FX(-D_MIN/2),FZ(0),FX(-D_MIN/2),FZ(SP_FL+H_BO))
hidden(FX( D_MIN/2),FZ(0),FX( D_MIN/2),FZ(SP_FL+H_BO))
hidden(FX(-D_MAJ/2),FZ(0),FX(-D_MAJ/2),FZ(SP_FL+H_BO))
hidden(FX( D_MAJ/2),FZ(0),FX( D_MAJ/2),FZ(SP_FL+H_BO))
# foro Ø10 orecchia (nascosto)
hidden(FX(LUG_X-D_LUG/2),FZ(0),FX(LUG_X-D_LUG/2),FZ(SP_FL))
hidden(FX(LUG_X+D_LUG/2),FZ(0),FX(LUG_X+D_LUG/2),FZ(SP_FL))
# assi
center_v(FX(0),FZ(-6),FZ(SP_FL+H_BO+8))
center_v(FX(LUG_X),FZ(-6),FZ(SP_FL+6))
ax.text(cx_f,FZ(SP_FL+H_BO)+11,"VISTA FRONTALE",ha="center",fontsize=7,weight="bold")
# superficie B (faccia sup. mozzo) + rugosita'
ax.annotate("B",(FX(18),FZ(SP_FL+H_BO)),(FX(30),FZ(SP_FL+H_BO)+6),fontsize=7,
            weight="bold",arrowprops=dict(arrowstyle="-",lw=0.6))
rough(FX(30)+2, FZ(SP_FL+H_BO)+8, "Ra 1.5")
# quote frontale
ext(FX(-30),FZ(0),FZ(-9)); ext(FX(30),FZ(0),FZ(-9))
dim_h(FX(-30),FX(30),FZ(-7),"Ø60")
ext(FX(-18),FZ(SP_FL+H_BO),FZ(SP_FL+H_BO+9)); ext(FX(18),FZ(SP_FL+H_BO),FZ(SP_FL+H_BO+9))
dim_h(FX(-18),FX(18),FZ(SP_FL+H_BO+7),"Ø36")
exty(FZ(0),FX(30),FX(46)); exty(FZ(SP_FL),FX(30),FX(46)); exty(FZ(SP_FL+H_BO),FX(30),FX(46))
dim_v(FZ(0),FZ(SP_FL),FX(44),"10")
dim_v(FZ(0),FZ(SP_FL+H_BO),FX(52),"22")

# --------- VISTA DA DESTRA (1° diedro -> a SINISTRA della frontale) ---------
cx_r=70;
def RX(depth): return cx_r+depth      # profondita' Y
def RZ(z): return base_f+z
# profilo: flangia (prof 60) + mozzo (prof 36)
visible([(RX(-30),RZ(0)),(RX(30),RZ(0)),(RX(30),RZ(SP_FL)),(RX(18),RZ(SP_FL)),
         (RX(18),RZ(SP_FL+H_BO)),(RX(-18),RZ(SP_FL+H_BO)),(RX(-18),RZ(SP_FL)),
         (RX(-30),RZ(SP_FL)),(RX(-30),RZ(0))])
# orecchia (dietro, a sinistra in X -> nascosta): appare come linee nascoste del foro
hidden(RX(-D_LUG/2),RZ(0),RX(-D_LUG/2),RZ(SP_FL))
hidden(RX( D_LUG/2),RZ(0),RX( D_LUG/2),RZ(SP_FL))
# foro filettato (nascosto)
hidden(RX(-D_MIN/2),RZ(0),RX(-D_MIN/2),RZ(SP_FL+H_BO))
hidden(RX( D_MIN/2),RZ(0),RX( D_MIN/2),RZ(SP_FL+H_BO))
center_v(RX(0),RZ(-6),RZ(SP_FL+H_BO+8))
center_h(RZ(SP_FL+H_BO/2+SP_FL/2),RX(-34),RX(34))
ax.text(cx_r,RZ(SP_FL+H_BO)+11,"VISTA DA DESTRA",ha="center",fontsize=7,weight="bold")

# --------- VISTA DALL'ALTO (pianta) sotto la frontale ---------
cx_t=150; cy_t=53
circle(cx_t,cy_t,D_FL)                     # flangia
circle(cx_t,cy_t,D_BO)                     # mozzo
circle(cx_t,cy_t,D_MIN)                    # foro (minore, spesso)
circle(cx_t,cy_t,D_MAJ,lw=LW_THIN,frac=0.75,start=100)   # filetto maggiore, sottile 3/4
# orecchia
visible([(cx_t-30,cy_t+LUG_W/2),(cx_t+LUG_X+LUG_W/2,cy_t+LUG_W/2)])
# raccordo orecchia-flangia (semplificato) + foro Ø10
lx=cx_t+LUG_X
ax.plot([cx_t-30,lx-LUG_W/2],[cy_t-LUG_W/2,cy_t-LUG_W/2],"-",lw=LW_THICK,color="k")
ax.plot([cx_t-30,lx-LUG_W/2],[cy_t+LUG_W/2,cy_t+LUG_W/2],"-",lw=LW_THICK,color="k")
ax.plot([lx-LUG_W/2,lx-LUG_W/2],[cy_t-LUG_W/2,cy_t+LUG_W/2],"-",lw=LW_THICK,color="k")
circle(lx,cy_t,D_LUG)
center_h(cy_t,cx_t-40, cx_t+34)            # asse orizzontale
center_v(cx_t,cy_t-38,cy_t+38)             # asse verticale
center_v(lx,cy_t-10,cy_t+10)
ax.text(cx_t-72,cy_t-30,"VISTA DALL'ALTO",ha="left",fontsize=7,weight="bold")
# linea di sezione A-A (verticale) con frecce
ya0=cy_t-32; ya1=cy_t+28
ax.plot([cx_t,cx_t],[ya0,ya1],"-.",lw=1.0,color="k",dashes=(10,3,2,3))
ax.annotate("",(cx_t,ya1+6),(cx_t,ya1),arrowprops=dict(arrowstyle="-|>",lw=1.2,color="k"))
ax.annotate("",(cx_t,ya0-6),(cx_t,ya0),arrowprops=dict(arrowstyle="-|>",lw=1.2,color="k"))
ax.text(cx_t+3,ya1+5,"A",fontsize=8,weight="bold")
ax.text(cx_t+3,ya0-9,"A",fontsize=8,weight="bold")
# quotatura foro Ø10 con tolleranza
ax.annotate("",(lx,cy_t),(lx-22,cy_t+22),arrowprops=dict(arrowstyle="-",lw=0.6))
ax.text(lx-23,cy_t+23,"Ø10  $^{+0.009}_{+0.005}$",ha="right",va="bottom",fontsize=7)
# interasse orecchia
ext(cx_t,cy_t+LUG_W/2,cy_t+LUG_W/2+9); ext(lx,cy_t+10,cy_t+LUG_W/2+9)
dim_h(lx,cx_t,cy_t+LUG_W/2+7,"42")

# --------- SEZIONE A-A (piano X=0, vista Y-Z) a destra ---------
cx_s=240; base_s=95
def SX(y): return cx_s+y
def SZ(z): return base_s+z
# contorno esterno (flangia+mozzo) come frontale ma pieno/tratteggiato
outline=[(SX(-30),SZ(0)),(SX(30),SZ(0)),(SX(30),SZ(SP_FL)),(SX(18),SZ(SP_FL)),
         (SX(18),SZ(SP_FL+H_BO)),(SX(D_MAJ/2),SZ(SP_FL+H_BO)),
         (SX(D_MAJ/2),SZ(0)),(SX(-D_MAJ/2),SZ(0)),(SX(-D_MAJ/2),SZ(SP_FL+H_BO)),
         (SX(-18),SZ(SP_FL+H_BO)),(SX(-18),SZ(SP_FL)),(SX(-30),SZ(SP_FL)),(SX(-30),SZ(0))]
visible(outline)
# tratteggio (due zone: sinistra e destra del foro)
hatch_rect(SX(D_MAJ/2),SX(30),SZ(0),SZ(SP_FL))
hatch_rect(SX(D_MAJ/2),SX(18),SZ(SP_FL),SZ(SP_FL+H_BO))
hatch_rect(SX(-30),SX(-D_MAJ/2),SZ(0),SZ(SP_FL))
hatch_rect(SX(-18),SX(-D_MAJ/2),SZ(SP_FL),SZ(SP_FL+H_BO))
# filetto interno in sezione: minore = linea spessa (gia' Ø_MAJ apertura=foro),
# rappresentiamo cresta (minore) sottile piu' interna e fondo (maggiore) spesso esterno
ax.plot([SX(-D_MIN/2),SX(-D_MIN/2)],[SZ(0),SZ(SP_FL+H_BO)],"-",lw=LW_THIN,color="k")
ax.plot([SX( D_MIN/2),SX( D_MIN/2)],[SZ(0),SZ(SP_FL+H_BO)],"-",lw=LW_THIN,color="k")
center_v(SX(0),SZ(-6),SZ(SP_FL+H_BO+8))
ax.text(cx_s,SZ(SP_FL+H_BO)+11,"SEZIONE  A-A",ha="center",fontsize=7,weight="bold")
# quote sezione
ext(SX(-30),SZ(0),SZ(-9)); ext(SX(30),SZ(0),SZ(-9))
dim_h(SX(-30),SX(30),SZ(-7),"Ø60")
# quota filettatura
ax.annotate("",(SX(D_MAJ/2),SZ(SP_FL+H_BO)),(SX(D_MAJ/2)+18,SZ(SP_FL+H_BO)+8),
            arrowprops=dict(arrowstyle="-",lw=0.6))
ax.text(SX(D_MAJ/2)+19,SZ(SP_FL+H_BO)+8,"M20",ha="left",va="bottom",fontsize=7)

# --------- indicazione rugosita' generale (in alto a dx) ---------
gx,gy=232,150
ax.plot([gx,gx-1.5,gx-3.0],[gy,gy+3.0,gy-1.0],"-",lw=0.8,color="k")
ax.text(gx-3.4,gy+1.4,"Ra 2",ha="right",va="bottom",fontsize=7)
ax.text(gx+2,gy+0.5,"(   )",fontsize=8,va="bottom")   # rugosita' generale + varie
ax.text(gx-14,gy+9,"Rugosità generale",ha="left",fontsize=6.5,style="italic")

# ---------- CARTIGLIO ----------
bx0,by0,bx1,by1=180,12,287,42
ax.add_patch(Rectangle((bx0,by0),bx1-bx0,by1-by0,fill=False,lw=1.0))
ax.plot([bx0,bx1],[by0+15,by0+15],"-",lw=0.6,color="k")
ax.plot([bx0+62,bx0+62],[by0,by0+15],"-",lw=0.6,color="k")
ax.text((bx0+bx1)/2,by1-4,"Esame di Disegno Tecnico Industriale per Gestionali",
        ha="center",fontsize=7,weight="bold")
ax.text((bx0+bx1)/2,by1-9,"Febbraio 2023  –  Prof. Davide Russo",ha="center",fontsize=6.5)
ax.text(bx0+31,by0+7,"Scala 1:1\nQuote in mm\n1° diedro (ISO-E)",ha="center",va="center",fontsize=6)
ax.text(bx0+62+22,by0+10,"Materiale: Acciaio\nSmussi 1x45°",ha="center",va="center",fontsize=6)

# ---------- note correzioni ----------
notes=("CORREZIONI APPLICATE:\n"
       "• Aggiunte Vista da destra e Sezione A-A\n"
       "• Assi di simmetria sistemati (linea mista fine)\n"
       "• Quote ridondanti eliminate, quote errate corrette\n"
       "• Rugosità generale Ra 2 ; superficie B Ra 1.5\n"
       "• Foro Ø10  Es=+0.009 / Ei=+0.005  ->  Ø10 +0.009/+0.005\n"
       "• Foro centrale filettato: filettatura metrica ISO (es. M20)")
ax.text(16,178,notes,ha="left",va="top",fontsize=6.4,
        bbox=dict(boxstyle="round,pad=0.4",fc="#f5f5f5",ec="0.5",lw=0.6))

fig.savefig("Esame_Disegno_Tecnico_Feb2023.pdf")
fig.savefig("Esame_Disegno_Tecnico_Feb2023_draft.jpg", dpi=200, pil_kwargs={"quality":92})
print("Creati: PDF + JPG (draft / messa in tavola)")
