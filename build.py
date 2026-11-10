import json,subprocess,os,hashlib,struct,sys
OUT='deck.pptx'
TOTAL=16
# --- palet M3 Expressive dari #B0C8E0 #C1E0E0 #DCE7D6 #F6F6F6 ---
BG,RAIL,CARD='F6F6F6','ECEEEE','E6E9E9'
TX,MUT='2F3334','5B6061'
P,ON_P,PC,ON_PC='46627A','F6F9FF','B0C8E0','355169'
SC,ON_SC='C1E0E0','3D6060'
TC,ON_TC='DCE7D6','536350'
EC,ON_EC='FFDAD6','65000B'
PILL_PC,PILL_EC='C9DBEC','F7C7C1'
COOKIE,FLOWER,CLOVER,SQUIRCLE,BURST,SUNNY='cookie','flower','clover','squircle','burst','sunny'
F='Calibri'
ops=[];specs={};n=0
counts={};shape_counts={};sidebar_shapes={};content_start={};sidebar_end={};pill_idx={};pill_top={}
def cm(v):return f'{v:.2f}cm'
def icon(name,shape,bg,fg):
    f=hashlib.md5(f'{name}{shape}{bg}{fg}'.encode()).hexdigest()[:10]+'.png'
    specs[f]=dict(file=f,icon=name,shape=shape,bg=bg,fg=fg);return f
def emit(parent,typ,props):ops.append(dict(command='add',parent=parent,type=typ,props={k:str(v) for k,v in props.items()}))
def add(parent,typ,**p):
    emit(parent,typ,p)
    if typ in ('shape','picture','chart','group'):counts[parent]=counts.get(parent,0)+1
    if typ=='shape':shape_counts[parent]=shape_counts.get(parent,0)+1
    return counts.get(parent)
def slide(bg):
    global n;n+=1;add('/','slide',background=bg);s=f'/slide[{n}]';counts[s]=0;shape_counts[s]=0;content_start[s]=1;return s
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
    assert abs(iw/ih-w/h)<0.01,f'{f}: rasio {iw/ih:.3f} tidak cocok dengan kartu {w/h:.3f}; jangan regangkan mask'
    pic(s,f,x,y,w,alt,h)
def notes(s,t):add(s,'notes',text=t)
def num(s,x,y,d,t,fill,col):
    add(s,'shape',geometry='ellipse',x=cm(x),y=cm(y),width=cm(d),height=cm(d),text=t,size=20,bold='true',color=col,
        align='center',valign='middle',font=F,fill=fill,line='none',margin='0',name='nomor')
SECT=[('MdMenuBook','Latar'),('MdLibraryBooks','Mengenal'),('MdBuild','Praktik'),('MdBalance','Evaluasi'),('MdFlag','Penutup')]
def page(s):tx(s,29.4,18.2,3,0.6,f'{n} / {TOTAL}',10,MUT,align='right',name='nomor-slide')
def frame(sec,title):
    s=slide(BG);box(s,1.0,1.0,2.8,17.05,RAIL,1.2,name='rail')
    pic(s,icon('MdLibraryBooks',COOKIE,P,'FFFFFF'),1.7,1.6,1.4,'Logo bagian')
    for k,(ic,lab) in enumerate(SECT):
        y=3.5+k*2.9;on=k==sec
        if on:
            pill_top[s]=counts[s]+1  # posisi top-level untuk grouping
            pill_idx[s]=shape_counts[s]+1  # posisi shape untuk AddAnimation
            box(s,1.3,y,2.2,2.6,PC,1.1,name=f'#s{n}-rail-pill')
        pic(s,icon(ic,'none','x',ON_PC if on else MUT),1.9,y+0.35,1.0,lab)
        tx(s,1.3,y+1.6,2.2,0.7,lab,12,ON_PC if on else MUT,on,'center','middle','rail-label')
    sidebar_end[s]=counts[s]
    sidebar_shapes[s]=shape_counts[s]
    content_start[s]=counts[s]+1
    tx(s,4.4,1.2,28,2.4,title,36,TX,True,valign='middle',name='judul')
    page(s)
    return s
X0,W=4.4,28.0
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
box(s,2.0,3.0,8.4,1.6,PC,0.8,name='label');tx(s,2.0,3.0,8.4,1.6,'Bahasa Indonesia',18,ON_PC,True,'center','middle')
tx(s,2.0,4.4,18,7.8,'Implementasi aplikasi Mendeley dalam penulisan karya ilmiah',44,TX,True,name='judul')
tx(s,2.0,13.4,18,1,'Mata kuliah Bahasa Indonesia',20,P,True)
notes(s,'Salam pembuka. Perkenalkan topik: cara Mendeley dipakai untuk menyusun kutipan dan daftar pustaka karya ilmiah.')
# 2 anggota
s=slide(BG)
tx(s,2.0,1.4,28,2.4,'Anggota kelompok',40,TX,True,valign='middle',name='judul')
tx(s,2.0,3.6,28,1,'Mata kuliah Bahasa Indonesia',18,P,True)
for k,(nm,nim) in enumerate([('Aminadab Yunus','202451028'),('Muhammad Rifqi al Khafis','202551019'),('Arkano Hamada Moslem','202551034'),('Farrel Aufa Athaya Ardiyono','202551042'),("Muhammad La'azidannak Rusda",'202551049'),('Aksel Agustiyan','202551058'),('Muhammad Arief Satria Nugraha','202551151')]):
    x=(2.0+k*7.3) if k<4 else (5.65+(k-4)*7.3);y=5.2 if k<4 else 11.0
    fill=[PC,CARD,TC,CARD,PC,CARD,CARD][k];col=[ON_PC,TX,ON_TC,TX,ON_PC,TX,TX][k]
    box(s,x,y,6.8,5.2,fill,1.2)
    clipped(s,f'num-{k+1:02d}.png',x+0.05,y+0.04,6.7,5.12,'Nomor '+f'{k+1:02d}')
    tx(s,x+0.6,y+1.3,5.6,2.4,nm,18,col,True)
    tx(s,x+0.6,y+3.8,5.6,1.2,nim,12,col)
page(s)
notes(s,'Sebutkan anggota kelompok satu per satu sesuai urutan NIM.')
# 3 latar belakang
s=frame(0,'Sitasi manual rawan salah dan lambat')
card3(s,4.0,8.2,[('MdFormatAlignLeft','Format berbeda','Gaya sitasi berbeda antarparagraf karena diketik satu per satu.'),
 ('MdLinkOff','Sumber terlupa','Kutipan ada di naskah, tetapi rujukannya tidak masuk daftar pustaka.'),
 ('MdCompareArrows','Daftar tak cocok','Isi daftar pustaka tidak sama dengan sumber yang dikutip di teks.')],[(CARD,PC,ON_PC,TX)]*3)
box(s,X0,13.0,W,5.0,PC,1.4)
pic(s,icon('MdTimer',SUNNY,P,'FFFFFF'),X0+1.0,14.2,2.6,'Ikon waktu')
tx(s,X0+4.4,13.4,W-5.4,4.2,'Menulis kutipan dan daftar pustaka secara manual menyita waktu. Sumber yang tidak tercantum dapat dinilai sebagai plagiarisme, sehingga kesalahan kecil pun berisiko.',22,ON_PC,False,valign='middle')
notes(s,'Mahasiswa sering salah pada tiga hal: format kutipan tidak seragam, sumber lupa dicantumkan, dan daftar pustaka tidak cocok dengan isi. Semua itu berkaitan dengan etika kutipan dan plagiarisme yang kita pelajari di mata kuliah ini.')
# 4 rumusan
s=frame(0,'Rumusan masalah dan tujuan')
for k,(ic,hd,its,pitch,fill,col,nb,nc) in enumerate([('MdQuestionAnswer','Rumusan masalah',['Bagaimana Mendeley diimplementasikan dalam penulisan karya ilmiah?','Apa manfaat dan keterbatasan Mendeley bagi mahasiswa?'],4.2,CARD,TX,P,'FFFFFF'),
 ('MdFlag','Tujuan',['Menjelaskan fungsi Mendeley.','Menguraikan langkah penggunaannya.','Menilai manfaat dan keterbatasannya.'],2.9,TC,ON_TC,ON_TC,'FFFFFF')]):
    x=X0+k*14.4;box(s,x,4.0,13.6,14.0,fill,1.4)
    clipped(s,'mask-04-tanya.png' if k==0 else 'mask-04-tujuan.png',x,4.0,13.6,14.0,'Masking tanda')
    pic(s,icon(ic,[COOKIE,CLOVER][k],PC if k==0 else SC,ON_PC if k==0 else ON_TC),x+0.9,4.9,2.2,hd)
    tx(s,x+3.6,4.9,9,2.2,hd,24,col,True,valign='middle')
    for j,t in enumerate(its):
        y=8.2+j*pitch;num(s,x+0.9,y,1.5,str(j+1),nb,nc);tx(s,x+3.0,y-0.2,10,pitch-0.4,t,20,col,valign='top')
notes(s,'Dua rumusan masalah menuntun presentasi ini: cara implementasi dan manfaat serta keterbatasan. Tiga tujuan mengikuti urutan tersebut: fungsi, langkah, lalu evaluasi.')
# 5 mengenal
s=frame(1,'Tiga komponen utama Mendeley')
box(s,X0,4.0,10.0,14.0,PC,1.4)
clipped(s,'mask-05-tiga.png',X0,4.0,10.0,14.0,'Masking angka tiga')
pic(s,icon('MdLibraryBooks',FLOWER,P,'FFFFFF'),X0+1.2,4.9,3.6,'Ikon Mendeley')
tx(s,X0+1.0,9.4,8,5.6,'Mendeley adalah aplikasi pengelola referensi dan jejaring akademik. Elsevier mengembangkannya.',22,ON_PC,True)
tx(s,X0+1.0,15.0,8,2.6,'Pengembangan Mendeley Desktop dihentikan; Reference Manager menjadi fokus.',16,ON_PC)
for k,(ic,hd,bd) in enumerate([('MdLibraryBooks','Mendeley Reference Manager','Pustaka pribadi untuk menyimpan, mengelompokkan, dan menganotasi PDF jurnal.'),
 ('MdDescription','Mendeley Cite','Add-in Microsoft Word untuk menyisipkan kutipan dan membuat daftar pustaka.'),
 ('MdExtension','Web Importer','Ekstensi peramban untuk menyimpan referensi dari halaman web.')]):
    y=4.0+k*4.9;box(s,X0+10.8,y,17.2,4.2,CARD,1.2)
    pic(s,icon(ic,[COOKIE,CLOVER,SQUIRCLE][k],SC,ON_SC),X0+11.5,y+0.8,2.6,hd)
    tx(s,X0+14.8,y+0.6,12.6,1.2,hd,24,TX,True);tx(s,X0+14.8,y+1.8,12.6,2.3,bd,18,MUT)
tx(s,X0,18.3,20,0.5,'Sumber: Mendeley (n.d.); Mendeley Support (2025).',10,MUT)
notes(s,'Mendeley dikembangkan Elsevier. Ada tiga komponen: Reference Manager untuk pustaka, Mendeley Cite untuk Word, dan Web Importer untuk peramban. Mendeley Desktop masih tersedia, tetapi pengembangannya sudah dihentikan; Reference Manager menjadi fokus.')
# 6 apa yang diolah
s=frame(1,'Apa yang diolah Mendeley')
box(s,X0,4.0,W,4.6,P,1.4)
pic(s,icon('MdDescription',SQUIRCLE,PC,ON_PC),X0+1.0,5.0,2.6,'Ikon metadata')
tx(s,X0+4.4,4.0,W-5.4,4.6,'Mendeley memindahkan metadata referensi ke sitasi dan daftar pustaka. Isi dan ketepatan data tetap diperiksa penulis.',24,'FFFFFF',True,valign='middle')
card3(s,9.4,8.6,[('MdDescription','Metadata','Judul, penulis, tahun, DOI, dan nama jurnal menjadi bahan sitasi.'),
 ('MdStyle','Gaya sitasi','Mendeley menerapkan gaya yang dipilih, misalnya APA atau IEEE.'),
 ('MdListAlt','Daftar pustaka','Entri disusun otomatis dari metadata dan gaya yang sama.')],[(CARD,SC,ON_SC,TX),(CARD,TC,ON_TC,TX),(CARD,PC,ON_PC,TX)])
tx(s,X0,18.3,20,0.5,'Sumber: Mendeley Support (2025).',10,MUT)
notes(s,'Mendeley mengolah metadata menjadi sitasi dan daftar pustaka. Jenis kutipan dan aturan tiap gaya dibahas Kelompok 4; fokus kita pada data yang diolah dan hasil yang dibuat Mendeley.')
# 7 satu sumber dua keluaran
s=frame(1,'Satu sumber, dua keluaran')
tx(s,X0,3.3,W,0.9,'Metadata yang sama dipakai untuk sitasi dan daftar pustaka.',18,MUT)
w3=(W-1.6)/3
for k,(hd,bd,fill,col) in enumerate([('01 Metadata','Judul, penulis, tahun, dan sumber.',CARD,TX),
 ('02 Sitasi','Mendeley Cite menyisipkan sitasi ke naskah.',SC,ON_SC),
 ('03 Daftar pustaka','Entri tersusun dari metadata yang sama.',TC,ON_TC)]):
    x=X0+k*(w3+0.8);box(s,x,4.6,w3,5.6,fill,1.3)
    tx(s,x+0.8,5.2,w3-1.6,2.05,hd,24,col,True)
    tx(s,x+0.8,6.6,w3-1.6,3.6,bd,18,col)
    if k<2:pic(s,icon('MdArrowForward','none','x',P),x+w3+0.1,7.1,0.6,'Panah')
box(s,X0,11.6,W,4.4,PC,1.4)
pic(s,icon('MdFactCheck',BURST,P,'FFFFFF'),X0+1.0,12.4,2.4,'Ikon pemeriksaan')
tx(s,X0+4.0,12.0,W-5.0,3.6,'Yang tetap manual: periksa metadata dan pastikan gaya sitasi sesuai pedoman. Teori jenis sitasi dibahas Kelompok 4.',20,ON_PC,False,valign='middle')
tx(s,X0,17.2,28,0.7,'Sumber: Mendeley Support (2025).',10,MUT)
notes(s,'Satu referensi menghasilkan sitasi dalam teks dan entri daftar pustaka. Mendeley memakai metadata yang sama. Teori jenis sitasi dan aturan APA/IEEE tidak dibahas di sini; itu materi Kelompok 4.')
# 8 persiapan
s=frame(2,'Persiapan: akun, aplikasi, dan add-in')
w3=(W-1.6)/3
for k,(ic,hd,bd) in enumerate([('MdPersonAdd','Buat akun','Daftar dengan email aktif.'),('MdDownload','Pasang aplikasi','Unduh Reference Manager, lalu pasang add-in Mendeley Cite di Word.'),('MdExtension','Pasang ekstensi','Tambahkan Web Importer ke peramban untuk menyimpan referensi dari web.')]):
    x=X0+k*(w3+0.8);box(s,x,4.2,w3,12.6,[CARD,SC,TC][k],1.4)
    clipped(s,f'mask-08-{k+1:02d}.png',x,4.2,w3,12.6,'Masking angka langkah')
    pic(s,icon(ic,[SUNNY,CLOVER,SQUIRCLE][k],PC,ON_PC),x+w3-5.4,4.8,4.6,hd)
    tx(s,x+0.9,10.4,w3-1.8,1.4,hd,24,[TX,ON_SC,TX][k],True);tx(s,x+0.9,12.2,w3-1.8,4.6,bd,20,[MUT,ON_SC,MUT][k])
tx(s,X0,18.3,20,0.5,'Sumber: Mendeley (n.d.).',10,MUT)
notes(s,'Tiga persiapan: membuat akun dengan email aktif, memasang Reference Manager dan add-in Mendeley Cite di Word, lalu memasang Web Importer di peramban.')
# 9 langkah 1
s=frame(2,'Langkah 1: kumpulkan referensi')
for k,(ic,hd,bd) in enumerate([('MdUploadFile','Impor PDF','Tambahkan PDF jurnal ke Library.'),('MdLanguage','Simpan dari web','Gunakan Web Importer pada halaman artikel.'),('MdFactCheck','Periksa metadata','Cek judul, penulis, tahun, dan DOI; koreksi yang salah.'),('MdFolder','Rapikan','Kelompokkan dengan folder dan tag per bab atau topik.')]):
    x=X0+(k%2)*14.4;y=4.0+(k//2)*7.4;box(s,x,y,13.6,6.6,[CARD,SC,TC,CARD][k],1.3)
    pic(s,icon(ic,[COOKIE,CLOVER,BURST,SQUIRCLE][k],[PC,P,SC,SC][k],[ON_PC,'FFFFFF',ON_TC,ON_SC][k]),x+0.9,y+1.6,3.4,hd)
    tx(s,x+5.0,y+1.2,8.0,1.3,hd,24,TX,True);tx(s,x+5.0,y+2.7,8.0,3.4,bd,19,MUT)
notes(s,'Mulai dari mengumpulkan sumber. Metadata hasil impor sering keliru, jadi periksa judul, penulis, tahun, dan DOI satu per satu. Folder dan tag per bab memudahkan pencarian saat menulis.')
# 10 langkah 2
s=frame(2,'Langkah 2: baca dan catat')
box(s,X0,4.0,17.6,14.0,CARD,1.4)
for k,(ic,hd,bd) in enumerate([('MdBorderColor','Highlight dan anotasi','Tandai bagian penting langsung pada PDF.'),('MdStickyNote2','Catatan per referensi','Tulis ide utama dengan kata sendiri sebelum menulis naskah.')]):
    y=4.9+k*6.6;pic(s,icon(ic,[CLOVER,SQUIRCLE][k],SC,ON_SC),X0+1.0,y+0.6,3.6,hd)
    tx(s,X0+5.4,y+0.6,11.2,1.4,hd,24,TX,True);tx(s,X0+5.4,y+2.2,11.2,3.4,bd,20,MUT)
box(s,X0+18.4,4.0,9.6,14.0,TC,1.4)
clipped(s,'mask-10-panah.png',X0+18.4,4.0,9.6,14.0,'Masking panah hasil')
pic(s,icon('MdLightbulb',SUNNY,SC,ON_TC),X0+19.6,5.2,4.2,'Ikon ide')
tx(s,X0+19.4,10.6,7.6,1.4,'Hasilnya',24,ON_TC,True);tx(s,X0+19.4,12.2,7.6,5,'Bahan parafrasa untuk menyusun kutipan tidak langsung.',22,ON_TC)
notes(s,'Anotasi dan catatan membantu kita memahami sumber lebih dulu. Dari catatan itulah kutipan tidak langsung ditulis ulang dengan kalimat sendiri, lengkap dengan sitasinya.')
# 11 langkah 3
s=frame(2,'Langkah 3: sisipkan kutipan di Word')
w4=(W-3*1.6)/4
for k,(ic,hd,bd) in enumerate([('MdDescription','Buka add-in','Buka Mendeley Cite di Microsoft Word.'),('MdFormatQuote','Sisipkan kutipan','Pilih referensi, lalu tempatkan pada kalimat.'),('MdStyle','Pilih gaya','Sesuaikan dengan pedoman kampus.'),('MdListAlt','Buat daftar pustaka','Daftar pustaka tersusun otomatis.')]):
    x=X0+k*(w4+1.6);box(s,x,4.4,w4,13.0,[CARD,SC,TC,PC][k],1.3)
    num(s,x+0.7,5.1,1.5,str(k+1),P,'FFFFFF')
    pic(s,icon(ic,[COOKIE,CLOVER,SQUIRCLE,BURST][k],[PC,P,SC,P][k],[ON_PC,'FFFFFF',ON_TC,'FFFFFF'][k]),x+0.7,7.2,3.4,hd)
    tx(s,x+0.7,11.0,w4-1.4,2.4,hd,22,TX,True);tx(s,x+0.7,13.6,w4-1.4,3.4,bd,18,MUT)
    if k<3:pic(s,icon('MdArrowForward','none','x',P),x+w4+0.3,10.2,1.0,'Panah')
notes(s,'Alurnya empat langkah di Word: buka Mendeley Cite, sisipkan kutipan, pilih gaya sesuai pedoman kampus, lalu buat daftar pustaka. Daftar pustaka ikut berubah otomatis saat kutipan ditambah atau dihapus.')
# 12 demo
s=frame(2,'Demo alur: impor sampai daftar pustaka')
tx(s,X0,3.4,W,1.55,'Dua tahap: rapikan referensi di Library, lalu sisipkan sitasi sampai daftar pustaka.',18,MUT)
for k,lab in enumerate(['Library','Mendeley Cite']):
    x=X0+k*14.4;y=4.6;fill=PC if k==0 else SC;col=ON_PC if k==0 else ON_SC
    box(s,x,y,13.6,12.4,fill,1.4)
    if k==0:
        pic(s,'img-library-fade.png',x+0.6,y+0.6,12.4,'Ilustrasi Library',6.97)
        box(s,x+0.6,y+8.0,3.6,1.0,CARD,0.55,name='label');tx(s,x+0.6,y+8.0,3.6,1.0,lab,14,col,True,'center','middle')
        tx(s,x+0.6,y+9.2,12.4,2.0,'Impor PDF, kelompokkan, dan rapikan metadata referensi.',16,col)
    else:
        tx(s,x+0.6,y+0.9,6.8,1.2,'Mendeley Cite',24,col,True)
        tx(s,x+0.6,y+2.2,6.8,4.0,'Sisipkan kutipan, pilih satu gaya, lalu buat daftar pustaka dari Word.',16,col)
        box(s,x+0.6,y+6.6,5.4,1.0,CARD,0.55,name='label');tx(s,x+0.6,y+6.6,5.4,1.0,'Insert Bibliography',12,col,True,'center','middle')
        tx(s,x+0.6,y+7.9,6.8,2.2,'Klik More, lalu pilih Insert Bibliography.',14,col)
        pic(s,'img-cite-panel.png',x+7.7,y+1.75,5.4,'Ilustrasi Mendeley Cite',7.45)
    tx(s,x+0.6,y+11.3,12.4,0.7,'Sumber: mendeley.com',10,col)
notes(s,'Peragakan alur: impor ke Library, cek metadata, sisipkan kutipan di Word, pilih gaya, lalu buat daftar pustaka. Gambar adalah ilustrasi dari aset resmi Mendeley (mendeley.com); ganti dengan tangkapan layar sendiri bila sudah mencoba alurnya.')
# 13 kelebihan keterbatasan
s=frame(3,'Kelebihan dan keterbatasan')
for k,(ic,hd,its,fill,col,sh,fg) in enumerate([('MdCheckCircle','Kelebihan',['Hemat waktu','Format konsisten','Kutipan dan daftar pustaka sinkron','Penyimpanan dan sinkronisasi antarperangkat'],PC,ON_PC,P,'FFFFFF'),
 ('MdWarning','Keterbatasan',['Metadata impor perlu dicek manual','Gaya sitasi kampus tertentu mungkin tidak tersedia','Penyimpanan gratis 2 GB','Kesalahan tetap menjadi tanggung jawab penulis'],EC,ON_EC,'F56965','FFFFFF')]):
    x=X0+k*14.4;box(s,x,4.0,13.6,14.0,fill,1.4)
    pic(s,icon(ic,[CLOVER,BURST][k],sh,fg),x+0.9,4.8,2.2,hd);tx(s,x+3.6,4.8,9.4,2.2,hd,24,col,True,valign='middle')
    pill=PILL_PC if k==0 else PILL_EC
    for j,t in enumerate(its):
        y=7.7+j*2.5
        box(s,x+0.8,y,12.0,1.9,pill,0.95,name='kapsul')
        tx(s,x+1.4,y,11.2,1.9,t,16,col,valign='middle')
tx(s,X0,18.3,20,0.5,'Sumber: Mendeley Support (2025).',10,MUT)
notes(s,'Kelebihan: hemat waktu, format konsisten, dan sinkron. Keterbatasannya: metadata perlu dicek, gaya sitasi kampus tertentu mungkin tidak tersedia, penyimpanan gratis 2 GB, dan kesalahan tetap menjadi tanggung jawab penulis.')
# 14 kesimpulan (terang)
s=slide(BG);tx(s,2.0,1.4,30,2.4,'Kesimpulan dan saran',40,TX,True,valign='middle',name='judul')
w3=9.6
for k,(ic,hd,bd) in enumerate([('MdCheckCircle','Implementasinya','Impor referensi, sisipkan sitasi di Word, lalu buat daftar pustaka otomatis.'),('MdSchool','Manfaat dan batasannya','Format menjadi konsisten, tetapi metadata dan kaidah tetap harus diperiksa.'),('MdFlag','Saran','Mulai dari tugas kecil, cek metadata, dan gunakan satu gaya sitasi.')]):
    x=2.0+k*10.4;box(s,x,4.6,w3,12.6,[PC,CARD,TC][k],1.4)
    clipped(s,f'mask-14-{k+1:02d}.png',x,4.6,w3,12.6,'Masking angka kesimpulan')
    pic(s,icon(ic,[COOKIE,CLOVER,SQUIRCLE][k],[P,SC,ON_TC][k],[ON_P,ON_SC,TC][k]),x+0.9,5.6,3.4,hd)
    tx(s,x+0.9,9.8,w3-1.8,2.8,hd,24,[ON_PC,TX,ON_TC][k],True);tx(s,x+0.9,12.8,w3-1.8,4.2,bd,18,[ON_PC,TX,ON_TC][k])
page(s)
notes(s,'Jawab kedua rumusan: implementasinya lewat impor, sitasi, dan daftar pustaka otomatis; manfaatnya format konsisten, tetapi metadata dan kaidah tetap harus diperiksa. Sarankan mulai dari tugas kecil dan satu gaya sitasi.')
# 15 pustaka
s=frame(4,'Daftar pustaka')
refs=[
 'Badan Pengembangan dan Pembinaan Bahasa. (n.d.). Parafrasa. KBBI VI Daring. https://kbbi.kemendikdasmen.go.id/entri/parafrasa',
 'Elsevier. (n.d.). Mendeley Reference Manager. https://www.mendeley.com/reference-management/reference-manager',
 'Elsevier. (n.d.). Mendeley Cite. https://www.mendeley.com/reference-management/mendeley-cite/',
 'Elsevier. (n.d.). Mendeley Web Importer. https://www.mendeley.com/reference-management/web-importer',
 'Elsevier Support. (2025). What do I get with a free Mendeley account? https://www.elsevier.support/mendeley/answer/what-do-i-get-with-a-free-mendeley-account',
 'Elsevier Support. (2025). What is Mendeley Reference Manager? https://www.elsevier.support/mendeley/answer/what-is-mendeley-reference-manager',
 'American Psychological Association. (2020). Publication manual of the American Psychological Association (7th ed.). https://doi.org/10.1037/0000165-000',
 'IEEE. (2024). IEEE editorial style manual for authors. https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE-Editorial-Style-Manual-for-Authors.pdf']
for k,t in enumerate(refs):
    x=X0+(k%2)*14.4;y=4.2+(k//2)*3.0
    fill=[CARD,SC,TC,PC][k%4];col=[TX,ON_SC,ON_TC,ON_PC][k%4]
    box(s,x,y,13.6,2.8,fill,1.2)
    tx(s,x+0.6,y+0.4,12.4,2.2,f'{k+1}. {t}',11.5,col)
tx(s,X0,16.8,28,0.8,'Semua sumber diakses 9 November 2026.',10,MUT)
notes(s,'Daftar pustaka memuat sumber yang benar-benar dibuka: halaman resmi Mendeley, Mendeley Support, KBBI VI Daring, dan panduan gaya APA serta IEEE. Perbarui tanggal akses bila presentasi dilakukan pada hari lain.')
# 16 penutup
s=slide(BG)
tx(s,2.4,4.2,19,4.0,'Terima kasih',72,TX,True)
tx(s,2.4,9.0,18,1.4,'Pertanyaan dan diskusi',24,P,True)
pic(s,icon('MdQuestionAnswer',FLOWER,PC,ON_PC),23.0,4.8,8.4,'Ikon tanya jawab')
notes(s,'Tutup dengan terima kasih dan ajak tanya jawab. Arahkan pertanyaan tentang langkah implementasi, kendala metadata, dan pilihan gaya sitasi ke slide terkait.')
# --- animasi per objek: group dianimasikan lewat proxy, lalu targetnya dipindah ke group ---
HIN,HOUT='M 1 0 L 0 0 E','M 0 0 L -1 0 E'
VIN,VOUT='M 0 1 L 0 0 E','M 0 0 L 0 -1 E'
SIN,SOUT='M -0.12 0 L 0 0 E','M 0 0 L -0.12 0 E'
PDOWN='M 0 -0.1522 L 0 0 E'
def anim(target,d,trigger,dur):
    emit(target,'animation',{'class':'motion','path':'custom','d':d,'trigger':trigger,'duration':dur})
def proxy(i,tag):
    emit(f'/slide[{i}]','shape',{'x':'0cm','y':'0cm','width':'0.01cm','height':'0.01cm','fill':'none','line':'none','name':f'#s{i}-proxy-{tag}'})
# AddAnimation hanya menghitung shape top-level, bukan group atau picture.
for i in range(1,TOTAL+1):
    s=f'/slide[{i}]';total=counts[s];cs=content_start[s];se=sidebar_end.get(s,cs-1);pill=pill_idx.get(s)
    emit(s,'group',{'shapes':','.join(map(str,range(cs,total+1))),'name':f'#s{i}-content'})
    split=i in (3,13,15)
    if split:
        emit(s,'group',{'shapes':'1,2','name':f'#s{i}-sidebar-bg','zorder':'1'})
        fg=[k for k in range(2,se) if k!=pill_top[s]-1]
        emit(s,'group',{'shapes':','.join(map(str,fg)),'name':f'#s{i}-sidebar-fg','zorder':'3'})
        ct,bt,ft=2,3,4
    else:
        ct=sidebar_shapes.get(s,0)+1;bt=ft=None
    proxy(i,'content')
    if split:
        proxy(i,'sidebar-bg');proxy(i,'sidebar-fg')
    c=f'/slide[{i}]/shape[{ct}]'
    if i in (1,2,14,16):
        if i in (2,14,16):anim(c,HIN,'afterPrevious',420)
        if i in (1,2,14):anim(c,HOUT,'onClick',220)
        continue
    if i in (3,15):
        b,f,p=f'/slide[{i}]/shape[{bt}]',f'/slide[{i}]/shape[{ft}]',f'/slide[{i}]/shape[1]'
        anim(b,SIN,'afterPrevious',400);anim(f,SIN,'withPrevious',400);anim(p,SIN,'withPrevious',400)
        anim(c,VIN,'withPrevious',500)
    else:
        anim(c,VIN,'afterPrevious',500)
    if i in (5,8,13):anim(f'/slide[{i}]/shape[{1 if i==13 else pill}]',PDOWN,'afterPrevious',500)
    anim(c,VOUT,'onClick',300)
    if i in (13,15):
        b,f,p=f'/slide[{i}]/shape[{bt}]',f'/slide[{i}]/shape[{ft}]',f'/slide[{i}]/shape[1]'
        anim(b,SOUT,'withPrevious',200);anim(f,SOUT,'withPrevious',200);anim(p,SOUT,'withPrevious',200)
# --- bangun ---
assert n==TOTAL,f'jumlah slide {n}, seharusnya {TOTAL}'
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
subprocess.run([sys.executable,'retarget_group_animations.py',OUT],check=True)
