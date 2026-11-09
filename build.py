import json,subprocess,os,hashlib
OUT='deck.pptx'
# --- palet M3 Expressive dari #B0C8E0 #C1E0E0 #DCE7D6 #F6F6F6 ---
BG,RAIL,CARD='F6F6F6','ECEEEE','E6E9E9'
TX,MUT='2F3334','5B6061'
P,ON_P,PC,ON_PC='46627A','F6F9FF','B0C8E0','355169'
SC,ON_SC='C1E0E0','3D6060'
TC,ON_TC='DCE7D6','536350'
EC,ON_EC='F56965','65000B'
DBG,DTX,DP,DPC,DTC='0C0F0F','E2E6E7','DCEDFF','355169','41513E'
DCARD='1C2021'
F='Calibri'
ops=[];specs={};n=0
def cm(v):return f'{v:.2f}cm'
def icon(name,shape,bg,fg):
    f=hashlib.md5(f'{name}{shape}{bg}{fg}'.encode()).hexdigest()[:10]+'.png'
    specs[f]=dict(file=f,icon=name,shape=shape,bg=bg,fg=fg);return f
def add(parent,typ,**p):ops.append(dict(command='add',parent=parent,type=typ,props={k:str(v) for k,v in p.items()}))
def slide(bg):
    global n;n+=1;add('/','slide',background=bg);return f'/slide[{n}]'
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
def notes(s,t):add(s,'notes',text=t)
def num(s,x,y,d,t,fill,col):
    add(s,'shape',geometry='ellipse',x=cm(x),y=cm(y),width=cm(d),height=cm(d),text=t,size=20,bold='true',color=col,
        align='center',valign='middle',font=F,fill=fill,line='none',margin='0',name='nomor')
SECT=[('menu_book','MdMenuBook','Latar'),('lib','MdLibraryBooks','Mengenal'),('build','MdBuild','Praktik'),('bal','MdBalance','Evaluasi'),('flag','MdFlag','Penutup')]
def frame(i,sec,title):
    s=slide(BG);box(s,1.0,1.0,2.8,17.05,RAIL,1.2,name='rail')
    pic(s,icon('MdLibraryBooks','cookie',P,'FFFFFF'),1.7,1.6,1.4,'Logo bagian')
    for k,(_,ic,lab) in enumerate(SECT):
        y=3.5+k*2.9;on=k==sec
        if on:box(s,1.3,y,2.2,2.6,PC,1.1,name='rail-aktif')
        pic(s,icon(ic,'none','x',ON_PC if on else MUT),1.9,y+0.35,1.0,lab)
        tx(s,1.3,y+1.6,2.2,0.7,lab,12,ON_PC if on else MUT,on,'center','middle','rail-label')
    tx(s,4.4,1.2,28,2.4,title,36,TX,True,valign='middle',name='judul')
    tx(s,29.4,18.2,3,0.6,f'{i} / 16',10,MUT,align='right',name='nomor-slide')
    return s
X0,W=4.4,28.0
def card3(s,y,h,items,fills):
    w=(W-1.6)/3
    for k,(ic,hd,bd) in enumerate(items):
        x=X0+k*(w+0.8);box(s,x,y,w,h,fills[k][0],1.2)
        pic(s,icon(ic,['cookie','flower','cookie'][k],fills[k][1],fills[k][2]),x+0.8,y+0.8,2.4,hd)
        tx(s,x+0.8,y+3.5,w-1.6,1.3,hd,22,fills[k][3],True)
        tx(s,x+0.8,y+4.8,w-1.6,h-4.6,bd,18,fills[k][3])
# 1 sampul
s=slide(BG)
pic(s,icon('MdLibraryBooks','flower',PC,ON_PC),20.6,2.6,12,'Ilustrasi Mendeley')
pic(s,icon('MdFormatQuote','cookie',TC,ON_TC),28.4,12.6,5,'Ikon kutipan')
box(s,2.0,3.0,8.4,1.6,PC,0.8,name='label');tx(s,2.0,3.0,8.4,1.6,'Bahasa Indonesia',18,ON_PC,True,'center','middle')
tx(s,2.0,4.4,18,7.8,'Implementasi aplikasi Mendeley dalam penulisan karya ilmiah',44,TX,True,name='judul')
tx(s,2.0,13.4,18,1,'Mata kuliah Bahasa Indonesia',20,P,True)
notes(s,'Salam pembuka. Perkenalkan topik: cara Mendeley dipakai untuk menyusun kutipan dan daftar pustaka karya ilmiah.')
# 2 anggota
s=slide(BG)
tx(s,2.0,1.4,28,2.4,'Anggota kelompok',40,TX,True,valign='middle',name='judul')
tx(s,2.0,3.6,28,1,'Mata kuliah Bahasa Indonesia',18,P,True)
for k,(nm,nim) in enumerate([('Aminadab Yunus','202451028'),('Arkano Hamada Moslem','202551034'),('Farrel Aufa Athaya Ardiyono','202551042'),("Muhammad La'azidannak Rusda",'202551049'),('Aksel Agustiyan','202551058'),('Muhammad Arief Satria Nugraha','202551151')]):
    x=(2.0+k*7.3) if k<4 else (8.85+(k-4)*7.3);y=5.2 if k<4 else 11.0
    fill=[PC,CARD,TC,CARD,PC,CARD][k];col=[ON_PC,TX,ON_TC,TX,ON_PC,TX][k]
    box(s,x,y,6.8,5.2,fill,1.2)
    tx(s,x+0.6,y+0.4,2.4,0.8,f'{k+1:02d}',16,col,True)
    tx(s,x+0.6,y+1.3,5.6,2.4,nm,16,col,True)
    tx(s,x+0.6,y+3.8,5.6,1.2,nim,12,MUT)
tx(s,29.4,18.2,3,0.6,'2 / 16',10,MUT,align='right',name='nomor-slide')
notes(s,'Sebutkan anggota kelompok satu per satu. Rifqy belum mengirim nama lengkap dan NIM; tambahkan kartunya saat data tersedia.')
# 3 latar belakang
s=frame(3,0,'Sitasi manual rawan salah dan lambat')
card3(s,4.0,8.2,[('MdFormatAlignLeft','Format berbeda','Gaya sitasi berbeda antarparagraf karena diketik satu per satu.'),
 ('MdLinkOff','Sumber terlupa','Kutipan ada di naskah, tetapi rujukannya tidak masuk daftar pustaka.'),
 ('MdCompareArrows','Daftar tak cocok','Isi daftar pustaka tidak sama dengan sumber yang dikutip di teks.')],[(CARD,PC,ON_PC,TX)]*3)
box(s,X0,13.0,W,5.0,PC,1.4)
pic(s,icon('MdTimer','circle',P,'FFFFFF'),X0+1.0,14.2,2.6,'Ikon waktu')
tx(s,X0+4.4,13.4,W-5.4,4.2,'Menulis kutipan dan daftar pustaka secara manual menyita waktu. Sumber yang tidak tercantum dapat dinilai sebagai plagiarisme, sehingga kesalahan kecil pun berisiko.',22,ON_PC,False,valign='middle')
notes(s,'Mahasiswa sering salah pada tiga hal: format kutipan tidak seragam, sumber lupa dicantumkan, dan daftar pustaka tidak cocok dengan isi. Semua itu berkaitan dengan etika kutipan dan plagiarisme yang kita pelajari di mata kuliah ini.')
# 4 rumusan
s=frame(4,0,'Rumusan masalah dan tujuan')
for k,(ic,hd,its,pitch,fill,col,nb,nc) in enumerate([('MdQuestionAnswer','Rumusan masalah',['Bagaimana Mendeley diimplementasikan dalam penulisan karya ilmiah?','Apa manfaat dan keterbatasan Mendeley bagi mahasiswa?'],4.2,CARD,TX,P,'FFFFFF'),
 ('MdFlag','Tujuan',['Menjelaskan fungsi Mendeley.','Menguraikan langkah penggunaannya.','Menilai manfaat dan keterbatasannya.'],2.9,TC,ON_TC,ON_TC,'FFFFFF')]):
    x=X0+k*14.4;box(s,x,4.0,13.6,14.0,fill,1.4)
    pic(s,icon(ic,'cookie',PC if k==0 else SC,ON_PC if k==0 else ON_TC),x+0.9,4.9,2.2,hd)
    tx(s,x+3.6,4.9,9,2.2,hd,26,col,True,valign='middle')
    for j,t in enumerate(its):
        y=8.2+j*pitch;num(s,x+0.9,y,1.5,str(j+1),nb,nc);tx(s,x+3.0,y-0.2,10,pitch-0.4,t,20,col,valign='top')
notes(s,'Dua rumusan masalah menuntun presentasi ini: cara implementasi dan manfaat serta keterbatasan. Tiga tujuan mengikuti urutan tersebut: fungsi, langkah, lalu evaluasi.')
# 5 mengenal
s=frame(5,1,'Tiga komponen utama Mendeley')
box(s,X0,4.0,10.0,14.0,PC,1.4)
pic(s,icon('MdLibraryBooks','flower',P,'FFFFFF'),X0+1.2,4.9,3.6,'Ikon Mendeley')
tx(s,X0+1.0,9.4,8,5.6,'Mendeley adalah aplikasi pengelola referensi dan jejaring akademik. Elsevier mengembangkannya.',22,ON_PC,True)
tx(s,X0+1.0,15.0,8,2.6,'Pengembangan Mendeley Desktop dihentikan; Reference Manager menjadi fokus.',16,ON_PC)
for k,(ic,hd,bd) in enumerate([('MdLibraryBooks','Mendeley Reference Manager','Pustaka pribadi untuk menyimpan, mengelompokkan, dan menganotasi PDF jurnal.'),
 ('MdDescription','Mendeley Cite','Add-in Microsoft Word untuk menyisipkan kutipan dan membuat daftar pustaka.'),
 ('MdExtension','Web Importer','Ekstensi peramban untuk menyimpan referensi dari halaman web.')]):
    y=4.0+k*4.9;box(s,X0+10.8,y,17.2,4.2,CARD,1.2)
    pic(s,icon(ic,'cookie',SC,ON_SC),X0+11.5,y+0.8,2.6,hd)
    tx(s,X0+14.8,y+0.6,12.6,1.2,hd,22,TX,True);tx(s,X0+14.8,y+1.8,12.6,2.3,bd,18,MUT)
tx(s,X0,18.3,20,0.4,'Sumber: Mendeley (n.d.); Mendeley Support (2025).',8,MUT)
notes(s,'Mendeley dikembangkan Elsevier. Ada tiga komponen: Reference Manager untuk pustaka, Mendeley Cite untuk Word, dan Web Importer untuk peramban. Mendeley Desktop masih tersedia, tetapi pengembangannya sudah dihentikan; Reference Manager menjadi fokus.')
# 6 kaidah
s=frame(6,1,'Kaitan Mendeley dengan kaidah bahasa')
box(s,X0,4.0,W,4.6,P,1.4)
pic(s,icon('MdSchool','circle',PC,ON_PC),X0+1.0,5.0,2.6,'Ikon pengetahuan')
tx(s,X0+4.4,4.0,W-5.4,4.6,'Mendeley menjaga konsistensi format. Pemahaman kaidah kutipan tetap menjadi tanggung jawab penulis.',24,'FFFFFF',True,valign='middle')
card3(s,9.4,8.6,[('MdFormatQuote','Kutipan','Langsung, yaitu kata demi kata dalam tanda petik, dan tidak langsung, yaitu parafrasa.'),
 ('MdListAlt','Daftar pustaka','Urutan, tanda baca, dan penulisan nama penulis mengikuti gaya yang dipilih.'),
 ('MdStyle','Gaya selingkung','APA, IEEE, atau Harvard sesuai ketentuan kampus, satu gaya untuk seluruh naskah.')],[(CARD,SC,ON_SC,TX),(CARD,TC,ON_TC,TX),(CARD,PC,ON_PC,TX)])
tx(s,X0,18.3,20,0.4,'Sumber: KBBI VI Daring.',8,MUT)
notes(s,'Materi kita di kelas membahas kutipan langsung dan tidak langsung, penulisan daftar pustaka, dan gaya selingkung. Mendeley hanya menerapkan gaya yang kita pilih; kalau kita salah memilih atau salah mengisi data, hasilnya tetap salah.')
# 7 contoh kaidah
s=frame(7,1,'Contoh kaidah: satu sumber')
box(s,X0,4.0,13.6,5.8,CARD,1.4)
tx(s,X0+0.8,4.6,12.0,1.2,'Kutipan langsung',20,TX,True)
tx(s,X0+0.8,6.0,12.0,3.4,'“pengungkapan kembali suatu tuturan dari sebuah tingkatan atau macam bahasa menjadi tuturan yang lain tanpa mengubah pengertian” (Badan Pengembangan dan Pembinaan Bahasa, n.d.).',15,TX)
box(s,X0,10.4,13.6,5.8,SC,1.4)
tx(s,X0+0.8,11.0,12.0,1.2,'Kutipan tidak langsung',20,ON_SC,True)
tx(s,X0+0.8,12.4,12.0,3.4,'Parafrasa mengungkapkan kembali suatu tuturan dengan bentuk lain tanpa mengubah maknanya (Badan Pengembangan dan Pembinaan Bahasa, n.d.).',15,ON_SC)
box(s,X0+14.4,4.0,13.6,5.8,TC,1.4)
tx(s,X0+15.2,4.6,12.0,1.2,'Daftar pustaka: APA',20,ON_TC,True)
tx(s,X0+15.2,6.0,12.0,3.6,'Badan Pengembangan dan Pembinaan Bahasa. (n.d.). Parafrasa. KBBI VI Daring. Diakses 9 November 2026, dari https://kbbi.kemendikdasmen.go.id/entri/parafrasa',11,ON_TC)
box(s,X0+14.4,10.4,13.6,5.8,PC,1.4)
tx(s,X0+15.2,11.0,12.0,1.2,'Daftar pustaka: IEEE',20,ON_PC,True)
tx(s,X0+15.2,12.4,12.0,3.6,'[1] Badan Pengembangan dan Pembinaan Bahasa, “Parafrasa,” KBBI VI Daring. [Online]. Available: https://kbbi.kemendikdasmen.go.id/entri/parafrasa. [Accessed: Nov. 9, 2026].',10,ON_PC)
tx(s,X0,16.8,28,0.8,'Satu sumber, dua bentuk kutipan, dua gaya daftar pustaka. Tanggal akses: 9 November 2026.',10,MUT)
notes(s,'Tunjukkan bahwa satu sumber yang sama bisa muncul sebagai kutipan langsung, kutipan tidak langsung, dan entri daftar pustaka. Bedanya hanya bentuk penyajian; sumbernya tetap harus sama.')
# 8 persiapan
s=frame(8,2,'Persiapan: akun, aplikasi, dan add-in')
w3=(W-1.6)/3
for k,(ic,hd,bd) in enumerate([('MdPersonAdd','Buat akun','Daftar dengan email aktif.'),('MdDownload','Pasang aplikasi','Unduh Reference Manager, lalu pasang add-in Mendeley Cite di Word.'),('MdExtension','Pasang ekstensi','Tambahkan Web Importer ke peramban untuk menyimpan referensi dari web.')]):
    x=X0+k*(w3+0.8);box(s,x,4.2,w3,12.6,CARD if k!=1 else PC,1.4)
    num(s,x+0.9,5.0,1.7,str(k+1),P,'FFFFFF')
    pic(s,icon(ic,'flower',PC if k!=1 else P,ON_PC if k!=1 else 'FFFFFF'),x+w3-5.4,4.8,4.6,hd)
    tx(s,x+0.9,10.4,w3-1.8,1.4,hd,24,TX if k!=1 else ON_PC,True);tx(s,x+0.9,12.2,w3-1.8,4.6,bd,20,MUT if k!=1 else ON_PC)
tx(s,X0,18.3,20,0.4,'Sumber: Mendeley (n.d.).',8,MUT)
notes(s,'Tiga persiapan: membuat akun dengan email aktif, memasang Reference Manager dan add-in Mendeley Cite di Word, lalu memasang Web Importer di peramban.')
# 9 langkah 1
s=frame(9,2,'Langkah 1: kumpulkan referensi')
for k,(ic,hd,bd) in enumerate([('MdUploadFile','Impor PDF','Tambahkan PDF jurnal ke Library.'),('MdLanguage','Simpan dari web','Gunakan Web Importer pada halaman artikel.'),('MdFactCheck','Periksa metadata','Cek judul, penulis, tahun, dan DOI; koreksi yang salah.'),('MdFolder','Rapikan','Kelompokkan dengan folder dan tag per bab atau topik.')]):
    x=X0+(k%2)*14.4;y=4.0+(k//2)*7.4;box(s,x,y,13.6,6.6,[CARD,SC,TC,CARD][k],1.3)
    pic(s,icon(ic,['cookie','flower','cookie','flower'][k],[PC,P,SC,SC][k],[ON_PC,'FFFFFF',ON_TC,ON_SC][k]),x+0.9,y+1.6,3.4,hd)
    tx(s,x+5.0,y+1.2,8.0,1.3,hd,24,TX,True);tx(s,x+5.0,y+2.7,8.0,3.4,bd,19,MUT)
notes(s,'Mulai dari mengumpulkan sumber. Metadata hasil impor sering keliru, jadi periksa judul, penulis, tahun, dan DOI satu per satu. Folder dan tag per bab memudahkan pencarian saat menulis.')
# 10 langkah 2
s=frame(10,2,'Langkah 2: baca dan catat')
box(s,X0,4.0,17.6,14.0,CARD,1.4)
for k,(ic,hd,bd) in enumerate([('MdBorderColor','Highlight dan anotasi','Tandai bagian penting langsung pada PDF.'),('MdStickyNote2','Catatan per referensi','Tulis ide utama dengan kata sendiri sebelum menulis naskah.')]):
    y=4.9+k*6.6;pic(s,icon(ic,'cookie',SC,ON_SC),X0+1.0,y+0.6,3.6,hd)
    tx(s,X0+5.4,y+0.6,11.2,1.4,hd,24,TX,True);tx(s,X0+5.4,y+2.2,11.2,3.4,bd,20,MUT)
box(s,X0+18.4,4.0,9.6,14.0,TC,1.4)
pic(s,icon('MdLightbulb','flower',SC,ON_TC),X0+19.6,5.2,4.2,'Ikon ide')
tx(s,X0+19.4,10.6,7.6,1.4,'Hasilnya',26,ON_TC,True);tx(s,X0+19.4,12.2,7.6,5,'Bahan parafrasa untuk menyusun kutipan tidak langsung.',22,ON_TC)
notes(s,'Anotasi dan catatan membantu kita memahami sumber lebih dulu. Dari catatan itulah kutipan tidak langsung ditulis ulang dengan kalimat sendiri, lengkap dengan sitasinya.')
# 11 langkah 3
s=frame(11,2,'Langkah 3: sisipkan kutipan di Word')
w4=(W-3*1.6)/4
for k,(ic,hd,bd) in enumerate([('MdDescription','Buka add-in','Buka Mendeley Cite di Microsoft Word.'),('MdFormatQuote','Sisipkan kutipan','Pilih referensi, lalu tempatkan pada kalimat.'),('MdStyle','Pilih gaya','Sesuaikan dengan pedoman kampus.'),('MdListAlt','Buat daftar pustaka','Daftar pustaka tersusun otomatis.')]):
    x=X0+k*(w4+1.6);box(s,x,4.4,w4,13.0,[CARD,SC,TC,PC][k],1.3)
    num(s,x+0.7,5.1,1.5,str(k+1),P,'FFFFFF')
    pic(s,icon(ic,'cookie',['E2E3D8','F9FAEF','F9FAEF','F9FAEF'][k] if False else [PC,P,SC,P][k],[ON_PC,'FFFFFF',ON_TC,'FFFFFF'][k]),x+0.7,7.2,3.4,hd)
    tx(s,x+0.7,11.0,w4-1.4,2.4,hd,22,TX,True);tx(s,x+0.7,13.6,w4-1.4,3.4,bd,18,MUT)
    if k<3:pic(s,icon('MdArrowForward','none','x',P),x+w4+0.3,10.2,1.0,'Panah')
notes(s,'Alurnya empat langkah di Word: buka Mendeley Cite, sisipkan kutipan, pilih gaya sesuai pedoman kampus, lalu buat daftar pustaka. Daftar pustaka ikut berubah otomatis saat kutipan ditambah atau dihapus.')
# 12 demo
s=frame(12,2,'Demo alur: impor sampai daftar pustaka')
box(s,X0,4.0,10.2,14.0,CARD,1.4)
for k,t in enumerate(['Metadata: judul, penulis, tahun, DOI','Gaya: satu gaya untuk seluruh naskah','Hasil: cek daftar pustaka sebelum dikumpulkan']):
    y=5.0+k*4.2;num(s,X0+0.9,y,1.6,str(k+1),P,'FFFFFF');tx(s,X0+3.1,y-0.3,6.6,2.4,t,20,TX,True,valign='middle')
for k,(lab,img,cap) in enumerate([('Library','mendeley-library.png','Impor PDF, kelompokkan, dan rapikan referensi.'),('Daftar pustaka','mendeley-bibliography.png','Sisipkan kutipan di Word, lalu buat daftar pustaka otomatis.')]):
    x=X0+11.0+k*8.6;box(s,x,4.0,8.4,14.0,CARD,1.4,line='AFB3B3',name='bingkai-gambar')
    pic(s,img,x+0.6,4.8,7.2,'Tangkapan layar '+lab,6.3)
    box(s,x+0.6,11.5,3.6,1.0,PC,0.55,name='label');tx(s,x+0.6,11.5,3.6,1.0,lab,14,ON_PC,True,'center','middle')
    tx(s,x+0.6,12.8,7.2,2.4,cap,16,MUT)
    tx(s,x+0.6,15.6,7.2,0.7,'Sumber: mendeley.com',10,MUT)
notes(s,'Peragakan alur singkat langsung: impor ke Library, sisipkan kutipan, lalu buat daftar pustaka. Gambar di slide adalah ilustrasi resmi Mendeley (mendeley.com), bukan hasil uji; ganti dengan tangkapan layar sendiri bila sudah mencoba alurnya.')
# 13 kelebihan keterbatasan
s=frame(13,3,'Kelebihan dan keterbatasan')
for k,(ic,hd,its,fill,col,sh,fg) in enumerate([('MdCheckCircle','Kelebihan',['Hemat waktu','Format konsisten','Kutipan dan daftar pustaka sinkron','Penyimpanan dan sinkronisasi antarperangkat'],PC,ON_PC,P,'FFFFFF'),
 ('MdWarning','Keterbatasan',['Metadata impor perlu dicek manual','Gaya sitasi kampus tertentu mungkin tidak tersedia','Penyimpanan gratis 2 GB','Kesalahan tetap menjadi tanggung jawab penulis'],EC,ON_EC,'AC3434','FFFFFF')]):
    x=X0+k*14.4;box(s,x,4.0,13.6,14.0,fill,1.4)
    pic(s,icon(ic,'cookie',sh,fg),x+0.9,4.8,2.2,hd);tx(s,x+3.6,4.8,9.4,2.2,hd,26,col,True,valign='middle')
    for j,t in enumerate(its):
        y=7.9+j*2.5;add(s,'shape',geometry='ellipse',x=cm(x+1.0),y=cm(y+0.35),width=cm(0.5),height=cm(0.5),fill=sh,line='none',name='titik')
        tx(s,x+2.0,y,10.8,2.3,t,19,col)
tx(s,X0,18.3,20,0.4,'Sumber: Mendeley Support (2025).',8,MUT)
notes(s,'Kelebihan: hemat waktu, format konsisten, dan sinkron. Keterbatasannya: metadata perlu dicek, gaya sitasi kampus tertentu mungkin tidak tersedia, penyimpanan gratis 2 GB, dan kesalahan tetap menjadi tanggung jawab penulis.')
# 14 kesimpulan (terang)
s=slide(BG);tx(s,2.0,1.4,30,2.4,'Kesimpulan dan saran',40,TX,True,valign='middle',name='judul')
w3=(31.8-2*0.9-2.0)/3 if False else 9.6
for k,(ic,hd,bd) in enumerate([('MdCheckCircle','Implementasinya','Impor referensi, sisipkan sitasi di Word, lalu buat daftar pustaka otomatis.'),('MdSchool','Manfaat dan batasannya','Format menjadi konsisten, tetapi metadata dan kaidah tetap harus diperiksa.'),('MdFlag','Saran','Mulai dari tugas kecil, cek metadata, dan gunakan satu gaya sitasi.')]):
    x=2.0+k*10.4;box(s,x,4.6,w3,12.6,[PC,CARD,TC][k],1.4)
    pic(s,icon(ic,'cookie',[P,SC,ON_TC][k],[ON_P,ON_SC,TC][k]),x+0.9,5.6,3.4,hd)
    tx(s,x+0.9,9.8,w3-1.8,2.8,hd,26,[ON_PC,TX,ON_TC][k],True);tx(s,x+0.9,12.8,w3-1.8,4.2,bd,19,[ON_PC,TX,ON_TC][k])
tx(s,29.4,18.2,3,0.6,'14 / 16',10,MUT,align='right',name='nomor-slide')
notes(s,'Jawab kedua rumusan: implementasinya lewat impor, sitasi, dan daftar pustaka otomatis; manfaatnya format konsisten, tetapi metadata dan kaidah tetap harus diperiksa. Sarankan mulai dari tugas kecil dan satu gaya sitasi.')
# 15 pustaka
s=frame(15,4,'Daftar pustaka')
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
    x=X0+(k%2)*14.4;y=4.2+(k//2)*2.9
    fill=[CARD,SC,TC,PC][k%4];col=[TX,ON_SC,ON_TC,ON_PC][k%4]
    box(s,x,y,13.6,2.6,fill,1.2)
    tx(s,x+0.6,y+0.4,12.4,2.0,f'{k+1}. {t}',9.5,col)
tx(s,X0,16.8,28,0.8,'Semua sumber diakses 9 November 2026.',10,MUT)
notes(s,'Daftar pustaka memuat sumber yang benar-benar dibuka: halaman resmi Mendeley, Mendeley Support, KBBI VI Daring, dan panduan gaya APA serta IEEE. Perbarui tanggal akses bila presentasi dilakukan pada hari lain.')
# 16 penutup
s=slide(BG)
box(s,2.0,2.0,9.2,1.4,PC,0.7);tx(s,2.0,2.0,9.2,1.4,'Penutup',18,ON_PC,True,'center','middle')
tx(s,2.0,4.4,20,3.0,'Terima kasih',54,TX,True)
tx(s,2.0,8.6,18,1.6,'Pertanyaan dan diskusi',28,P,True)
tx(s,2.0,11.0,18,2.4,'Sumber lengkap ada di slide daftar pustaka.',16,MUT)
pic(s,icon('MdQuestionAnswer','flower',TC,ON_TC),22.0,6.0,8.0,'Ikon tanya jawab')
tx(s,29.4,18.2,3,0.6,'16 / 16',10,MUT,align='right',name='nomor-slide')
notes(s,'Buka sesi tanya jawab. Arahkan pertanyaan tentang langkah implementasi, kendala metadata, dan pilihan gaya sitasi ke slide terkait.')
# --- bangun ---
json.dump(list(specs.values()),open('specs.json','w'))
subprocess.run(['node','icons.js','specs.json'],check=True)
json.dump(ops,open('ops.json','w'))
if os.path.exists(OUT):os.remove(OUT)
subprocess.run(['officecli','create',OUT],check=True)
r=subprocess.run(['officecli','batch',OUT,'--input','ops.json','--json'],capture_output=True,text=True);print(r.stdout[-1500:],r.stderr[-800:]);r.check_returncode()
