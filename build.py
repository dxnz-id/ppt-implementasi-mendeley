import json,subprocess,os,hashlib,struct
OUT='deck.pptx'
TOTAL=16
# --- palet editorial Mastercard ---
CREAM,LIFT,SOFT,BONE,DUST='F3F0EE','FCFBFA','F4F4F4','E8E2DA','D1CDC7'
INK,CHAR,SLATE='141413','262627','696969'
ORANGE,ORANGE_L,CLAY,WHITE='CF4500','F37338','9A3A0A','FFFFFF'
BG,CARD,TX,MUT=ORANGE_L,LIFT,INK,SLATE
BODY=CHAR
P,ON_P=INK,CREAM
PC,ON_PC=SOFT,INK
SC,ON_SC=BONE,INK
TC,ON_TC=SOFT,INK
EC,ON_EC=CLAY,CREAM
PILL_PC,PILL_EC=BONE,ORANGE_L
CIRCLE='circle'
F='Arial'
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
def tx(s,x,y,w,h,t,size=18,color=TX,bold=False,align='left',valign='top',name='teks',spacing=0,lineSpacing=None):
    pr=dict(x=cm(x),y=cm(y),width=cm(w),height=cm(h),text=t,size=size,color=color,bold=str(bold).lower(),
        align=align,valign=valign,font=F,fill='none',line='none',margin='0',name=name)
    if spacing:pr['spacing']=str(spacing)
    if lineSpacing:pr['lineSpacing']=lineSpacing
    add(s,'shape',**pr)
def pic(s,f,x,y,w,alt,h=None):add(s,'picture',src=os.path.abspath('assets/'+f),x=cm(x),y=cm(y),width=cm(w),height=cm(h or w),alt=alt)
def clipped(s,f,x,y,w,h,alt):
    with open(os.path.abspath('assets/'+f),'rb') as fh:head=fh.read(24)
    iw,ih=struct.unpack('>II',head[16:24])
    if not abs(iw/ih-w/h)<0.01:raise ValueError(f'{f}: rasio {iw/ih:.3f} tidak cocok dengan kartu {w/h:.3f}; jangan regangkan mask')
    pic(s,f,x,y,w,alt,h)
def shot(s,f,x,y,w,alt,mask='shot-mask-orange.png'):
    h=w*9/16
    clipped(s,f,x,y,w,h,alt)
    pic(s,mask,x,y,w,'Bingkai',h)
    return h
def notes(s,t):add(s,'notes',text=t)
def num(s,x,y,d,t,fill=INK,col=CREAM):
    add(s,'shape',geometry='ellipse',x=cm(x),y=cm(y),width=cm(d),height=cm(d),text=t,size=20,bold='true',color=col,
        align='center',valign='middle',font=F,fill=fill,line='none',margin='0',name='nomor')
def eyebrow(s,x,y,t,w=10,color=INK):
    box(s,x,y+0.18,0.18,0.18,INK,999,name='titik')
    tx(s,x+0.42,y,w,0.55,t.upper(),10,color,True,spacing=0.7,name='eyebrow')
def satellite(s,x,y,d=0.95,size=11):
    box(s,x,y,d,d,WHITE,999,name='satelit')
    tx(s,x,y,d,d,'→',size,INK,True,'center','middle',name='satelit-panah')
def portrait(s,ic,x,y,d,bg=INK,fg=CREAM):
    pic(s,icon(ic,CIRCLE,bg,fg),x,y,d,ic)
    satellite(s,x+d*0.68,y+d*0.68,d*0.34,max(7,int(d*4)))
def orbit(s,f,x,y,w):
    pic(s,f,x,y,w,'Orbit',w*0.30)
def page(s,col=INK):
    box(s,28.95,18.30,0.14,0.14,INK,999,name='titik-halaman')
    tx(s,29.3,18.2,3,0.6,f'{n} / {TOTAL}',9,col,align='right',name='nomor-slide')
def frame(title,eyebrow_text=None,title_color=TX,page_color=INK):
    s=slide(BG)
    if eyebrow_text:eyebrow(s,X0,0.85,eyebrow_text)
    if title:tx(s,X0,1.55,31.2,2.1,title,32,title_color,True,valign='middle',spacing=-0.7,name='judul')
    page(s,page_color)
    return s
X0,W=1.2,31.2

# 1 sampul
s=slide(BG)
orbit(s,'orbit-cream-2.png',15.5,4.4,17.0)
eyebrow(s,X0,2.6,'Bahasa Indonesia',10)
tx(s,X0,3.6,19.2,8.2,'Implementasi Mendeley dalam penulisan karya ilmiah',48,INK,True,spacing=-1.0,lineSpacing='0.95x',name='judul')
box(s,X0,13.4,7.8,1.5,INK,999,name='label')
tx(s,X0,13.4,7.8,1.5,'Mata kuliah Bahasa Indonesia',12,CREAM,True,'center','middle',name='label-teks')
portrait(s,'MdLibraryBooks',23.2,3.0,8.2,INK,CREAM)
notes(s,'Salam pembuka. Perkenalkan topik: cara Mendeley dipakai untuk menyusun kutipan dan daftar pustaka karya ilmiah.')

# 2 anggota
s=slide(BG)
eyebrow(s,X0,0.85,'Kelompok')
tx(s,X0,1.55,31.2,2.1,'Anggota kelompok',32,INK,True,valign='middle',spacing=-0.7,name='judul')
tx(s,X0,3.55,31.2,0.8,'Mata kuliah Bahasa Indonesia',14,BODY)
page(s)
for k,(nm,nim) in enumerate([('Aminadab Yunus','202451028'),('Muhammad Rifqi al Khafis','202551019'),('Arkano Hamada Moslem','202551034'),('Farrel Aufa Athaya Ardiyono','202551042'),("Muhammad La'azidannak Rusda",'202551049'),('Aksel Agustiyan','202551058'),('Muhammad Arief Satria Nugraha','202551151')]):
    x=(X0+k*8.0) if k<4 else (5.335+(k-4)*8.0);y=4.8 if k<4 else 10.8
    box(s,x,y,7.2,5.2,LIFT if k%2==0 else SOFT,1.05)
    tx(s,x+0.6,y+0.45,1.6,1.2,f'{k+1:02d}',28,ORANGE,True,spacing=-1.0)
    tx(s,x+0.6,y+1.7,6.0,2.5,nm,18,INK,True,spacing=-0.2)
    tx(s,x+0.6,y+4.2,6.0,0.7,nim,11,MUT)
notes(s,'Sebutkan anggota kelompok satu per satu sesuai urutan NIM.')

# 3 kekurangan sitasi manual
s=frame('Kekurangan sitasi manual','Latar belakang')
w3=(W-1.6)/3
for k,(ic,hd,bd) in enumerate([('MdFormatAlignLeft','Format berbeda','Gaya sitasi bisa berbeda antarbagian karena diketik satu per satu.'),
 ('MdLinkOff','Sumber terlupa','Kutipan ada di naskah, tetapi rujukannya tidak masuk daftar pustaka.'),
 ('MdCompareArrows','Daftar tidak cocok','Isi daftar pustaka tidak sama dengan sumber yang dikutip di teks.')]):
    x=X0+k*(w3+0.8);box(s,x,4.0,w3,8.0,LIFT,1.05)
    portrait(s,ic,x+0.8,4.8,1.8,INK,CREAM)
    tx(s,x+0.8,7.0,w3-1.6,1.2,hd,20,INK,True,spacing=-0.3)
    tx(s,x+0.8,8.2,w3-1.6,3.2,bd,15,MUT)
box(s,X0,13.0,W,5.0,INK,1.05)
pic(s,icon('MdTimer',CIRCLE,CLAY,CREAM),X0+1.0,14.2,2.2,'Ikon waktu')
tx(s,X0+4.2,13.4,W-5.2,4.2,'Sitasi manual memakan waktu. Sumber yang lupa dicantumkan bisa dianggap plagiarisme.',20,CREAM,False,valign='middle')
notes(s,'Tiga kekurangan sitasi manual: format tidak konsisten, sumber terlupa, dan daftar pustaka tidak cocok dengan teks. Ketiganya berkaitan dengan etika kutipan dan plagiarisme yang kita pelajari di mata kuliah ini.')

# 4 rumusan masalah dan tujuan
s=frame('Rumusan masalah dan tujuan','Arah presentasi')
w2,gap=13.6,0.8
start=X0+(W-(2*w2+gap))/2
for k,(ic,hd,its,pitch,fill,col,ib,ifg,nb,nc) in enumerate([('MdQuestionAnswer','Rumusan masalah',['Bagaimana cara mengimplementasikan Mendeley dalam penulisan karya ilmiah?','Apa manfaat dan keterbatasan Mendeley bagi mahasiswa?'],4.2,LIFT,INK,INK,CREAM,INK,CREAM),
 ('MdFlag','Tujuan',['Menjelaskan fungsi Mendeley.','Menguraikan langkah penggunaannya.','Menilai manfaat dan keterbatasannya.'],2.9,INK,CREAM,CREAM,INK,CREAM,INK)]):
    x=start+k*(w2+gap);box(s,x,4.0,w2,14.0,fill,1.05)
    portrait(s,ic,x+0.9,4.9,2.0,ib,ifg)
    tx(s,x+3.4,4.9,9.0,2.0,hd,24,col,True,valign='middle',spacing=-0.4)
    for j,t in enumerate(its):
        y=8.0+j*pitch;num(s,x+0.9,y,1.2,str(j+1),nb,nc);tx(s,x+2.6,y-0.2,10.4,pitch-0.4,t,17,col,valign='top')
notes(s,'Dua rumusan masalah menuntun presentasi ini: cara implementasi dan manfaat serta keterbatasan. Tiga tujuan mengikuti urutan tersebut: fungsi, langkah, lalu evaluasi.')

# 5 fitur utama
s=frame('Fitur utama','Yang ditawarkan')
feats=[('MdLibraryBooks','Reference Library','Simpan dan kelola referensi.'),
 ('MdPictureAsPdf','PDF Reader','Baca, highlight, dan beri catatan.'),
 ('MdFormatQuote','Mendeley Cite','Sitasi langsung di Microsoft Word.'),
 ('MdCloudSync','Sinkronisasi cloud','Akses dari berbagai perangkat.'),
 ('MdGroup','Groups','Bagikan referensi dengan kolaborator.'),
 ('MdExtension','Web Importer','Simpan referensi dari browser.')]
w3=(W-1.6)/3;rh=6.5
for k,(ic,hd,bd) in enumerate(feats):
    x=X0+(k%3)*(w3+0.8);y=4.0+(k//3)*(rh+0.8)
    portrait(s,ic,x+0.2,y,2.6,INK if k%2==0 else BONE,CREAM if k%2==0 else INK)
    tx(s,x+0.2,y+3.3,w3-0.4,1.2,hd,20,INK,True,spacing=-0.3)
    tx(s,x+0.2,y+4.5,w3-0.4,1.8,bd,15,BODY)
notes(s,'Enam fitur utama Mendeley: Reference Library untuk menyimpan referensi, PDF Reader untuk membaca dan menandai, Mendeley Cite untuk sitasi di Word, sinkronisasi cloud, Groups untuk berbagi, dan Web Importer untuk menyimpan referensi dari browser.')

# 6 instalasi akun dan aplikasi
s=frame('Instalasi: akun dan aplikasi','Instalasi')
shot(s,'shot-account.png',X0,4.0,18.0,'Situs resmi Mendeley')
tx(s,X0,14.3,18.0,0.6,'Situs resmi Mendeley',10,BODY,align='center')
for k,t in enumerate(['Buka situs resmi Mendeley.','Buat akun dengan email atau akun Elsevier.','Unduh Mendeley Reference Manager.','Instal aplikasi, lalu login.']):
    y=4.2+k*3.2;num(s,20.0,y,1.3,str(k+1));tx(s,21.6,y-0.2,10.8,3.0,t,18,INK,valign='top')
notes(s,'Instalasi dimulai dari situs resmi Mendeley. Buat akun dengan email atau akun Elsevier, unduh Reference Manager, lalu instal dan login. Tangkapan layar: Mendeley (n.d.).')

# 7 instalasi web importer dan cite
s=frame('Instalasi: Web Importer dan Cite','Instalasi')
for k,(f,hd,bd) in enumerate([('shot-extension.png','Web Importer','Pasang ekstensi di browser, lalu simpan referensi dari halaman artikel.'),('shot-addin.png','Mendeley Cite','Pasang add-in di Microsoft Word, lalu buka tab References.')]):
    x=X0+k*16.0;shot(s,f,x,4.0,15.2,hd)
    num(s,x,12.9,1.2,str(k+5));tx(s,x+1.7,12.8,13.5,1.2,hd,22,INK,True,spacing=-0.3)
    tx(s,x,14.2,15.2,1.8,bd,15,BODY)
notes(s,'Langkah kelima memasang Web Importer di browser. Langkah keenam memasang Mendeley Cite di Microsoft Word. Tangkapan layar: Mendeley (n.d.).')

# 8 antarmuka
s=frame('Tampilan antarmuka','Antarmuka')
shot(s,'shot-details.png',X0,4.0,19.2,'Antarmuka Mendeley Reference Manager')
tx(s,X0,14.9,19.2,0.6,'Antarmuka Mendeley Reference Manager',10,BODY,align='center')
for k,(hd,bd) in enumerate([('Panel kiri','Koleksi, folder, dan grup.'),('Panel tengah','Daftar referensi.'),('Panel kanan','Detail metadata.')]):
    y=4.2+k*4.2;box(s,21.2,y+0.2,0.18,0.18,INK,999,name='titik');tx(s,21.6,y,9.8,1.0,hd,20,INK,True,spacing=-0.3);tx(s,21.6,y+1.0,9.8,2.2,bd,16,BODY)
notes(s,'Tampilan Reference Manager dibagi tiga panel: koleksi, folder, dan grup di kiri; daftar referensi di tengah; detail metadata di kanan. Tangkapan layar: Mendeley (n.d.).')

# 9 pdf reader
s=frame('PDF Reader: baca dan tandai','Antarmuka')
for k,(f,hd,bd) in enumerate([('shot-highlight.png','Highlight dan anotasi','Tandai bagian penting langsung di PDF.'),('shot-notes.png','Catatan','Tulis ringkasan atau komentar per referensi.')]):
    x=X0+k*16.0;shot(s,f,x,4.0,15.2,hd)
    tx(s,x,12.9,15.2,1.2,hd,22,INK,True,spacing=-0.3)
    tx(s,x,14.2,15.2,1.8,bd,15,BODY)
notes(s,'PDF Reader terintegrasi dengan Reference Manager. Bagian penting bisa di-highlight, diberi anotasi, atau dicatat di Notebook. Tangkapan layar: Mendeley (n.d.).')

# 10 menambahkan referensi
s=frame('Menambahkan referensi','Referensi')
shot(s,'shot-rm-add.png',X0,4.0,18.0,'Menu Add reference')
tx(s,X0,14.3,18.0,0.6,'Menu Add reference',10,BODY,align='center')
for k,(ic,hd,bd) in enumerate([('MdUploadFile','Unggah PDF','Tarik file ke Library.'),('MdExtension','Web Importer','Simpan dari halaman artikel.'),('MdEdit','Input manual','Isi DOI, ISBN, atau PMID.'),('MdFileUpload','Impor file','RIS, BibTeX, EndNote XML.')]):
    y=4.2+k*3.2;portrait(s,ic,20.0,y,1.5,INK if k%2==0 else BONE,CREAM if k%2==0 else INK)
    tx(s,21.8,y-0.2,10.6,1.0,hd,20,INK,True,spacing=-0.3);tx(s,21.8,y+0.9,10.6,2.0,bd,15,BODY)
notes(s,'Referensi bisa masuk lewat unggahan PDF, Web Importer, input manual DOI/ISBN/PMID, atau impor RIS, BibTeX, dan EndNote XML. Tangkapan layar menu Add reference: Mendeley (n.d.).')

# 11 mendeley cite
s=frame('Mendeley Cite di Word','Cite')
shot(s,'shot-addin.png',X0,4.0,14.0,'Mendeley Cite di Microsoft Word')
tx(s,X0,12.2,14.0,0.6,'Mendeley Cite di Microsoft Word',10,BODY,align='center')
box(s,X0,13.2,14.0,4.2,INK,1.05)
tx(s,X0+0.9,13.2,12.2,4.2,'Gaya sitasi bisa diganti tanpa menulis ulang.',17,CREAM,False,valign='middle')
for k,t in enumerate(['Buka Microsoft Word, lalu tab References.','Klik Mendeley Cite.','Pilih referensi dari pustaka.','Klik Insert Citation.','Pilih gaya sitasi.','Klik Insert Bibliography.']):
    y=4.2+k*2.2;num(s,16.0,y,1.2,str(k+1));tx(s,17.4,y-0.1,14.6,2.0,t,16,INK,valign='top')
notes(s,'Di Word, buka tab References lalu Mendeley Cite. Pilih referensi, klik Insert Citation, tentukan gaya, lalu Insert Bibliography. Gaya bisa diganti kapan saja. Tangkapan layar: Mendeley Support (2025).')

# 12 gaya sitasi
s=frame('Gaya sitasi','Referensi')
box(s,X0,4.0,W,1.2,INK,999,name='header')
tx(s,X0+1.0,4.0,6.0,1.2,'Gaya',14,CREAM,True,valign='middle',spacing=0.3)
tx(s,X0+8.0,4.0,22.0,1.2,'Contoh bidang',14,CREAM,True,valign='middle',spacing=0.3)
for k,(style,field) in enumerate([('APA','Psikologi, pendidikan, sosial'),('IEEE','Teknik, informatika'),('Harvard','Bisnis, manajemen'),('Chicago','Humaniora, sejarah'),('Vancouver','Kedokteran, kesehatan')]):
    y=5.5+k*2.3;box(s,X0,y,W,2.1,[LIFT,SOFT][k%2],999,name='baris')
    tx(s,X0+1.0,y,6.0,2.1,style,18,INK,True,valign='middle',spacing=-0.2)
    tx(s,X0+8.0,y,22.0,2.1,field,17,MUT,valign='middle')
tx(s,X0,17.0,W,0.8,'Gaya dapat diganti kapan saja tanpa menulis ulang.',12,BODY)
notes(s,'Lima gaya yang umum: APA untuk psikologi, pendidikan, dan sosial; IEEE untuk teknik dan informatika; Harvard untuk bisnis dan manajemen; Chicago untuk humaniora dan sejarah; Vancouver untuk kedokteran dan kesehatan. Gaya bisa diganti kapan saja.')

# 13 satu sumber dua keluaran
s=frame('Satu sumber untuk dua rujukan','Alur')
tx(s,X0,3.3,W,0.8,'Metadata yang sama menjadi bahan sitasi dan daftar pustaka.',14,BODY)
wL,wR=12.0,18.4
box(s,X0,4.2,wL,13.2,LIFT,1.05)
tx(s,X0+0.8,4.8,wL-1.6,0.7,'Satu sumber',11,ORANGE,True,spacing=0.5)
shot(s,'shot-source.png',X0+1.2,5.6,9.6,'PDF jurnal dan metadata',mask='shot-mask.png')
tx(s,X0+0.8,11.2,wL-1.6,0.8,'PDF jurnal dan metadata',15,INK,True)
tx(s,X0+0.8,12.0,wL-1.6,3.2,'Penulis, tahun, judul, dan DOI dipakai untuk keduanya.',15,MUT)
xR=X0+wL+0.8
for k,(f,hd,bd,fill) in enumerate([('shot-citation.png','Sitasi dalam teks','Mendeley Cite menyisipkan sitasi ke dalam kalimat.',SOFT),('shot-bib-menu.png','Daftar pustaka','Mendeley menyusun entri lengkap dari metadata yang sama.',LIFT)]):
    y=4.2+k*6.9;box(s,xR,y,wR,6.3,fill,1.05)
    tx(s,xR+0.8,y+0.5,wR-1.6,0.7,hd,11,ORANGE,True,spacing=0.5)
    shot(s,f,xR+0.8,y+1.3,7.2,hd,mask='shot-mask.png')
    tx(s,xR+8.4,y+1.5,wR-9.2,2.6,bd,16,INK)
    tx(s,X0+wL+0.05,7.0 if k==0 else 13.9,0.7,1.1,'→',20,INK,True,'center','middle')
notes(s,'Satu referensi di Library menjadi sumber untuk sitasi di Word dan entri daftar pustaka. Tangkapan layar menunjukkan panel Cite dan menu Insert Bibliography; teori gaya sitasi tetap di Kelompok 4. Tangkapan layar: Mendeley Support (2025).')

# 14 kelebihan keterbatasan
s=frame('Kelebihan dan keterbatasan','Evaluasi')
for k,(ic,hd,its,fill,col,sh,fg,pill,pcol) in enumerate([('MdCheckCircle','Kelebihan',['Hemat waktu','Gaya sitasi konsisten','Kutipan dan daftar pustaka sinkron','Penyimpanan dan sinkronisasi lintas perangkat'],LIFT,INK,INK,CREAM,SOFT,INK),('MdWarning','Keterbatasan',['Metadata hasil impor perlu diperiksa','Gaya sitasi khusus kampus perlu ditambahkan manual','Penyimpanan gratis hanya 2 GB','PDF hasil pindai biasanya masuk tanpa metadata'],INK,CREAM,ORANGE_L,INK,CHAR,CREAM)]):
    w2=(W-0.8)/2;x=X0+k*(w2+0.8);box(s,x,4.0,w2,14.0,fill,1.05)
    portrait(s,ic,x+0.9,4.8,2.2,sh,fg);tx(s,x+3.6,4.8,w2-4.2,2.2,hd,24,col,True,valign='middle',spacing=-0.4)
    for j,t in enumerate(its):
        y=7.7+j*2.5;box(s,x+0.8,y,w2-1.6,1.9,pill,999,name='kapsul');tx(s,x+1.4,y,w2-2.4,1.9,t,15,pcol,valign='middle')
notes(s,'Kelebihan: hemat waktu, gaya sitasi konsisten, dan sinkron. Keterbatasannya: metadata hasil impor perlu diperiksa, gaya sitasi khusus kampus perlu ditambahkan manual, penyimpanan gratis hanya 2 GB, dan PDF hasil pindai biasanya masuk tanpa metadata.')

# 15 kesimpulan
s=frame('Kesimpulan','Penutup')
w2=(W-0.8)/2
for k,(ic,hd,bd,fill,col,ib,ifg) in enumerate([('MdCheckCircle','Implementasinya','Impor referensi, sisipkan sitasi di Word, lalu buat daftar pustaka otomatis.',INK,CREAM,ORANGE_L,INK),('MdSchool','Manfaat dan batasannya','Gaya sitasi menjadi konsisten, tetapi metadata dan pedoman kampus tetap perlu diperiksa.',LIFT,INK,INK,CREAM)]):
    x=X0+k*(w2+0.8);box(s,x,4.0,w2,14.0,fill,1.05)
    portrait(s,ic,x+0.9,5.0,2.4,ib,ifg)
    tx(s,x+0.9,9.8,w2-1.8,2.6,hd,26,col,True,spacing=-0.4)
    tx(s,x+0.9,12.8,w2-1.8,3.8,bd,17,col)
notes(s,'Jawab kedua rumusan: implementasinya lewat impor, sitasi, dan daftar pustaka otomatis; manfaatnya gaya sitasi konsisten, tetapi metadata dan pedoman kampus tetap perlu diperiksa.')

# 16 penutup
s=slide(BG)
orbit(s,'orbit-cream-1.png',13.5,4.8,17.0)
eyebrow(s,X0,1.0,'Penutup',10)
tx(s,2.0,6.0,20.0,4.0,'Terima kasih',64,INK,True,spacing=-1.2)
portrait(s,'MdWavingHand',23.0,4.2,8.4,CREAM,INK)
tx(s,2.0,14.0,20.0,0.8,'Mata kuliah Bahasa Indonesia',14,BODY)
box(s,28.95,18.30,0.14,0.14,INK,999,name='titik-halaman')
tx(s,29.3,18.2,3,0.6,f'{n} / {TOTAL}',9,INK,align='right',name='nomor-slide')
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
