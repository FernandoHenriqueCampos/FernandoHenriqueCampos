"""Compact stack reference using local Devicon vectors and Horizonte tokens."""
import xml.etree.ElementTree as ET
from build_assets import OUT, svg, text, line, CYAN, MUTED

ET.register_namespace('', 'http://www.w3.org/2000/svg')
GROUPS=[
    ('INTERFACE',[('React','react'),('Next.js','nextjs'),('Vue.js','vuejs'),('React Native','react'),('TypeScript','typescript'),('JavaScript','javascript')]),
    ('BACKEND',[('Python','python'),('FastAPI','fastapi'),('Java','java'),('Spring','spring')]),
    ('DATA',[('PostgreSQL','postgresql'),('Supabase','supabase'),('SQLite','sqlite')]),
    ('INFRASTRUCTURE',[('Docker','docker'),('Git','git'),('GitHub','github')]),
]

def icon(name,x,y,size):
    root=ET.parse(OUT/'icons'/f'{name}.svg').getroot()
    root.set('x',str(x)); root.set('y',str(y)); root.set('width',str(size)); root.set('height',str(size))
    root.set('fill',CYAN)
    for node in root.iter():
        for attr in ('fill','stroke'):
            if attr in node.attrib and node.attrib[attr]!='none': node.set(attr,CYAN)
    return ET.tostring(root,encoding='unicode')

def build(mobile):
    w,h=(720,850) if mobile else (1440,420)
    m=40 if mobile else 80
    b=line(m,35,m+24,35,CYAN)+text(m+38,41,'STACK / FERRAMENTAS',16,CYAN,spacing=2,family='mono')
    top=96
    for group,items in GROUPS:
        if mobile:
            b+=text(m,top,group,18,MUTED,spacing=1,family='mono')+line(40,top+15,680,top+15)
            for i,(name,key) in enumerate(items):
                x=m+(i%2)*330; y=top+35+(i//2)*54
                b+=icon(key,x,y,29)+text(x+45,y+24,name,25)
            top+=52+((len(items)+1)//2)*54
        else:
            b+=text(m,top+23,group,17,MUTED,spacing=1,family='mono')
            for i,(name,key) in enumerate(items):
                x=305+i*178
                b+=icon(key,x,top,28)+text(x+40,top+23,name,20)
            b+=line(m,top+53,1360,top+53)
            top+=80
    description='; '.join(group+': '+', '.join(name for name,key in items) for group,items in GROUPS)
    svg('stack-card'+('-mobile' if mobile else ''),w,h,'Stack — tecnologias e ícones',description,b)

if __name__=='__main__':
    build(False); build(True)
