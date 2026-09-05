# -*- coding: utf-8 -*-
"""
Soluzioni - Meccanica Teorica e Applicata - Appello 17/06/2025
Universita' degli Studi di Bergamo - Ing. Gestionale
PDF multi-pagina con svolgimento e disegni (FBD, diagrammi azioni interne,
curva caratteristica, schema meccanismo).
"""
import numpy as np
import matplotlib
matplotlib.use("PDF")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle

plt.rcParams.update({"font.size":10, "mathtext.fontset":"cm"})

BLUE="#16507b"; GREY="#444"; RED="#b02418"; GREEN="#1a6b3c"

def new_page():
    fig=plt.figure(figsize=(8.27,11.69))
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    return fig,ax

def T(ax,x,y,s,size=10,w="normal",c="k",ha="left"):
    ax.text(x,y,s,fontsize=size,weight=w,color=c,ha=ha,va="top")

def box(ax,x,y,s,size=11,c=BLUE,pad=0.35):
    ax.text(x,y,s,fontsize=size,weight="bold",color=c,va="top",ha="left",
            bbox=dict(boxstyle=f"round,pad={pad}",fc="#eef4fa",ec=c,lw=1.1))

def head(ax):
    ax.add_patch(Rectangle((0.05,0.945),0.90,0.045,fc=BLUE,ec="none",transform=ax.transAxes))
    T(ax,0.07,0.984,"Meccanica Teorica e Applicata  —  Appello 17/06/2025",12,"bold","white")
    T(ax,0.07,0.966,"Universita' degli Studi di Bergamo · Corso di Laurea in Ing. Gestionale · Svolgimento",8.5,"normal","white")

pdf=PdfPages("Soluzioni_Meccanica_17-06-2025.pdf")

# =====================================================================
# PAGINA 1 — ESERCIZIO 1 (accelerazione + verifica slittamento)
# =====================================================================
fig,ax=new_page(); head(ax)
T(ax,0.07,0.925,"ESERCIZIO 1  —  Sistema puleggia/cinghia + aste AD-DB e DC",12,"bold",BLUE)
T(ax,0.07,0.905,
 "Ipotesi di lettura schema: AB verticale trasla in verticale (B = pattino/guida verticale;\n"
 "fune in A verticale, allineata ad AB). DC (massa m) saldata in D, orizzontale; carico m$_1$ in C.\n"
 "Le due pulegge (J, R) muovono la cinghia orizzontale su cui appoggia m$_c$ (moto orizzontale).",9)

# --- schizzo FBD ---
axd=fig.add_axes([0.62,0.62,0.34,0.235]); axd.set_xlim(-1,4); axd.set_ylim(-0.5,4.2); axd.axis("off")
# pulegge + cinghia
for cx in (0.6,2.6):
    axd.add_patch(Circle((cx,3.5),0.32,fill=False,lw=1.3))
axd.plot([0.6,2.6],[3.82,3.82],'k',lw=1.2); axd.plot([0.6,2.6],[3.18,3.18],'k',lw=1.2)
axd.add_patch(Rectangle((1.3,3.82),0.7,0.35,fc="#cfe0ef",ec="k")); axd.text(1.65,4.0,"m$_c$",ha="center",fontsize=8)
axd.text(0.6,2.9,"J,R",ha="center",fontsize=7); axd.text(2.6,2.9,"J,R",ha="center",fontsize=7)
# fune A -> puleggia sx
axd.plot([0.6,0.6],[3.18,2.2],'k',lw=1.0)
axd.annotate("T",(0.6,2.6),(0.15,2.6),fontsize=9,va="center")
# asta AB verticale
axd.plot([0.6,0.6],[2.2,0.0],'k',lw=2.2)
axd.text(0.72,2.15,"A",fontsize=8); axd.text(0.72,1.15,"D",fontsize=8); axd.text(0.72,0.05,"B",fontsize=8)
# DC orizzontale in D (a meta')
axd.plot([0.6,2.0],[1.1,1.1],'k',lw=2.2)
axd.text(2.05,1.15,"C",fontsize=8); axd.text(1.25,1.28,"m",fontsize=8)
axd.add_patch(Circle((2.0,1.1),0.10,fc="k")); axd.text(2.15,0.95,"m$_1$",fontsize=8)
# pattino B
axd.add_patch(Rectangle((0.35,-0.35),0.5,0.3,fc="none",ec="k",hatch="////"))
axd.annotate("",(0.6,-0.6),(0.6,0.0),arrowprops=dict(arrowstyle="->",color=RED))
axd.text(0.75,-0.5,"a",color=RED,fontsize=9)
axd.set_title("Schema / FBD",fontsize=8)

T(ax,0.07,0.845,"1) Accelerazione di AB  (bilancio di potenze, 1 g.d.l.)",10.5,"bold",GREY)
T(ax,0.07,0.828,
 "Velocita' cinghia = velocita' fune = velocita' di A  ⇒  m$_c$ ha accel. orizzontale = a ;\n"
 "pulegge:  ω = v/R ,  α = a/R.  Il peso di m$_c$ non lavora (moto orizzontale).",9)
T(ax,0.09,0.795,"Potenza pesi = Potenza forze d'inerzia:",9.5)
ax.text(0.11,0.775,r"$(m+m_1)\,g\,v=\left[\,m+m_1+m_c+\dfrac{2J}{R^2}\,\right]a\,v$",fontsize=12,va="top")
box(ax,0.09,0.735,r"$a=\dfrac{(m+m_1)\,g}{\,m+m_1+m_c+2J/R^{2}\,}$",12)
T(ax,0.09,0.665,"Con  m$_1$ = m$_p$ = m ,  m$_c$ = 2m :",9.5)
box(ax,0.11,0.645,r"$a=\dfrac{2mg}{\,4m+2J/R^{2}\,}=\dfrac{mg}{\,2m+J/R^{2}\,}$",12,GREEN)

T(ax,0.07,0.560,"2) Verifica di non slittamento di m$_c$  (f$_s$ = 1)",10.5,"bold",GREY)
T(ax,0.07,0.543,
 "Forza d'attrito necessaria per accelerare m$_c$:  F = m$_c$·a ;  attrito max = f$_s$·N = f$_s$·m$_c$·g.\n"
 "Condizione:  m$_c$·a ≤ f$_s$·m$_c$·g  ⇒  a ≤ f$_s$·g = g.",9)
ax.text(0.09,0.495,r"$a=\dfrac{mg}{2m+J/R^{2}}=\dfrac{g}{\,2+J/(mR^{2})\,}\;\leq\;\dfrac{g}{2}\;<\;g=f_s\,g$",fontsize=11.5,va="top")
box(ax,0.09,0.445,"Poiche' a ≤ g/2 < g  →  m$_c$ NON slitta.  ✓  (verificato per qualsiasi J)",10.5,GREEN)

T(ax,0.07,0.360,"Note di metodo",10,"bold",GREY)
T(ax,0.07,0.343,
 "• Il termine 2J/R² è l'inerzia delle due pulegge ridotta al moto lineare della cinghia/fune.\n"
 "• Il carico m$_c$ compare nell'inerzia (viene trascinato) ma non nei pesi motori (moto orizz.).\n"
 "• I pesi motori del sistema sono quelli di DC (m) e di m$_1$, che fanno scendere AB.",9)
pdf.savefig(fig); plt.close(fig)

# =====================================================================
# PAGINA 2 — ESERCIZIO 1: reazioni + diagrammi azioni interne
# =====================================================================
fig,ax=new_page(); head(ax)
T(ax,0.07,0.925,"ESERCIZIO 1  —  Reazioni vincolari e azioni interne",12,"bold",BLUE)
T(ax,0.07,0.905,"Posto  g−a = g·(m+J/R²)/(2m+J/R²).  Corpo AB+DC+m$_1$ in traslazione verticale (d'Alembert).",9)

box(ax,0.07,0.865,"Tiro della fune in A:   T = (m+m$_1$)(g−a) = 2m(g−a)",11,BLUE)
box(ax,0.07,0.808,"Reazioni in B (pattino verticale):   H$_B$ = 0 ,   M$_B$ = (3/4)·m·(g−a)·L",11,BLUE)
box(ax,0.07,0.751,"Reazioni in D (incastro AB–DC):   N$_D$ = 2m(g−a) ,  V$_D$ = 0 ,  M$_D$ = (3/4)m(g−a)L",11,BLUE)
T(ax,0.07,0.700,
 "ΣF$_x$=0 ⇒ H$_B$=0 (tutte le forze/inerzie sono verticali).  ΣF$_y$ dà T e N$_D$.\n"
 "ΣM attorno a B (o a D) con carichi a x=L/4 (baric. DC) e x=L/2 (m$_1$) ⇒ M = (3/4)m(g−a)L.\n"
 "AB è priva di massa e scarica trasversalmente: il momento resta costante = M$_B$ = M$_D$.",9)

T(ax,0.07,0.628,"Diagrammi delle azioni interne",10.5,"bold",GREY)
# ---- 4 subplot ----
w=2*(1)  # placeholder
p=lambda l,b: fig.add_axes([l,b,0.38,0.20])
k=2  # unit factor label uses m(g-a)
# DC: taglio
a1=p(0.08,0.36)
x=np.linspace(0,0.5,50); w=2  # w=2m(g-a)/L -> in unita' m(g-a)/L
V=w*(0.5-x)+1.0            # +m1(g-a)=1
a1.plot(x,V,color=BLUE,lw=2); a1.fill_between(x,0,V,color=BLUE,alpha=0.12)
a1.plot([0.5,0.5],[V[-1],0],color=BLUE,lw=2)
a1.set_title("DC — Taglio  T(x)",fontsize=8.5)
a1.set_xlabel("da D (x=0) a C (x=L/2)",fontsize=7)
a1.text(0.0,2.0,"2m(g−a)",fontsize=7,color=BLUE); a1.text(0.42,1.0,"m(g−a)",fontsize=7,color=BLUE)
a1.set_ylim(0,2.4); a1.grid(alpha=0.25)
# DC: momento
a2=p(0.56,0.36)
M=w*(0.5-x)*(0.5-x)/2 + 1.0*(0.5-x)   # in m(g-a)L? scale
a2.plot(x,M,color=RED,lw=2); a2.fill_between(x,0,M,color=RED,alpha=0.12)
a2.set_title("DC — Momento flettente  M(x)",fontsize=8.5)
a2.set_xlabel("da D a C",fontsize=7)
a2.text(0.0,M[0]+0.02,"M$_D$=(3/4)m(g−a)L",fontsize=7,color=RED)
a2.set_ylim(0,0.9); a2.grid(alpha=0.25)
# AB: normale
a3=p(0.08,0.09)
z=np.array([0,1,1,2]); N=np.array([0,0,2,2])  # B=0..D=0 then jump to 2 in D..A (tension)
a3.step([0,1,1,2],[0,0,2,2],where="post",color=GREEN,lw=2)
a3.fill_between([0,1],[0,0],step="post",color=GREEN,alpha=0.1)
a3.fill_between([1,2],[2,2],step="post",color=GREEN,alpha=0.1)
a3.set_title("AB — Sforzo normale  N",fontsize=8.5)
a3.set_xlabel("da B (0) a D (1) ad A (2)  [×L]",fontsize=7)
a3.text(1.05,2.05,"N=2m(g−a) (traz.)",fontsize=7,color=GREEN)
a3.text(0.15,0.15,"N=0",fontsize=7,color=GREEN)
a3.set_ylim(-0.3,2.6); a3.grid(alpha=0.25)
# AB: momento
a4=p(0.56,0.09)
a4.step([0,1,1,2],[0.75,0.75,0,0],where="post",color=RED,lw=2)
a4.fill_between([0,1],[0.75,0.75],step="post",color=RED,alpha=0.12)
a4.set_title("AB — Momento flettente  M",fontsize=8.5)
a4.set_xlabel("da B a D ad A  [×L]",fontsize=7)
a4.text(0.05,0.83,"M=(3/4)m(g−a)L  (tratto B–D)",fontsize=7,color=RED)
a4.text(1.15,0.12,"M=0 (tratto D–A)",fontsize=7,color=RED)
a4.set_ylim(0,1.0); a4.grid(alpha=0.25)
pdf.savefig(fig); plt.close(fig)

# =====================================================================
# PAGINA 3 — ESERCIZIO 2 (nastro trasportatore)
# =====================================================================
fig,ax=new_page(); head(ax)
T(ax,0.07,0.925,"ESERCIZIO 2  —  Nastro trasportatore inclinato (α)",12,"bold",BLUE)
T(ax,0.07,0.905,
 "Dati: motore M$_m$ (J$_m$), trasmissione τ=ω$_p$/ω$_m$, rendimento diretto η e retrogrado η*.\n"
 "Pulegge (J$_p$,R), rulli (J$_r$,r).  Sul ramo superiore 2 casse (m); sul ramo inferiore m/2.\n"
 "Convenzione: forze ridotte alla cinghia; coppie ridotte all'albero motore.",9)

T(ax,0.07,0.845,"1) Coppia a regime (v = cost, a = 0)",10.5,"bold",GREY)
T(ax,0.07,0.828,
 "Forza resistente lungo il nastro (salita): pesi che salgono meno peso che scende sul ramo inf.:",9)
ax.text(0.09,0.800,r"$F_r=2mg\sin\alpha-\dfrac{m}{2}g\sin\alpha=\dfrac{3}{2}mg\sin\alpha$",fontsize=12,va="top")
ax.text(0.09,0.760,r"$C_r=F_r\cdot R=\dfrac{3}{2}mgR\sin\alpha\quad(\text{alla puleggia})$",fontsize=11,va="top")
box(ax,0.09,0.720,r"Salita (motore motore): $\;M_m^{sal}=\dfrac{3}{2}mgR\sin\alpha\cdot\dfrac{\tau}{\eta}$",11.5,GREEN)
T(ax,0.09,0.665,
 "In discesa il carico è trascinante (il peso aiuta il moto): il motore FRENA → rendimento retrogrado η*.",9)
box(ax,0.09,0.635,r"Discesa (carico trascinante): $\;M_m^{disc}=\dfrac{3}{2}mgR\sin\alpha\cdot\tau\,\eta^{*}$  (coppia frenante)",11.5,RED)

# --- curva caratteristica ---
axc=fig.add_axes([0.09,0.30,0.52,0.24])
w=np.linspace(0,1.25,200); ws=1.0
# coppia motore asincrono (in funzione di ω): 0 a ω=0? usiamo forma tipica
C=2.4*((ws-w)/0.18)/(1+((ws-w)/0.18)**2)   # curva a campana attorno a ws
axc.plot(C,w,color=BLUE,lw=2,label="Motore asincrono")
axc.axhline(ws,ls=":",color=GREY,lw=0.8); axc.text(0.05,ws+0.01,"ω$_s$ (sincronismo)",fontsize=7)
Cl=0.9
axc.axvline(Cl,color=GREEN,lw=1.6,ls="--")
axc.axvline(-Cl,color=RED,lw=1.6,ls="--")
axc.plot([Cl],[0.94],'o',color=GREEN); axc.text(Cl+0.05,0.90,"regime\nsalita",fontsize=7,color=GREEN)
axc.plot([-Cl],[1.06],'o',color=RED); axc.text(-Cl-0.05,1.06,"regime\ndiscesa",fontsize=7,color=RED,ha="right")
axc.axvline(0,color="k",lw=0.6); axc.set_xlim(-2.2,2.6); axc.set_ylim(0,1.25)
axc.set_xlabel("Coppia C  (ridotta al motore)",fontsize=8); axc.set_ylabel("ω",fontsize=8)
axc.set_title("Curva caratteristica: motore ∩ utilizzatore",fontsize=8.5)
axc.tick_params(labelsize=7)
T(ax,0.64,0.52,
 "Utilizzatore =\ncoppia costante\n(retta verticale):\n\n"
 "• salita  C = +C$_r$τ/η\n   (1° quadr., motore)\n\n"
 "• discesa C = −C$_r$τη*\n   (motore in frenatura,\n   ω>ω$_s$, scorr.<0)\n\n"
 "Intersezione = regime.",8.5)

T(ax,0.07,0.245,"2) Accelerazione in salita togliendo una cassa (dalla condiz. di regime)",10.5,"bold",GREY)
T(ax,0.07,0.228,
 "M$_m$ resta = M$_m^{sal}$.  Nuova resistenza (1 cassa su + m/2 giù): (1/2)mg·sinα.  Forza netta ridotta\n"
 "alla cinghia = (3/2 − 1/2)mg sinα = mg sinα.  Equazione ridotta al motore:",9)
ax.text(0.08,0.183,
 r"$M_m^{sal}-C_r^{new}\dfrac{\tau}{\eta}=[J_m+(2J_p+2J_r\frac{R^2}{r^2}+\frac{3}{2}mR^2)\dfrac{\tau^2}{\eta}]\alpha_m$",
 fontsize=10.5,va="top")
box(ax,0.08,0.130,
 r"$a=\tau R\,\alpha_m=\dfrac{mgR^{2}\tau^{2}\sin\alpha}{\;\eta J_m+(2J_p+2J_r R^{2}/r^{2}+\frac{3}{2}mR^{2})\tau^{2}\;}$",11,GREEN)
T(ax,0.07,0.070,
 "N.B. il numero di pulegge/rulli (qui 2+2) va adeguato allo schema reale; il metodo non cambia.",8.5,"normal",GREY)
pdf.savefig(fig); plt.close(fig)

# =====================================================================
# PAGINA 4 — ESERCIZIO 3 (meccanismo ECD)
# =====================================================================
fig,ax=new_page(); head(ax)
T(ax,0.07,0.925,"ESERCIZIO 3  —  Corpo ECD (aste CE e CD)  +  meccanismo",12,"bold",BLUE)
T(ax,0.07,0.905,"CE: lunghezza L, massa m (verticale).   CD: lunghezza L, massa m/2 (orizzontale).  Linee piane.",9)

# --- schizzo ECD ---
axe=fig.add_axes([0.63,0.62,0.32,0.235]); axe.set_xlim(-0.4,1.4); axe.set_ylim(-0.4,1.4); axe.axis("off")
axe.plot([0,0],[0,1],color=BLUE,lw=3); axe.text(-0.22,1.0,"E",fontsize=9); axe.text(-0.3,0.5,"CE (m)",fontsize=7,rotation=90,color=BLUE)
axe.plot([0,1],[0,0],color=GREEN,lw=3); axe.text(1.05,0,"D",fontsize=9); axe.text(0.4,-0.22,"CD (m/2)",fontsize=7,color=GREEN)
axe.text(-0.15,-0.15,"C",fontsize=9)
axe.plot([1/6],[1/3],'o',color=RED,ms=7); axe.text(1/6+0.06,1/3+0.05,"G",fontsize=9,color=RED)
axe.set_title("Corpo ECD (origine in C)",fontsize=8)

T(ax,0.07,0.845,"1) Baricentro G  (origine in C: E=(0,L), D=(L,0))",10.5,"bold",GREY)
ax.text(0.09,0.815,r"$M=m+\frac{m}{2}=\frac{3}{2}m$",fontsize=11,va="top")
ax.text(0.09,0.780,r"$x_G=\dfrac{m\cdot0+\frac{m}{2}\cdot\frac{L}{2}}{\frac{3}{2} m}=\dfrac{L}{6},\qquad y_G=\dfrac{m\cdot\frac{L}{2}+\frac{m}{2}\cdot0}{\frac{3}{2} m}=\dfrac{L}{3}$",fontsize=11,va="top")
box(ax,0.09,0.735,r"$G=\left(\dfrac{L}{6},\ \dfrac{L}{3}\right)$  rispetto a C",12,BLUE)

T(ax,0.07,0.665,"2) Momento d'inerzia rispetto a D",10.5,"bold",GREY)
ax.text(0.09,0.635,r"$I_D^{CE}=\frac{1}{12}mL^2+m\,d^2,\quad d^2=(L)^2+(\frac{L}{2})^2=\frac{5}{4}L^2\ \Rightarrow\ \frac{1}{12}mL^2+\frac{5}{4}mL^2=\frac{4}{3}mL^2$",fontsize=10.5,va="top")
ax.text(0.09,0.590,r"$I_D^{CD}=\frac{1}{3}(\frac{m}{2})L^2=\frac{1}{6}mL^2\quad(\text{asta con estremo in D})$",fontsize=10.5,va="top")
box(ax,0.09,0.545,r"$I_D=\frac{4}{3}mL^2+\frac{1}{6}mL^2=\dfrac{3}{2}\,mL^{2}$",12,GREEN)

T(ax,0.07,0.470,"3) Moto del meccanismo, coppia motrice M$_m$ e reazione in B",10.5,"bold",GREY)
T(ax,0.07,0.453,
 "Con manovella AB (priva di massa, ω = cost) si procede così:",9)
T(ax,0.09,0.420,
 "a) CINEMATICA: nota ω di AB, dai vincoli (guida in E/F e appoggio in D) si ricavano ω$_{ECD}$ e\n"
 "   le accelerazioni; con ω costante l'acc. angolare di AB è nulla (α$_{AB}$=0), ma α$_{ECD}$≠0 in genere.\n\n"
 "b) DINAMICA (teorema energia/potenze o eq. cardinali sul corpo ECD):\n"
 "   M$_m$·ω = d/dt(Energia cinetica) + potenza dei pesi   →   ricava M$_m$(θ).\n"
 "   Con I$_D$ = (3/2)mL² ed M = (3/2)m si scrive T = ½ I$_G$ ω$_{ECD}$² + ½ M v$_G$².\n\n"
 "c) REAZIONE in B: eq. di equilibrio dinamico (d'Alembert) del solo tratto/manovella collegato in B,\n"
 "   proiettando lungo e ortogonale ad AB.",9)
box(ax,0.07,0.235,
 "Le parti (1) baricentro e (2) I$_D$ sono complete ed esatte.\n"
 "Le parti (3) cinematica/coppia/reazione dipendono dalla geometria esatta dei vincoli\n"
 "(posizione di A, corsa della guida in E/F, punto B su CE): servono le quote/gli angoli\n"
 "leggibili dalla tavola per i valori numerici. Metodo sopra, formule pronte.",9.5,RED,pad=0.5)
T(ax,0.07,0.075,"Impostazione valida; con le quote della figura si completano i conti di (3).",8.5,"normal",GREY)
pdf.savefig(fig); plt.close(fig)

pdf.close()
print("Creato: Soluzioni_Meccanica_17-06-2025.pdf (4 pagine)")
