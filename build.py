import json,subprocess,os,hashlib,struct
OUT='deck.pptx'
TOTAL=16
# --- palet M3 Expressive dari #B0C8E0 #C1E0E0 #DCE7D6 #F6F6F6 ---
BG,CARD='F6F6F6','E6E9E9'
TX,MUT='2F3334','5B6061'
P,ON_P,PC,ON_PC='46627A','F6F9FF','B0C8E0','355169'
SC,ON_SC='C1E0E0','3D6060'
TC,ON_TC='DCE7D6','536350'
EC,ON_EC='FFDAD6','65000B'
PILL_PC,PILL_EC='C9DBEC','F7C7C1'
COOKIE,FLOWER,CLOVER,SQUIRCLE,BURST,SUNNY='cookie','flower','clover','squircle','burst','sunny'
F='Calibri'
ops=[];specs={};n=0
counts={}
def cm(v):return f'{v:.2f}cm'
def icon(name,shape,bg,fg):
    f=hashlib.md5(f'{name}{shape}{bg}{fg}'.encode()).hexdigest()[:10]+'.png'
    specs[f]=dict(file=f,icon=name,shape=shape,bg=bg,fg=fg);return f
def emit(parent,typ,props):ops.append(dict(command='add',parent=parent,type=typ,props={k:str(v) for k,v in props.items()}))
def add(parent,typ,**p):
    emit(parent,typ,p)
    if typ in ('shape','picture','chart','group'):counts[parent]=counts.get(parent,0)+1
    return counts.get(parent)
def slide(bg):
    global n;n+=1;add('/','slide',background=bg);s=f'/slide[{n}]';counts[s]=0;return s
def box(s,x,y,w,h,fill,r=1.0,line=None,dash=None,name='kartu'):
    a=min(50000,int(r/min(w,h)*100000))
    pr=dict(geometry='roundRect',adj=f'adj:val {a}',x=cm(x),y=cm(y),width=cm(w),height=cm(h),fill=fill,name=name)
    if line:pr.update(line=line,lineWidth='1.5pt')
    else:pr.update(line='none')
    if dash:pr['lineDash']=dash
    add(s,'shape',**pr)
def tx(s,x,y,w,h,t,size=18,color=TX,bold=False,align='left',valign='top',name='teks'):
    add(s,'shape',x=cm(x),y=cm(y),width=cm(w),height=cm(h),text=t,size=size,color=color,bold=str(bold).lower(),
        align=align,valign=valign,font=F,fill='none',line='none',margin='0',name=name)
def pic(s,f,x,y,w,alt,h=None):add(s,'picture',src=os.path.abspath('assets/'+f),x=cm(x),y=cm(y),width=cm(w),height=cm(h or w),alt=alt)
def clipped(s,f,x,y,w,h,alt):
    with open(os.path.abspath('assets/'+f),'rb') as fh:head=fh.read(24)
    iw,ih=struct.unpack('>II',head[16:24])
    if not abs(iw/ih-w/h)<0.01:raise ValueError(f'{f}: rasio {iw/ih:.3f} tidak cocok dengan kartu {w/h:.3f}; jangan regangkan mask')
    pic(s,f,x,y,w,alt,h)
def shot(s,f,x,y,w,alt):
    h=w*9/16
    box(s,x-0.08,y-0.08,w+0.16,h+0.16,'FFFFFF',0.4,name='bingkai')
    clipped(s,f,x,y,w,h,alt)
    return h
def notes(s,t):add(s,'notes',text=t)
def num(s,x,y,d,t,fill,col):
    add(s,'shape',geometry='ellipse',x=cm(x),y=cm(y),width=cm(d),height=cm(d),text=t,size=20,bold='true',color=col,
        align='center',valign='middle',font=F,fill=fill,line='none',margin='0',name='nomor')
def page(s):tx(s,29.4,18.2,3,0.6,f'{n} / {TOTAL}',10,MUT,align='right',name='nomor-slide')
def frame(title):
    s=slide(BG)
    if title:tx(s,1.2,1.2,31.2,2.4,title,36,TX,True,valign='middle',name='judul')
    page(s)
    return s
X0,W=1.2,31.2
def card3(s,y,h,items,fills):
    w=(W-1.6)/3
    for k,(ic,hd,bd) in enumerate(items):
        x=X0+k*(w+0.8);box(s,x,y,w,h,fills[k][0],1.2)
        pic(s,icon(ic,[COOKIE,CLOVER,SQUIRCLE][k],fills[k][1],fills[k][2]),x+0.8,y+0.8,2.4,hd)
        tx(s,x+0.8,y+3.5,w-1.6,2.05,hd,24,fills[k][3],True)
        tx(s,x+0.8,y+4.8,w-1.6,h-4.6,bd,18,fills[k][3])
# 1 sampul
s=slide(BG)
pic(s,icon('MdLibraryBooks',FLOWER,PC,ON_PC),20.6,2.6,12,'Ilustrasi Mendeley')
pic(s,icon('MdFormatQuote',CLOVER,TC,ON_TC),29.0,14.7,4.2,'Ikon kutipan')
box(s,1.2,3.0,8.4,1.6,PC,0.8,name='label');tx(s,1.2,3.0,8.4,1.6,'Bahasa Indonesia',18,ON_PC,True,'center','middle')
tx(s,1.2,4.4,18.8,7.8,'Implementasi Mendeley dalam penulisan karya ilmiah',44,TX,True,name='judul')
tx(s,1.2,13.4,18.8,1,'Mata kuliah Bahasa Indonesia',20,P,True)
notes(s,'Salam pembuka. Perkenalkan topik: cara Mendeley dipakai untuk menyusun kutipan dan daftar pustaka karya ilmiah.')
# 2 anggota
s=slide(BG)
tx(s,1.2,1.4,31.2,2.4,'Anggota kelompok',40,TX,True,valign='middle',name='judul')
tx(s,1.2,3.6,31.2,1,'Mata kuliah Bahasa Indonesia',18,P,True)
for k,(nm,nim) in enumerate([('Aminadab Yunus','202451028'),('Muhammad Rifqi al Khafis','202551019'),('Arkano Hamada Moslem','202551034'),('Farrel Aufa Athaya Ardiyono','202551042'),("Muhammad La'azidannak Rusda",'202551049'),('Aksel Agustiyan','202551058'),('Muhammad Arief Satria Nugraha','202551151')]):
    x=(1.2+k*7.6) if k<4 else (5.8+(k-4)*7.6);y=5.2 if k<4 else 11.0
    fill=[PC,CARD,TC,CARD,PC,CARD,CARD][k];col=[ON_PC,TX,ON_TC,TX,ON_PC,TX,TX][k]
    box(s,x,y,6.8,5.2,fill,1.2)
    clipped(s,f'num-{k+1:02d}.png',x+0.05,y+0.04,6.7,5.12,'Nomor '+f'{k+1:02d}')
    tx(s,x+0.6,y+1.3,5.6,2.4,nm,18,col,True)
    tx(s,x+0.6,y+3.8,5.6,1.2,nim,12,col)
page(s)
notes(s,'Sebutkan anggota kelompok satu per satu sesuai urutan NIM.')
# 3 latar belakang
s=frame('Kekurangan sitasi manual')
card3(s,4.0,8.2,[('MdFormatAlignLeft','Format berbeda','Gaya sitasi bisa berbeda antarbagian karena diketik satu per satu.'),
 ('MdLinkOff','Sumber terlupa','Kutipan ada di naskah, tetapi rujukannya tidak masuk daftar pustaka.'),
 ('MdCompareArrows','Daftar tidak cocok','Isi daftar pustaka tidak sama dengan sumber yang dikutip di teks.')],[(CARD,PC,ON_PC,TX)]*3)
box(s,X0,13.0,W,5.0,PC,1.4)
pic(s,icon('MdTimer',SUNNY,P,'FFFFFF'),X0+1.0,14.2,2.6,'Ikon waktu')
tx(s,X0+4.4,13.4,W-5.4,4.2,'Sitasi manual memakan waktu. Sumber yang lupa dicantumkan bisa dianggap plagiarisme.',22,ON_PC,False,valign='middle')
notes(s,'Tiga kekurangan sitasi manual: format tidak konsisten, sumber terlupa, dan daftar pustaka tidak cocok dengan teks. Ketiganya berkaitan dengan etika kutipan dan plagiarisme yang kita pelajari di mata kuliah ini.')
# 4 rumusan
s=frame('Rumusan masalah dan tujuan')
w2,gap=13.6,0.8
start=X0+(W-(2*w2+gap))/2
for k,(ic,hd,its,pitch,fill,col,nb,nc) in enumerate([('MdQuestionAnswer','Rumusan masalah',['Bagaimana cara mengimplementasikan Mendeley dalam penulisan karya ilmiah?','Apa manfaat dan keterbatasan Mendeley bagi mahasiswa?'],4.2,CARD,TX,P,'FFFFFF'),
 ('MdFlag','Tujuan',['Menjelaskan fungsi Mendeley.','Menguraikan langkah penggunaannya.','Menilai manfaat dan keterbatasannya.'],2.9,TC,ON_TC,ON_TC,'FFFFFF')]):
    x=start+k*(w2+gap);box(s,x,4.0,w2,14.0,fill,1.4)
    clipped(s,'mask-04-tanya.png' if k==0 else 'mask-04-tujuan.png',x,4.0,w2,14.0,'Masking tanda')
    pic(s,icon(ic,[COOKIE,CLOVER][k],PC if k==0 else SC,ON_PC if k==0 else ON_TC),x+0.9,4.9,2.2,hd)
    tx(s,x+3.6,4.9,9,2.2,hd,24,col,True,valign='middle')
    for j,t in enumerate(its):
        y=8.2+j*pitch;num(s,x+0.9,y,1.5,str(j+1),nb,nc);tx(s,x+3.0,y-0.2,10,pitch-0.4,t,20,col,valign='top')
notes(s,'Dua rumusan masalah menuntun presentasi ini: cara implementasi dan manfaat serta keterbatasan. Tiga tujuan mengikuti urutan tersebut: fungsi, langkah, lalu evaluasi.')
# 5 fitur utama
s=frame('Fitur utama')
feats=[
 ('MdLibraryBooks','Reference Library','Simpan dan kelola referensi.',COOKIE,PC,ON_PC),
 ('MdPictureAsPdf','PDF Reader','Baca, highlight, dan beri catatan.',CLOVER,SC,ON_SC),
 ('MdFormatQuote','Mendeley Cite','Sitasi langsung di Microsoft Word.',SQUIRCLE,TC,ON_TC),
 ('MdCloudSync','Sinkronisasi cloud','Akses dari berbagai perangkat.',BURST,PC,ON_PC),
 ('MdGroup','Groups','Bagikan referensi dengan kolaborator.',SUNNY,SC,ON_SC),
 ('MdExtension','Web Importer','Simpan referensi dari browser.',FLOWER,TC,ON_TC),
]
w3=(W-1.6)/3;h=6.6
for k,(ic,hd,bd,shape,bg,fg) in enumerate(feats):
    x=X0+(k%3)*(w3+0.8);y=4.0+(k//3)*(h+0.8)
    box(s,x,y,w3,h,CARD,1.4)
    pic(s,icon(ic,shape,bg,fg),x+0.8,y+0.8,2.0,hd)
    tx(s,x+0.8,y+3.1,w3-1.6,1.0,hd,20,TX,True)
    tx(s,x+0.8,y+4.2,w3-1.6,2.0,bd,16,MUT)
notes(s,'Enam fitur utama Mendeley: Reference Library untuk menyimpan referensi, PDF Reader untuk membaca dan menandai, Mendeley Cite untuk sitasi di Word, sinkronisasi cloud, Groups untuk berbagi, dan Web Importer untuk menyimpan referensi dari browser.')
# 6 instalasi akun dan aplikasi
s=frame('Instalasi: akun dan aplikasi')
shot(s,'shot-account.png',X0,4.0,18.0,'Situs resmi Mendeley')
tx(s,X0,14.4,18.0,0.7,'Situs resmi Mendeley',12,MUT,align='center')
for k,t in enumerate(['Buka situs resmi Mendeley.','Buat akun dengan email atau akun Elsevier.','Unduh Mendeley Reference Manager.','Instal aplikasi, lalu login.']):
    y=4.0+k*3.3
    num(s,20.0,y,1.3,str(k+1),P,'FFFFFF')
    tx(s,21.7,y-0.1,10.7,3.0,t,18,TX,valign='top')
notes(s,'Instalasi dimulai dari situs resmi Mendeley. Buat akun dengan email atau akun Elsevier, unduh Reference Manager, lalu instal dan login. Tangkapan layar: Mendeley (n.d.).')
# 7 instalasi web importer dan cite
s=frame('Instalasi: Web Importer dan Cite')
for k,(f,hd,bd) in enumerate([('shot-extension.png','Web Importer','Pasang ekstensi di browser, lalu simpan referensi dari halaman artikel.'),('shot-addin.png','Mendeley Cite','Pasang add-in di Microsoft Word, lalu buka tab References.')]):
    x=X0+k*16.0;box(s,x,4.0,15.2,14.0,CARD,1.4)
    shot(s,f,x+0.8,4.8,13.6,hd)
    num(s,x+0.8,12.8,1.2,str(k+5),P,'FFFFFF')
    tx(s,x+2.2,12.7,12.2,1.2,hd,22,TX,True)
    tx(s,x+0.8,14.2,13.6,2.8,bd,17,MUT)
notes(s,'Langkah kelima memasang Web Importer di browser. Langkah keenam memasang Mendeley Cite di Microsoft Word. Tangkapan layar: Mendeley (n.d.).')
# 8 antarmuka
s=frame('Tampilan antarmuka')
shot(s,'shot-details.png',X0,4.0,19.2,'Antarmuka Mendeley Reference Manager')
tx(s,X0,14.9,19.2,0.7,'Antarmuka Mendeley Reference Manager',12,MUT,align='center')
for k,(hd,bd,col) in enumerate([('Panel kiri','Koleksi, folder, dan grup.',PC),('Panel tengah','Daftar referensi.',SC),('Panel kanan','Detail metadata.',TC)]):
    y=4.2+k*4.2
    box(s,21.2,y+0.1,0.3,2.8,col,0.15)
    tx(s,21.8,y,9.8,1.0,hd,20,TX,True)
    tx(s,21.8,y+1.0,9.8,2.2,bd,17,MUT)
notes(s,'Tampilan Reference Manager dibagi tiga panel: koleksi, folder, dan grup di kiri; daftar referensi di tengah; detail metadata di kanan. Tangkapan layar: Mendeley (n.d.).')
# 9 pdf reader
s=frame('PDF Reader: baca dan tandai')
for k,(f,hd,bd) in enumerate([('shot-highlight.png','Highlight dan anotasi','Tandai bagian penting langsung di PDF.'),('shot-notes.png','Catatan','Tulis ringkasan atau komentar per referensi.')]):
    x=X0+k*16.0;box(s,x,4.0,15.2,14.0,CARD,1.4)
    shot(s,f,x+0.8,4.8,13.6,hd)
    tx(s,x+0.8,12.8,13.6,1.2,hd,22,TX,True)
    tx(s,x+0.8,14.2,13.6,2.8,bd,17,MUT)
notes(s,'PDF Reader terintegrasi dengan Reference Manager. Bagian penting bisa di-highlight, diberi anotasi, atau dicatat di Notebook. Tangkapan layar: Mendeley (n.d.).')
# 10 menambahkan referensi
s=frame('Menambahkan referensi')
shot(s,'shot-rm-add.png',X0,4.0,18.0,'Menu Add reference')
tx(s,X0,14.4,18.0,0.7,'Menu Add reference',12,MUT,align='center')
for k,(ic,hd,bd,shape,bg,fg) in enumerate([('MdUploadFile','Unggah PDF','Tarik file ke Library.',COOKIE,PC,ON_PC),('MdExtension','Web Importer','Simpan dari halaman artikel.',CLOVER,SC,ON_SC),('MdEdit','Input manual','Isi DOI, ISBN, atau PMID.',SQUIRCLE,TC,ON_TC),('MdFileUpload','Impor file','RIS, BibTeX, EndNote XML.',BURST,PC,ON_PC)]):
    y=4.0+k*3.3
    pic(s,icon(ic,shape,bg,fg),20.0,y,1.6,hd)
    tx(s,22.0,y-0.1,10.4,1.0,hd,20,TX,True)
    tx(s,22.0,y+1.0,10.4,2.2,bd,16,MUT)
notes(s,'Referensi bisa masuk lewat unggahan PDF, Web Importer, input manual DOI/ISBN/PMID, atau impor RIS, BibTeX, dan EndNote XML. Tangkapan layar menu Add reference: Mendeley (n.d.).')
# 11 mendeley cite
s=frame('Mendeley Cite di Word')
shot(s,'shot-addin.png',X0,4.0,14.0,'Mendeley Cite di Microsoft Word')
tx(s,X0,12.2,14.0,0.7,'Mendeley Cite di Microsoft Word',12,MUT,align='center')
box(s,X0,13.2,14.0,4.2,CARD,1.2)
tx(s,X0+0.9,13.2,12.2,4.2,'Gaya sitasi bisa diganti tanpa menulis ulang.',18,MUT,valign='middle')
for k,t in enumerate(['Buka Microsoft Word, lalu tab References.','Klik Mendeley Cite.','Pilih referensi dari pustaka.','Klik Insert Citation.','Pilih gaya sitasi.','Klik Insert Bibliography.']):
    y=4.0+k*2.3
    num(s,16.0,y,1.3,str(k+1),P,'FFFFFF')
    tx(s,17.4,y-0.1,14.6,2.1,t,17,TX,valign='top')
notes(s,'Di Word, buka tab References lalu Mendeley Cite. Pilih referensi, klik Insert Citation, tentukan gaya, lalu Insert Bibliography. Gaya bisa diganti kapan saja. Tangkapan layar: Mendeley Support (2025).')
# 12 gaya sitasi
s=frame('Gaya sitasi')
box(s,X0,4.0,W,1.2,P,0.6)
tx(s,X0+1.0,4.0,6.0,1.2,'Gaya',16,'FFFFFF',True,valign='middle')
tx(s,X0+8.0,4.0,22.0,1.2,'Contoh bidang',16,'FFFFFF',True,valign='middle')
for k,(style,field) in enumerate([('APA','Psikologi, pendidikan, sosial'),('IEEE','Teknik, informatika'),('Harvard','Bisnis, manajemen'),('Chicago','Humaniora, sejarah'),('Vancouver','Kedokteran, kesehatan')]):
    y=5.5+k*2.3
    box(s,X0,y,W,2.1,[CARD,SC,TC,CARD,SC][k],0.9)
    tx(s,X0+1.0,y,6.0,2.1,style,18,TX,True,valign='middle')
    tx(s,X0+8.0,y,22.0,2.1,field,18,MUT,valign='middle')
tx(s,X0,17.0,W,0.8,'Gaya dapat diganti kapan saja tanpa menulis ulang.',14,MUT)
notes(s,'Lima gaya yang umum: APA untuk psikologi, pendidikan, dan sosial; IEEE untuk teknik dan informatika; Harvard untuk bisnis dan manajemen; Chicago untuk humaniora dan sejarah; Vancouver untuk kedokteran dan kesehatan. Gaya bisa diganti kapan saja.')
# 13 satu sumber dua keluaran
s=frame('Satu sumber untuk dua rujukan')
tx(s,X0,3.3,W,0.9,'Metadata yang sama menjadi bahan sitasi dan daftar pustaka.',18,MUT)
wL,wR=12.0,18.4
box(s,X0,4.2,wL,13.2,PC,1.4)
tx(s,X0+0.8,4.8,wL-1.6,0.8,'Satu sumber',14,ON_PC,True)
shot(s,'shot-source.png',X0+1.2,5.7,9.6,'PDF jurnal dan metadata')
tx(s,X0+0.8,11.3,wL-1.6,0.8,'PDF jurnal dan metadata',16,ON_PC,True)
tx(s,X0+0.8,12.1,wL-1.6,3.2,'Penulis, tahun, judul, dan DOI dipakai untuk keduanya.',16,ON_PC)
xR=X0+wL+0.8
for k,(f,hd,bd,fill,col) in enumerate([('shot-citation.png','Sitasi dalam teks','Mendeley Cite menyisipkan sitasi ke dalam kalimat.',SC,ON_SC),('shot-bib-menu.png','Daftar pustaka','Mendeley menyusun entri lengkap dari metadata yang sama.',TC,ON_TC)]):
    y=4.2+k*6.9;box(s,xR,y,wR,6.3,fill,1.4)
    tx(s,xR+0.8,y+0.5,wR-1.6,0.7,hd,14,col,True)
    shot(s,f,xR+0.8,y+1.4,7.2,hd)
    tx(s,xR+8.4,y+1.6,wR-9.2,2.6,bd,18,col)
    if k==0:pic(s,icon('MdArrowForward','none','x',P),X0+wL+0.05,7.1,0.7,'Panah')
    else:pic(s,icon('MdArrowForward','none','x',P),X0+wL+0.05,14.0,0.7,'Panah')
notes(s,'Satu referensi di Library menjadi sumber untuk sitasi di Word dan entri daftar pustaka. Tangkapan layar menunjukkan panel Cite dan menu Insert Bibliography; teori gaya sitasi tetap di Kelompok 4. Tangkapan layar: Mendeley Support (2025).')
# 14 kelebihan keterbatasan
s=frame('Kelebihan dan keterbatasan')
for k,(ic,hd,its,fill,col,sh,fg) in enumerate([('MdCheckCircle','Kelebihan',['Hemat waktu','Gaya sitasi konsisten','Kutipan dan daftar pustaka sinkron','Penyimpanan dan sinkronisasi lintas perangkat'],PC,ON_PC,P,'FFFFFF'),('MdWarning','Keterbatasan',['Metadata hasil impor perlu diperiksa','Gaya sitasi khusus kampus perlu ditambahkan manual','Penyimpanan gratis hanya 2 GB','PDF hasil pindai biasanya masuk tanpa metadata'],EC,ON_EC,'F56965','FFFFFF')]):
    w2=(W-0.8)/2
    x=X0+k*(w2+0.8);box(s,x,4.0,w2,14.0,fill,1.4)
    pic(s,icon(ic,[CLOVER,BURST][k],sh,fg),x+0.9,4.8,2.2,hd);tx(s,x+3.6,4.8,w2-4.2,2.2,hd,24,col,True,valign='middle')
    pill=PILL_PC if k==0 else PILL_EC
    for j,t in enumerate(its):
        y=7.7+j*2.5
        box(s,x+0.8,y,w2-1.6,1.9,pill,0.95,name='kapsul')
        tx(s,x+1.4,y,w2-2.4,1.9,t,16,col,valign='middle')
notes(s,'Kelebihan: hemat waktu, gaya sitasi konsisten, dan sinkron. Keterbatasannya: metadata hasil impor perlu diperiksa, gaya sitasi khusus kampus perlu ditambahkan manual, penyimpanan gratis hanya 2 GB, dan PDF hasil pindai biasanya masuk tanpa metadata.')
# 15 kesimpulan (terang)
s=frame('Kesimpulan')
w2=(W-0.8)/2
for k,(ic,hd,bd,fill,col,ib,ifg) in enumerate([
 ('MdCheckCircle','Implementasinya','Impor referensi, sisipkan sitasi di Word, lalu buat daftar pustaka otomatis.',PC,ON_PC,P,ON_P),
 ('MdSchool','Manfaat dan batasannya','Gaya sitasi menjadi konsisten, tetapi metadata dan pedoman kampus tetap perlu diperiksa.',CARD,TX,SC,ON_SC)]):
    x=X0+k*(w2+0.8);box(s,x,4.6,w2,12.6,fill,1.4)
    pic(s,icon(ic,[COOKIE,CLOVER][k],ib,ifg),x+0.9,5.6,3.8,hd)
    tx(s,x+0.9,10.0,w2-1.8,2.6,hd,28,col,True)
    tx(s,x+0.9,13.0,w2-1.8,3.6,bd,20,col)
notes(s,'Jawab kedua rumusan: implementasinya lewat impor, sitasi, dan daftar pustaka otomatis; manfaatnya gaya sitasi konsisten, tetapi metadata dan pedoman kampus tetap perlu diperiksa.')
# 16 penutup
s=frame('')
tx(s,2.0,6.6,18.0,4.0,'Terima kasih',72,TX,True)
pic(s,icon('MdWavingHand',FLOWER,PC,ON_PC),23.0,4.8,8.4,'Ikon penutup')
notes(s,'Tutup dengan terima kasih.')
# --- bangun ---
if n!=TOTAL:raise ValueError(f'jumlah slide {n}, seharusnya {TOTAL}')
json.dump(list(specs.values()),open('specs.json','w'))
subprocess.run(['node','icons.js','specs.json'],check=True)
json.dump(ops,open('ops.json','w'))
if os.path.exists(OUT):os.remove(OUT)
subprocess.run(['officecli','create',OUT],check=True)
r=subprocess.run(['officecli','batch',OUT,'--input','ops.json','--json'],capture_output=True,text=True)
if r.returncode:
    print('STDOUT:',r.stdout);print('STDERR:',r.stderr)
else:
    print(r.stdout[-1500:],r.stderr[-800:])
r.check_returncode()
subprocess.run(['officecli','close',OUT],check=True)
