from PIL import Image
import io,struct, pathlib, shutil
root=pathlib.Path(__file__).parent
im=Image.open(str(root/'NETUpdateManager.png')).convert('RGBA')
# crop transparent edges and center in square
alpha=im.getchannel('A'); bbox=alpha.point(lambda a:255 if a>10 else 0).getbbox(); im=im.crop(bbox)
side=max(im.size); canvas=Image.new('RGBA',(side,side),(0,0,0,0));canvas.alpha_composite(im,((side-im.width)//2,(side-im.height)//2))
images=[]
for s in [16,32,48,256]:
 t=canvas.resize((s,s),Image.Resampling.LANCZOS); b=io.BytesIO();t.save(b,'PNG');images.append((s,b.getvalue()))
# ico standalone
ico=bytearray(struct.pack('<HHH',0,1,len(images)));offset=6+16*len(images)
for s,content in images:
 ico+=struct.pack('<BBBBHHII',0 if s==256 else s,0 if s==256 else s,0,0,1,32,len(content),offset);offset+=len(content)
for s,content in images:ico+=content
(root/'NETUpdateManager.ico').write_bytes(ico)
(root/'NETUpdateManager.png').write_bytes((lambda x: (lambda b:b.getvalue())(io.BytesIO()))(None) if False else b'')
canvas.resize((512,512),Image.Resampling.LANCZOS).save(root/'NETUpdateManager.png')
# PE modify
f=root/'NETUpdateManager.exe'; data=bytearray(f.read_bytes()); pe=struct.unpack_from('<I',data,0x3c)[0]; coff=pe+4; n=struct.unpack_from('<H',data,coff+2)[0]; opt=pe+24; optsize=struct.unpack_from('<H',data,coff+16)[0]; sh=opt+optsize
align=lambda x,a:(x+a-1)//a*a
sec_align,file_align=struct.unpack_from('<II',data,opt+32)
last=sh+(n-1)*40;lv,lr,lp=struct.unpack_from('<III',data,last+8)
base=align(lv+lr,sec_align);rawptr=align(len(data),file_align)
# resource directory with RT_ICON ID=3 and RT_GROUP_ICON ID=14: directory tree each type -> id -> lang
R=bytearray();
def append(blob,alignment=4):
 while len(R)%alignment:R.append(0)
 pos=len(R);R.extend(blob);return pos
rootdir=append(bytes(16+2*8))
typedirs={3:append(bytes(16+4*8)),14:append(bytes(16+1*8))}
subdirs={}
for typ,items in [(3,list(range(1,len(images)+1))),(14,[1])]:
 for i in items:subdirs[(typ,i)]=append(bytes(16+8))
# data entries
entries={}
for typ,items in [(3,list(range(1,len(images)+1))),(14,[1])]:
 for i in items:entries[(typ,i)]=append(bytes(16))
# data blobs
data_blobs={}
for i,(s,content) in enumerate(images,1):data_blobs[(3,i)]=append(content)
grp=bytearray(struct.pack('<HHH',0,1,len(images)))
for i,(s,content) in enumerate(images,1):grp+=struct.pack('<BBBBHHIH',0 if s==256 else s,0 if s==256 else s,0,0,1,32,len(content),i)
data_blobs[(14,1)]=append(grp)
# write tree
struct.pack_into('<HH',R,12,0,2)
for ii,typ in enumerate((3,14)):
 struct.pack_into('<II',R,16+ii*8,typ,typedirs[typ]|0x80000000)
 ids=list(range(1,5)) if typ==3 else [1]; d=typedirs[typ];struct.pack_into('<HH',R,d+12,0,len(ids))
 for j,i in enumerate(ids):
  struct.pack_into('<II',R,d+16+8*j,i,subdirs[(typ,i)]|0x80000000)
  sub=subdirs[(typ,i)];struct.pack_into('<HH',R,sub+12,0,1);struct.pack_into('<II',R,sub+16,1033,entries[(typ,i)])
  entry=entries[(typ,i)]; offset=data_blobs[(typ,i)]; content=images[i-1][1] if typ==3 else grp
  struct.pack_into('<IIII',R,entry,base+offset,len(content),0,0)
# PE headers
newraw=align(len(R),file_align);data.extend(bytes(rawptr-len(data)));data.extend(R);data.extend(bytes(newraw-len(R)))
struct.pack_into('<H',data,coff+2,n+1)
struct.pack_into('<I',data,opt+56,align(base+len(R),sec_align))
# resource directory index 2, opt+112 for PE32+
magic=struct.unpack_from('<H',data,opt)[0];datadir=opt+(112 if magic==0x20b else 96);struct.pack_into('<II',data,datadir+2*8,base,len(R))
# section header
struct.pack_into('<8sIIIIIIHHI',data,sh+n*40,b'.rsrc\x00\x00\x00',len(R),base,newraw,rawptr,0,0,0,0,0x40000040)
f.write_bytes(data)
print('resource',len(R),'EXE',len(data),'icon',len(ico),'rva',hex(base))
