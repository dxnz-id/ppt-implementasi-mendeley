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
        tx(s,1.3,y+1.6,2.2,0.7,lab,10,ON_PC if on else MUT,on,'center','middle','rail-label')
    tx(s,4.4,1.2,28,2.4,title,36,TX,True,valign='middle',name='judul')
    tx(s,29.4,18.2,3,0.6,f'{i} / 13',10,MUT,align='right',name='nomor-slide')
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
s=slide(DBG)
pic(s,icon('MdLibraryBooks','flower',DPC,DP),20.6,2.6,12,'Ilustrasi Mendeley')
pic(s,icon('MdFormatQuote','cookie',DTC,'SC'),28.4,12.6,5,'Ikon kutipan')
box(s,2.0,3.0,8.4,1.6,DPC,0.8,name='label');tx(s,2.0,3.0,8.4,1.6,'Bahasa Indonesia',18,DP,True,'center','middle')
tx(s,2.0,5.0,18,8.6,'Implementasi aplikasi Mendeley dalam penulisan karya ilmiah',44,DTX,True,name='judul')
tx(s,2.0,14.0,18,1,'Mata kuliah Bahasa Indonesia',20,DP,True)
tx(s,2.0,15.4,19.5,1.4,'[Nama penyaji]  |  [NIM]  |  [Kelas]  |  [Dosen pengampu]',18,DTX)
notes(s,'Salam pembuka. Perkenalkan diri, lalu sebutkan topik: cara Mendeley dipakai untuk menyusun kutipan dan daftar pustaka karya ilmiah. Ganti teks dalam kurung siku dengan nama, NIM, kelas, dan dosen pengampu.')
# 2 latar belakang
s=frame(2,0,'Sitasi manual rawan salah dan lambat')
card3(s,4.0,8.2,[('MdFormatAlignLeft','Format berbeda','Gaya kutipan berbeda antarparagraf karena diketik satu per satu.'),
 ('MdLinkOff','Sumber terlupa','Kutipan ada di naskah, tetapi rujukannya tidak masuk daftar pustaka.'),
 ('MdCompareArrows','Daftar tak cocok','Isi daftar pustaka tidak sama dengan sumber yang dikutip di teks.')],[(CARD,PC,ON_PC,TX)]*3)
box(s,X0,13.0,W,5.0,PC,1.4)
pic(s,icon('MdTimer','circle',P,'FFFFFF'),X0+1.0,14.2,2.6,'Ikon waktu')
tx(s,X0+4.4,13.4,W-5.4,4.2,'Menulis kutipan dan daftar pustaka secara manual menyita waktu. Sumber yang tidak tercantum dapat dinilai sebagai plagiarisme, sehingga kesalahan kecil pun berisiko.',22,ON_PC,False,valign='middle')
notes(s,'Mahasiswa sering salah pada tiga hal: format kutipan tidak seragam, sumber lupa dicantumkan, dan daftar pustaka tidak cocok dengan isi. Semua itu berkaitan dengan etika kutipan dan plagiarisme yang kita pelajari di mata kuliah ini.')
# 3 rumusan
s=frame(3,0,'Rumusan masalah dan tujuan')
for k,(ic,hd,its,pitch,fill,col,nb,nc) in enumerate([('MdQuestionAnswer','Rumusan masalah',['Bagaimana Mendeley diimplementasikan dalam penulisan karya ilmiah?','Apa manfaat dan keterbatasan Mendeley bagi mahasiswa?'],4.2,CARD,TX,P,'FFFFFF'),
 ('MdFlag','Tujuan',['Menjelaskan fungsi Mendeley.','Menguraikan langkah penggunaannya.','Mengevaluasi hasil penggunaannya.'],2.9,TC,ON_TC,ON_TC,'FFFFFF')]):
    x=X0+k*14.4;box(s,x,4.0,13.6,14.0,fill,1.4)
    pic(s,icon(ic,'cookie',PC if k==0 else 'SC',ON_PC if k==0 else ON_TC),x+0.9,4.9,2.2,hd)
    tx(s,x+3.6,4.9,9,2.2,hd,26,col,True,valign='middle')
    for j,t in enumerate(its):
        y=8.2+j*pitch;num(s,x+0.9,y,1.5,str(j+1),nb,nc);tx(s,x+3.0,y-0.2,10,pitch-0.4,t,20,col,valign='top')
notes(s,'Dua rumusan masalah menuntun presentasi ini: cara implementasi dan manfaat serta keterbatasan. Tiga tujuan mengikuti urutan tersebut: fungsi, langkah, lalu evaluasi.')
# 4 mengenal
s=frame(4,1,'Tiga komponen utama Mendeley')
box(s,X0,4.0,10.0,14.0,PC,1.4)
pic(s,icon('MdLibraryBooks','flower',P,'FFFFFF'),X0+1.2,4.9,3.6,'Ikon Mendeley')
tx(s,X0+1.0,9.4,8,5.6,'Mendeley adalah aplikasi pengelola referensi dan jejaring akademik. Elsevier mengembangkannya.',22,ON_PC,True)
tx(s,X0+1.0,15.0,8,2.6,'Mendeley Desktop versi lama telah digantikan oleh Reference Manager.',16,ON_PC)
for k,(ic,hd,bd) in enumerate([('MdLibraryBooks','Mendeley Reference Manager','Pustaka pribadi untuk menyimpan, mengelompokkan, dan menganotasi PDF jurnal.'),
 ('MdDescription','Mendeley Cite','Plugin Microsoft Word untuk menyisipkan kutipan dan membuat daftar pustaka.'),
 ('MdExtension','Web Importer','Ekstensi peramban untuk menyimpan referensi dari halaman web.')]):
    y=4.0+k*4.9;box(s,X0+10.8,y,17.2,4.2,CARD,1.2)
    pic(s,icon(ic,'cookie',SC,ON_SC),X0+11.5,y+0.8,2.6,hd)
    tx(s,X0+14.8,y+0.6,12.6,1.2,hd,22,TX,True);tx(s,X0+14.8,y+1.8,12.6,2.3,bd,18,MUT)
notes(s,'Mendeley dikembangkan Elsevier. Ada tiga komponen: Reference Manager untuk pustaka, Mendeley Cite untuk Word, dan Web Importer untuk peramban. Mendeley Desktop versi lama sudah digantikan Reference Manager; cek tanggal dan status terbarunya di situs resmi sebelum presentasi.')
# 5 kaidah
s=frame(5,1,'Kaitan Mendeley dengan kaidah bahasa')
box(s,X0,4.0,W,4.6,P,1.4)
pic(s,icon('MdSchool','circle',PC,ON_PC),X0+1.0,5.0,2.6,'Ikon pengetahuan')
tx(s,X0+4.4,4.0,W-5.4,4.6,'Mendeley menjaga konsistensi format. Pemahaman kaidah kutipan tetap menjadi tanggung jawab penulis.',24,'FFFFFF',True,valign='middle')
card3(s,9.4,8.6,[('MdFormatQuote','Kutipan','Langsung, yaitu kata demi kata dalam tanda petik, dan tidak langsung, yaitu parafrasa.'),
 ('MdListAlt','Daftar pustaka','Urutan, tanda baca, dan penulisan nama penulis mengikuti gaya yang dipilih.'),
 ('MdStyle','Gaya selingkung','APA, IEEE, atau Harvard sesuai ketentuan kampus, satu gaya untuk seluruh naskah.')],[(CARD,SC,ON_SC,TX),(CARD,TC,ON_TC,TX),(CARD,PC,ON_PC,TX)])
notes(s,'Materi kita di kelas membahas kutipan langsung dan tidak langsung, penulisan daftar pustaka, dan gaya selingkung. Mendeley hanya menerapkan gaya yang kita pilih; kalau kita salah memilih atau salah mengisi data, hasilnya tetap salah.')
# 6 persiapan
s=frame(6,2,'Persiapan: akun, aplikasi, dan plugin')
w3=(W-1.6)/3
for k,(ic,hd,bd) in enumerate([('MdPersonAdd','Buat akun','Daftar memakai email institusi kampus.'),('MdDownload','Pasang aplikasi','Unduh Reference Manager, lalu pasang plugin Mendeley Cite di Word.'),('MdExtension','Pasang ekstensi','Tambahkan Web Importer ke peramban untuk menyimpan referensi dari web.')]):
    x=X0+k*(w3+0.8);box(s,x,4.2,w3,12.6,CARD if k!=1 else PC,1.4)
    num(s,x+0.9,5.0,1.7,str(k+1),P,'FFFFFF')
    pic(s,icon(ic,'flower',PC if k!=1 else P,ON_PC if k!=1 else 'FFFFFF'),x+w3-5.4,4.8,4.6,hd)
    tx(s,x+0.9,10.4,w3-1.8,1.4,hd,24,TX if k!=1 else ON_PC,True);tx(s,x+0.9,12.2,w3-1.8,4.6,bd,20,MUT if k!=1 else ON_PC)
notes(s,'Tiga persiapan: membuat akun dengan email institusi, memasang Reference Manager dan plugin Mendeley Cite di Word, lalu memasang Web Importer di peramban.')
# 7 langkah 1
s=frame(7,2,'Langkah 1: kumpulkan referensi')
for k,(ic,hd,bd) in enumerate([('MdUploadFile','Impor PDF','Tambahkan PDF jurnal ke Library.'),('MdLanguage','Simpan dari web','Gunakan Web Importer pada halaman artikel.'),('MdFactCheck','Periksa metadata','Cek judul, penulis, tahun, dan DOI; koreksi yang salah.'),('MdFolder','Rapikan','Kelompokkan dengan folder dan tag per bab atau topik.')]):
    x=X0+(k%2)*14.4;y=4.0+(k//2)*7.4;box(s,x,y,13.6,6.6,[CARD,SC,TC,CARD][k],1.3)
    pic(s,icon(ic,['cookie','flower','cookie','flower'][k],[PC,P,'SC',SC][k],[ON_PC,'FFFFFF',ON_TC,ON_SC][k]),x+0.9,y+1.6,3.4,hd)
    tx(s,x+5.0,y+1.2,8.0,1.3,hd,24,TX,True);tx(s,x+5.0,y+2.7,8.0,3.4,bd,19,MUT)
notes(s,'Mulai dari mengumpulkan sumber. Metadata hasil impor sering keliru, jadi periksa judul, penulis, tahun, dan DOI satu per satu. Folder dan tag per bab memudahkan pencarian saat menulis.')
# 8 langkah 2
s=frame(8,2,'Langkah 2: baca dan catat')
box(s,X0,4.0,17.6,14.0,CARD,1.4)
for k,(ic,hd,bd) in enumerate([('MdBorderColor','Highlight dan anotasi','Tandai bagian penting langsung pada PDF.'),('MdStickyNote2','Catatan per referensi','Tulis ide utama dengan kata sendiri sebelum menulis naskah.')]):
    y=4.9+k*6.6;pic(s,icon(ic,'cookie',SC,ON_SC),X0+1.0,y+0.6,3.6,hd)
    tx(s,X0+5.4,y+0.6,11.2,1.4,hd,24,TX,True);tx(s,X0+5.4,y+2.2,11.2,3.4,bd,20,MUT)
box(s,X0+18.4,4.0,9.6,14.0,TC,1.4)
pic(s,icon('MdLightbulb','flower','SC',ON_TC),X0+19.6,5.2,4.2,'Ikon ide')
tx(s,X0+19.4,10.6,7.6,1.4,'Hasilnya',26,ON_TC,True);tx(s,X0+19.4,12.2,7.6,5,'Bahan parafrase untuk menyusun kutipan tidak langsung.',22,ON_TC)
notes(s,'Anotasi dan catatan membantu kita memahami sumber lebih dulu. Dari catatan itulah kutipan tidak langsung ditulis ulang dengan kalimat sendiri, lengkap dengan sitasinya.')
# 9 langkah 3
s=frame(9,2,'Langkah 3: sisipkan kutipan di Word')
w4=(W-3*1.6)/4
for k,(ic,hd,bd) in enumerate([('MdDescription','Buka plugin','Buka Mendeley Cite di Microsoft Word.'),('MdFormatQuote','Sisipkan kutipan','Pilih referensi, lalu tempatkan pada kalimat.'),('MdStyle','Pilih gaya','Sesuaikan dengan pedoman kampus.'),('MdListAlt','Buat bibliografi','Daftar pustaka tersusun otomatis.')]):
    x=X0+k*(w4+1.6);box(s,x,4.4,w4,13.0,[CARD,SC,TC,PC][k],1.3)
    num(s,x+0.7,5.1,1.5,str(k+1),P,'FFFFFF')
    pic(s,icon(ic,'cookie',['E2E3D8','F9FAEF','F9FAEF','F9FAEF'][k] if False else [PC,P,'SC',P][k],[ON_PC,'FFFFFF',ON_TC,'FFFFFF'][k]),x+0.7,7.2,3.4,hd)
    tx(s,x+0.7,11.0,w4-1.4,2.4,hd,22,TX,True);tx(s,x+0.7,13.6,w4-1.4,3.4,bd,18,MUT)
    if k<3:pic(s,icon('MdArrowForward','none','x',P),x+w4+0.3,10.2,1.0,'Panah')
notes(s,'Alurnya empat langkah di Word: buka Mendeley Cite, sisipkan kutipan, pilih gaya sesuai pedoman kampus, lalu buat bibliografi. Daftar pustaka ikut berubah otomatis saat kutipan ditambah atau dihapus.')
# 10 demo
s=frame(10,2,'Demo: dari impor sampai daftar pustaka')
box(s,X0,4.0,10.2,14.0,CARD,1.4)
for k,t in enumerate(['Impor jurnal ke Library','Sisipkan kutipan di paragraf','Buat daftar pustaka otomatis']):
    y=5.0+k*4.2;num(s,X0+0.9,y,1.6,str(k+1),P,'FFFFFF');tx(s,X0+3.1,y-0.3,6.6,2.4,t,20,TX,True,valign='middle')
for k,(lab,img,cap) in enumerate([('Library','mendeley-library.png','Impor PDF, kelompokkan, dan rapikan referensi.'),('Daftar pustaka','mendeley-bibliography.png','Sisipkan kutipan di Word, lalu buat daftar pustaka otomatis.')]):
    x=X0+11.0+k*8.6;box(s,x,4.0,8.4,14.0,CARD,1.4,line='AFB3B3',name='bingkai-gambar')
    pic(s,img,x+0.6,4.8,7.2,'Tangkapan layar '+lab,6.3)
    box(s,x+0.6,11.5,3.6,1.0,PC,0.55,name='label');tx(s,x+0.6,11.5,3.6,1.0,lab,14,ON_PC,True,'center','middle')
    tx(s,x+0.6,12.8,7.2,2.4,cap,16,MUT)
    tx(s,x+0.6,15.6,7.2,0.7,'Sumber: mendeley.com',10,MUT)
notes(s,'Peragakan alur singkat langsung: impor ke Library, sisipkan kutipan, lalu buat daftar pustaka. Gambar di slide memakai tangkapan layar resmi Mendeley (mendeley.com); ganti dengan tangkapan layar sendiri bila sudah mencoba alurnya.')
# 11 kelebihan kekurangan
s=frame(11,3,'Kelebihan dan kekurangan')
for k,(ic,hd,its,fill,col,sh,fg) in enumerate([('MdCheckCircle','Kelebihan',['Hemat waktu','Format konsisten','Kutipan dan daftar pustaka sinkron','Penyimpanan dan sinkronisasi antarperangkat'],PC,ON_PC,P,'FFFFFF'),
 ('MdWarning','Kekurangan dan risiko',['Metadata impor sering keliru dan wajib dicek manual','Gaya sitasi kampus tertentu mungkin tidak tersedia','Penyimpanan gratis terbatas','Kesalahan Mendeley tetap menjadi tanggung jawab penulis'],EC,ON_EC,'AC3434','FFFFFF')]):
    x=X0+k*14.4;box(s,x,4.0,13.6,14.0,fill,1.4)
    pic(s,icon(ic,'cookie',sh,fg),x+0.9,4.8,2.2,hd);tx(s,x+3.6,4.8,9.4,2.2,hd,26,col,True,valign='middle')
    for j,t in enumerate(its):
        y=7.9+j*2.5;add(s,'shape',geometry='ellipse',x=cm(x+1.0),y=cm(y+0.35),width=cm(0.5),height=cm(0.5),fill=sh,line='none',name='titik')
        tx(s,x+2.0,y,10.8,2.3,t,19,col)
notes(s,'Kelebihan: hemat waktu, format konsisten, dan sinkron. Risikonya: metadata sering keliru, gaya sitasi kampus bisa tidak tersedia, penyimpanan gratis terbatas (cek batasnya di situs resmi), dan kesalahan tetap menjadi tanggung jawab penulis.')
# 12 kesimpulan (gelap)
s=slide(DBG);tx(s,2.0,1.4,30,2.4,'Kesimpulan dan saran',40,DTX,True,valign='middle',name='judul')
w3=(31.8-2*0.9-2.0)/3 if False else 9.6
for k,(ic,hd,bd) in enumerate([('MdCheckCircle','Efektif untuk kerapian','Mendeley merapikan kutipan dan daftar pustaka, tetapi tidak menjamin naskah bebas plagiarisme.'),('MdSchool','Kaidah tetap dipahami','Penulis perlu menguasai aturan kutipan dan memeriksa hasil akhir.'),('MdFlag','Saran','Mulai dari tugas kecil, lalu cek ulang daftar pustaka sebelum naskah dikumpulkan.')]):
    x=2.0+k*10.4;box(s,x,4.6,w3,12.6,[DPC,DCARD,DTC][k],1.4)
    pic(s,icon(ic,'cookie',[DP,DPC,'SC'][k],[DPC,DP,DTC][k]),x+0.9,5.6,3.4,hd)
    tx(s,x+0.9,9.8,w3-1.8,2.8,hd,26,DTX,True);tx(s,x+0.9,12.8,w3-1.8,4.2,bd,19,DTX)
notes(s,'Simpulkan: Mendeley efektif merapikan sitasi tetapi tidak menjamin bebas plagiarisme. Penulis tetap harus memahami kaidah dan memeriksa hasil akhir. Sarankan mulai dari tugas kecil dan cek ulang daftar pustaka sebelum dikumpulkan.')
# 13 pustaka
s=frame(13,4,'Daftar pustaka')
for k,(ic,hd,bd,dash) in enumerate([('MdLanguage','Situs resmi Mendeley','www.mendeley.com beserta panduan penggunaannya.',False),('MdMenuBook','Pedoman ejaan','Pedoman ejaan dan penulisan karya ilmiah yang dipakai kampus.',False),('MdSchool','Jurnal tentang reference manager','Tambahkan 2 sampai 3 artikel hasil pencarian dan verifikasi sendiri.',True)]):
    y=4.0+k*4.9
    if dash:box(s,X0,y,W,4.2,BG,1.2,line=P,dash='dash')
    else:box(s,X0,y,W,4.2,[CARD,SC][k],1.2)
    pic(s,icon(ic,'cookie',PC,ON_PC),X0+0.8,y+0.8,2.6,hd)
    tx(s,X0+4.2,y+0.7,23,1.3,hd,24,TX,True);tx(s,X0+4.2,y+2.1,23,1.6,bd,19,MUT)
notes(s,'Cantumkan hanya sumber yang benar-benar dibuka dan diperiksa. Isi bagian jurnal dengan hasil pencarian sendiri, jangan mengarang rujukan.')
# --- bangun ---
json.dump(list(specs.values()),open('specs.json','w'))
subprocess.run(['node','icons.js','specs.json'],check=True)
json.dump(ops,open('ops.json','w'))
if os.path.exists(OUT):os.remove(OUT)
subprocess.run(['officecli','create',OUT],check=True)
r=subprocess.run(['officecli','batch',OUT,'--input','ops.json','--json'],capture_output=True,text=True);print(r.stdout[-1500:],r.stderr[-800:]);r.check_returncode()
