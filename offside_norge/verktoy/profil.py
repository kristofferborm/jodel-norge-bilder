from PIL import Image, ImageDraw, ImageFont
F="fonts/Poppins-%s.ttf"
S=1080
def font(w,s): return ImageFont.truetype(F%w,s)
def dashed_v(d,x,y0,y1,col,w=10,dash=34,gap=22):
    y=y0
    while y<y1:
        d.rectangle([x-w//2,y,x+w//2,min(y+dash,y1)],fill=col); y+=dash+gap
def center_text(d,txt,f,y,col,cx=S//2):
    w=d.textlength(txt,font=f); d.text((cx-w/2,y),txt,font=f,fill=col)

def v_a(bg,fg,ac,name):
    # "offsid | e" — e-en står offside
    im=Image.new("RGB",(S,S),bg); d=ImageDraw.Draw(im)
    f=font("Bold",165)
    a,b="offsid","e"
    wa=d.textlength(a,font=f); wb=d.textlength(b,font=f); gap=70
    tot=wa+gap+wb; x0=(S-tot)/2
    bbox=d.textbbox((0,0),"offside",font=f); th=bbox[3]-bbox[1]
    y=(S-th)/2-bbox[1]
    d.text((x0,y),a,font=f,fill=fg)
    lx=x0+wa+gap/2
    dashed_v(d,int(lx),300,780,ac)
    d.text((x0+wa+gap,y),b,font=f,fill=fg)
    im.save(f"profil/{name}.png"); return im

def v_b(bg,fg,ac,name):
    # Stablet ordmerke med aksentstrek, som postene
    im=Image.new("RGB",(S,S),bg); d=ImageDraw.Draw(im)
    f=font("Bold",170)
    bb=d.textbbox((0,0),"OFFSIDE",font=f)
    w=bb[2]-bb[0]
    y=430
    d.rectangle([S//2-w//2, y-70, S//2-w//2+160, y-50],fill=ac)
    d.text((S//2-w//2-bb[0],y-bb[1]),"OFFSIDE",font=f,fill=fg)
    d.text((S//2-w//2,y+bb[3]-bb[1]+30),"NORGE",font=font("SemiBold",64),fill=ac)
    im.save(f"profil/{name}.png"); return im

def circle_preview(ims,labels,out):
    sz=360; pad=40
    sheet=Image.new("RGB",(len(ims)*(sz+pad)+pad,sz+2*pad+190),"#FFFFFF")
    d=ImageDraw.Draw(sheet)
    mask=Image.new("L",(sz,sz),0); ImageDraw.Draw(mask).ellipse([0,0,sz,sz],fill=255)
    for i,(im,l) in enumerate(zip(ims,labels)):
        x=pad+i*(sz+pad)
        sheet.paste(im.resize((sz,sz),Image.LANCZOS),(x,pad),mask)
        d.text((x,pad+sz+12),l,font=font("SemiBold",26),fill="#222")
    for i,im in enumerate(ims):
        for j,t in enumerate((110,44)):
            m=Image.new("L",(t,t),0); ImageDraw.Draw(m).ellipse([0,0,t,t],fill=255)
            x=pad+i*(sz+pad)+200+j*125
            sheet.paste(im.resize((t,t),Image.LANCZOS),(x,pad+sz+60),m)
    sheet.save(out)

ims=[v_a("#111418","#FFFFFF","#3DDC84","A_mork"),
     v_a("#1F6B3F","#FFFFFF","#FFFFFF","A_gress"),
     v_b("#111418","#FFFFFF","#3DDC84","B_mork")]
circle_preview(ims,["A – mørk","A – gress","B – ordmerke"],"profil/forhandsvisning.png")
