const fs=require('fs'),React=require('react'),S=require('react-dom/server'),sharp=require('sharp'),m=require('react-icons/md');
const specs=JSON.parse(fs.readFileSync(process.argv[2]));
fs.mkdirSync('assets',{recursive:true});
function outline(shape,N=480){const p=[];for(let i=0;i<N;i++){const t=i/N*2*Math.PI;let r=1;
 if(shape==='cookie')r=(1+.055*Math.cos(9*t))/1.055;
 else if(shape==='flower')r=(1+.12*Math.cos(8*t))/1.12;
 else if(shape==='squircle')r=1/Math.pow(Math.pow(Math.abs(Math.cos(t)),4)+Math.pow(Math.abs(Math.sin(t)),4),.25)/1.05;
 p.push([256+250*r*Math.cos(t),256+250*r*Math.sin(t)]);}
 return 'M'+p.map(a=>a[0].toFixed(1)+' '+a[1].toFixed(1)).join('L')+'Z';}
(async()=>{for(const s of specs){
 const sz=s.shape==='none'?512:290, ic=S.renderToStaticMarkup(React.createElement(m[s.icon],{size:sz})).replace(/currentColor/g,'#'+s.fg);
 const icon=await sharp(Buffer.from(ic)).resize(sz,sz).png().toBuffer();
 let base;
 if(s.shape==='none')base=sharp({create:{width:512,height:512,channels:4,background:{r:0,g:0,b:0,alpha:0}}}).png();
 else base=sharp(Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512"><path d="${outline(s.shape)}" fill="#${s.bg}"/></svg>`));
 await base.composite([{input:icon,left:Math.round((512-sz)/2),top:Math.round((512-sz)/2)}]).png().toFile('assets/'+s.file);}
 console.log('icons',specs.length);})();
