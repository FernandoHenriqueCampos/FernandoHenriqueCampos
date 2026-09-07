"""Generate Horizonte's self-contained SVG artwork. Python standard library only."""
from pathlib import Path
from html import escape
import math
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'horizonte'
OUT.mkdir(parents=True, exist_ok=True)
BG, WHITE, MUTED, CYAN, VIOLET, LINE = '#060b12', '#edf3f5', '#a4b3c2', '#a3dce4', '#9b93b8', '#263541'

def text(x, y, value, size=24, color=WHITE, weight=400, spacing=None, family='sans', anchor=None):
    font = 'Consolas, monospace' if family == 'mono' else 'Arial, Helvetica, sans-serif'
    extra = (f' letter-spacing="{spacing}"' if spacing is not None else '') + (f' text-anchor="{anchor}"' if anchor else '')
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{color}"{extra}>{escape(value)}</text>'

def line(x1,y1,x2,y2,color=LINE,width=1,opacity=1):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>' if y1==y2 else f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>'

def circle(x,y,r,fill=BG,stroke=LINE,width=1):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'

DEFS = f'''<defs>
  <radialGradient id="halo"><stop stop-color="{CYAN}" stop-opacity=".16"/><stop offset=".5" stop-color="#45687b" stop-opacity=".09"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>
  <radialGradient id="sphere" cx=".24" cy=".16" r=".84"><stop stop-color="#304450"/><stop offset=".23" stop-color="#13202d"/><stop offset=".6" stop-color="#090f19"/><stop offset="1" stop-color="#03070c"/></radialGradient>
  <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#d4eff1"/><stop offset=".34" stop-color="#63939e"/><stop offset=".64" stop-color="#273742"/><stop offset="1" stop-color="#141c29"/></linearGradient>
  <linearGradient id="orbit" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#9b93b8" stop-opacity=".06"/><stop offset=".42" stop-color="#a3dce4" stop-opacity=".4"/><stop offset=".72" stop-color="#d5eef1"/><stop offset="1" stop-color="#718697" stop-opacity=".1"/></linearGradient>
  <linearGradient id="fade"><stop stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".7"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
  <style>@media (prefers-reduced-motion: reduce) {{ .motion {{ display:none; }} }}</style>
</defs>'''

def svg(name,w,h,title,desc,body):
    content=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">\n<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>\n{DEFS}\n<rect width="{w}" height="{h}" fill="{BG}"/>\n{body}\n</svg>\n'
    (OUT/f'{name}.svg').write_text(content,encoding='utf-8')
    return content

def label(w,n,name,mobile=False):
    m=40 if mobile else 80
    return line(m,52,m+24,52,CYAN)+text(m+38,58,f'{n} / {name}',17,CYAN,spacing=2,family='mono')+text(w-m,58,'FHC',17,MUTED,spacing=3,family='mono',anchor='end')

def planet(cx,cy,r):
    # A conceptual gravitational horizon, not a scientific measurement or film asset.
    a=f'<g transform="translate({cx} {cy})">'+circle(0,0,r*1.95,'url(#halo)','none')
    for k in range(7):
        a+=f'<ellipse rx="{r*(1.62+k*.075):.2f}" ry="{r*(.39+k*.024):.2f}" transform="rotate(-27)" fill="none" stroke="url(#orbit)" stroke-width="{1 if k else 2}" opacity="{.5-k*.045:.3f}"/>'
    a+=circle(0,0,r,'url(#sphere)','url(#rim)',1.5)
    a+=f'<path d="M{-r*.75} {-r*.65} A{r} {r} 0 0 1 {r*.45} {-r*.895}" fill="none" stroke="#bee7ec" stroke-width="4" opacity=".35" filter="url(#soft)"/>'
    for k in range(4):
        rx=r*(1.62+k*.075); ry=r*(.39+k*.024)
        a+=f'<path d="M{-rx} 0 A{rx} {ry} 0 0 0 {rx} 0" transform="rotate(-27)" fill="none" stroke="url(#orbit)" stroke-width="{1.3 if k else 2.2}" opacity="{.8-k*.13}"/>'
    a+='</g>'
    return a

def stars(points):
    return ''.join(circle(x,y,r,CYAN,'none') for x,y,r in points)

def hero(mobile=False):
    w,h=(720,1040) if mobile else (1440,760)
    b=label(w,'01','HORIZONTE',mobile)
    if mobile:
        b+=planet(558,320,171)+stars([(420,130,1),(659,119,1),(363,356,1),(637,584,1.2)])
        b+=text(40,158,'FERNANDO',68,weight=600,spacing=-2)
        b+=text(40,236,'HENRIQUE',68,weight=600,spacing=-2)
        b+=text(40,314,'CAMPOS',68,weight=600,spacing=-2)
        b+=text(40,520,'FULL STACK DEVELOPER',25,CYAN,spacing=2)
        b+=text(40,576,'Sistemas · Automações',27)+text(40,616,'Soluções Corporativas',27)
        b+=text(40,680,'React · Next.js · FastAPI · PostgreSQL',23,MUTED)
        b+=line(40,734,680,734)
        b+=text(40,787,'PROCESS IMPACT',18,CYAN,spacing=2,family='mono')
        b+=text(40,875,'90',80,weight=500)+text(153,873,'MIN',20,MUTED,family='mono')
        b+=text(227,867,'→',50,MUTED)+text(308,817,'ATÉ',17,CYAN,family='mono')+text(306,875,'10',80,CYAN)+text(415,873,'MIN',20,MUTED,family='mono')
        b+=text(40,928,'Automação de uma rotina fiscal na Michelc.',24,MUTED)
        b+=text(40,996,'ENGENHARIA APLICADA AO TRABALHO REAL',16,MUTED,spacing=1,family='mono')
    else:
        b+=planet(1150,294,220)+stars([(878,133,1.2),(1385,147,.9),(827,367,.9),(1342,530,1),(1024,80,.8)])
        b+=text(80,184,'FERNANDO',100,weight=600,spacing=-4)
        b+=text(80,273,'HENRIQUE CAMPOS',78,weight=500,spacing=-3)
        b+=line(82,322,140,322,CYAN)
        b+=text(80,377,'FULL STACK DEVELOPER',25,CYAN,spacing=4)
        b+=text(80,430,'Sistemas · Automações · Soluções Corporativas',26)
        b+=text(80,479,'React · Next.js · FastAPI · PostgreSQL',22,MUTED)
        b+=line(80,555,1360,555)
        b+=text(80,606,'PROCESS IMPACT',17,CYAN,spacing=2,family='mono')
        b+=text(78,691,'90',82,weight=500)+text(183,689,'MIN',20,MUTED,family='mono')
        b+=text(250,680,'→',50,MUTED)+text(329,625,'ATÉ',16,CYAN,family='mono')+text(328,691,'10',82,CYAN)+text(431,689,'MIN',20,MUTED,family='mono')
        b+=line(547,602,547,699)
        b+=text(590,637,'Menos operação manual.',29)+text(590,682,'Mais espaço para o que importa.',29)
        b+=text(1360,732,'AUTOMAÇÃO FISCAL · MICHELC',15,MUTED,spacing=2,family='mono',anchor='end')
    svg('hero-mobile' if mobile else 'hero',w,h,'Fernando Henrique Campos — Full Stack Developer','Sistemas, automações e soluções corporativas. React, Next.js, FastAPI e PostgreSQL. Uma rotina fiscal de aproximadamente 90 minutos passou a levar até 10 minutos na Michelc.',b)

JOURNEY=[('2025','SERRATEC',['Residência em TIC','6 meses · período integral']),('2026','CODE ACADEMY',['Instituto 3C','Fundamentos + novas tecnologias']),('2026 — ATUAL','MICHELC',['Full Stack Trainee','Sistemas + automações']),('2026 — ATUAL','UTFPR',['Sistemas para Internet','Tecnologia · graduação'])]

def journey(mobile=False):
    w,h=(720,1050) if mobile else (1440,560)
    b=label(w,'03','TRAJETÓRIA',mobile)
    m=40 if mobile else 80
    b+=text(m,136,'A prática abre caminhos.',38 if mobile else 47,spacing=-1)
    b+=text(m,183,'Os fundamentos ampliam o horizonte.',25 if mobile else 29,MUTED)
    if mobile:
        b+='<path d="M76 280 C110 440 44 620 76 880" fill="none" stroke="url(#rim)" stroke-width="1.5"/>'
        for i,(year,title,desc) in enumerate(JOURNEY):
            y=280+i*185
            b+=circle(76,y,17,BG,LINE)+circle(76,y,5,CYAN if i<2 else BG,CYAN,1.5)
            b+=text(126,y-5,year,21,CYAN,family='mono')+text(126,y+39,title,32,weight=500)
            b+=text(126,y+79,desc[0],24,MUTED)+text(126,y+113,desc[1],23,MUTED)
        b+=line(40,991,680,991)+text(40,1023,'FORMAÇÃO → EXPERIÊNCIA → APROFUNDAMENTO',16,MUTED,family='mono')
    else:
        b+='<path d="M80 372 C400 372 650 288 960 283 S1280 248 1360 234" fill="none" stroke="url(#rim)" stroke-width="1.5"/>'
        positions=[(100,372),(415,338),(755,290),(1080,274)]
        for i,((x,y),(year,title,desc)) in enumerate(zip(positions,JOURNEY)):
            b+=line(x,y+21,x,419,LINE)+circle(x,y,17,BG,LINE)+circle(x,y,5,CYAN if i<2 else BG,CYAN,1.5)
            b+=text(x,y-57,year,20,CYAN,family='mono')
            b+=text(x,448,title,28,weight=500)+text(x,487,desc[0],22,MUTED)+text(x,519,desc[1],18,MUTED)
    svg('journey-mobile' if mobile else 'journey',w,h,'Trajetória — da formação à engenharia aplicada','2025: Serratec. 2026: Code Academy, Instituto 3C. 2026 até o presente: Michelc. 2026 até o presente: UTFPR. A curva representa progressão de trajetória, sem escala quantitativa.',b)

def orbital(cx,cy,r):
    b=f'<g transform="translate({cx} {cy})">'+circle(0,0,r*1.5,'url(#halo)','none')
    b+=circle(0,0,r*.66,'url(#sphere)','url(#rim)',1)
    for deg in [-28,28,90]:
        b+=f'<ellipse rx="{r}" ry="{r*.4}" transform="rotate({deg})" fill="none" stroke="{CYAN}" stroke-width="1" opacity=".3"/>'
    b+=circle(0,0,r,'none',LINE,1)
    for deg in range(0,360,15):
        rad=math.radians(deg)
        b+=line(round(math.cos(rad)*(r+8),2),round(math.sin(rad)*(r+8),2),round(math.cos(rad)*(r+13),2),round(math.sin(rad)*(r+13),2),LINE)
    b+=text(0,-7,'SISTEMAS',23,WHITE,spacing=3,anchor='middle')+text(0,27,'FULL STACK',15,CYAN,spacing=2,family='mono',anchor='middle')
    # Keep type fixed. Only the small satellite moves along the outer orbit.
    b+=f'<g class="motion"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="48s" repeatCount="indefinite"/>'+circle(0,-r,5,CYAN,'none')+circle(0,-r,12,'none',CYAN,1)+'</g></g>'
    return b

STACK=[('01','INTERFACE',['React · Next.js · Vue.js','React Native','TypeScript · JavaScript']),('02','BACKEND',['Python · FastAPI','Java · Spring']),('03','DATA',['PostgreSQL','Supabase · SQLite']),('04','INFRASTRUCTURE',['Docker','Git · GitHub'])]

def tech(mobile=False):
    w,h=(720,1250) if mobile else (1440,800)
    m=40 if mobile else 80
    b=label(w,'04','TECNOLOGIAS',mobile)+text(m,138,'Um sistema. Várias camadas.',37 if mobile else 47,spacing=-1)
    b+=text(m,181,'Da interface à infraestrutura.',26 if mobile else 29,MUTED)
    if mobile:
        b+=orbital(360,423,168)
        for (number,title,rows),(x,y) in zip(STACK,[(40,706),(395,706),(40,969),(395,969)]):
            b+=text(x,y-36,number,16,CYAN,family='mono')+line(x+36,y-43,x+280,y-43)
            b+=text(x,y,title,21,CYAN,spacing=1,family='mono')
            for j,row in enumerate(rows):
                # Shorter mobile lines preserve readable type without shrinking the whole diagram.
                if row=='React · Next.js · Vue.js':
                    row='React · Next.js'
                elif row=='React Native':
                    row='Vue.js · React Native'
                b+=text(x,y+45+j*37,row,23)
        b+=line(40,1175,680,1175)+text(40,1214,'INTERFACE / BACKEND / DATA / INFRA',17,MUTED,family='mono')
    else:
        b+=orbital(720,473,215)
        positions=[(80,326),(1055,326),(80,592),(1055,592)]
        paths=['M385 355 H450 L563 371','M1030 355 H973 L877 371','M330 605 H457 L563 575','M1030 605 H968 L877 575']
        for (number,title,rows),(x,y),p in zip(STACK,positions,paths):
            b+=f'<path d="{p}" fill="none" stroke="{LINE}" stroke-width="1"/>'
            b+=text(x,y-36,number,16,CYAN,family='mono')+line(x+36,y-43,x+280,y-43)
            b+=text(x,y,title,21,CYAN,spacing=2,family='mono')
            for j,row in enumerate(rows): b+=text(x,y+46+j*35,row,24)
        b+=line(80,741,1360,741)+text(80,776,'FERRAMENTAS CONECTADAS A NECESSIDADES REAIS',16,MUTED,spacing=1,family='mono')
        b+=text(1360,776,'INTERFACE → INFRAESTRUTURA',16,MUTED,family='mono',anchor='end')
    name='technologies-mobile' if mobile else 'technologies'
    content=svg(name,w,h,'Tecnologias — um sistema, várias camadas','Interface: React, Next.js, Vue.js, React Native, TypeScript, JavaScript. Backend: Python, FastAPI, Java, Spring. Data: PostgreSQL, Supabase, SQLite. Infrastructure: Docker, Git, GitHub. Órbitas conceituais, sem indicar proficiência ou tempo de experiência.',b)
    (OUT/f'{name}-static.svg').write_text(re.sub(r'<g class="motion">.*?</g>','',content),encoding='utf-8')

def footer(mobile=False):
    w,h=(720,380) if mobile else (1440,290)
    b=label(w,'08','CONTATO',mobile)
    if mobile:
        b+=text(40,133,'Transformando problemas',33,spacing=-.5)+text(40,180,'em sistemas,',33,spacing=-.5)+text(40,227,'uma solução de cada vez.',33,spacing=-.5)
        b+='<path d="M40 344 Q360 272 680 344" fill="none" stroke="url(#fade)"/>'
    else:
        b+=text(80,142,'Transformando problemas em sistemas,',40,spacing=-1)+text(80,198,'uma solução de cada vez.',40,spacing=-1)
        b+='<path d="M845 280 Q1120 121 1470 227" fill="none" stroke="url(#fade)"/>'
        b+=circle(1172,185,4,CYAN,'none')
    svg('footer-mobile' if mobile else 'footer',w,h,'Transformando problemas em sistemas, uma solução de cada vez.','Encerramento do perfil de Fernando Henrique Campos. Os links de LinkedIn e GitHub ficam em HTML, abaixo desta imagem, para serem clicáveis no README.',b)

if __name__=='__main__':
    for mobile in (False,True):
        hero(mobile); journey(mobile); tech(mobile); footer(mobile)
    print(f'Generated 10 SVG files in {OUT}')
