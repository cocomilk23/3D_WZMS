import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const $=id=>document.getElementById(id);
const state=window.__previewState={ready:false,mode:'interactive',view:'oblique',error:null};
const presets={
  front:{position:[0,2.3,22],target:[0,3,-1],lens:31,label:'正面 · 校名墙',image:'01_Front_reference.png'},
  oblique:{position:[17,3.5,20],target:[0,2.7,-1],lens:34,label:'斜侧 · 入口关系',image:'02_Oblique_walkup.png'},
  aerial:{position:[37,31,43],target:[0,1.8,-6],lens:43,label:'航拍 · 场景布局',image:'03_Aerial_overview.png'},
  detail:{position:[7,1.72,7],target:[1,2.1,0],lens:27,label:'近景 · 墙面与花盆',image:'04_Ground_detail.png'}
};
const scene=new THREE.Scene();
scene.background=new THREE.Color('#adc4d3');
scene.fog=new THREE.Fog('#adc4d3',110,240);
const camera=new THREE.PerspectiveCamera(40,1,.08,500);
let renderer,controls,model,tween,dirty=true,wireframe=false;
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
function fail(error){
  state.error=String(error);$('loading').hidden=false;
  $('loading-title').textContent='三维预览未能载入';
  $('loading-text').textContent='可先查看渲染对照，再尝试重新加载';
  $('retry').hidden=false;
  console.error(error);
}
$('retry').onclick=()=>location.reload();
applyView('oblique',true);
try{
  renderer=new THREE.WebGLRenderer({canvas:$('viewport'),antialias:true,alpha:false});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.6));
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure=1;
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFShadowMap;
  const pmrem=new THREE.PMREMGenerator(renderer);
  const room=new RoomEnvironment();
  scene.environment=pmrem.fromScene(room,.04).texture;
  room.dispose();pmrem.dispose();
  scene.environmentIntensity=.55;
  scene.add(new THREE.HemisphereLight(0xd9ebff,0x746b55,2));
  const sun=new THREE.DirectionalLight(0xfff4dc,3);
  sun.position.set(-22,32,18);sun.target.position.set(0,0,-2);
  sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);
  Object.assign(sun.shadow.camera,{left:-42,right:42,top:42,bottom:-42,near:1,far:120});
  sun.shadow.normalBias=.025;sun.shadow.bias=-.00015;
  scene.add(sun,sun.target);
  controls=new OrbitControls(camera,renderer.domElement);
  controls.enableDamping=true;controls.dampingFactor=.08;
  controls.minDistance=1.2;controls.maxDistance=105;
  controls.maxPolarAngle=Math.PI*.53;
  controls.autoRotateSpeed=.5;
  controls.addEventListener('change',()=>dirty=true);
  controls.addEventListener('start',()=>tween=null);
  new ResizeObserver(resize).observe($('stage'));
  applyView('oblique',true);
  const draco=new DRACOLoader();
  draco.setDecoderPath('./node_modules/three/examples/jsm/libs/draco/gltf/');
  draco.setWorkerLimit(2);
  const loader=new GLTFLoader().setDRACOLoader(draco);
  loader.load('./assets/south-gate.glb',gltf=>{
    model=gltf.scene;
    const paving=makePaving();let meshes=0,triangles=0;
    model.traverse(o=>{
      if(!o.isMesh)return;
      meshes++;triangles+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;
      o.castShadow=true;o.receiveShadow=true;
      for(const m of Array.isArray(o.material)?o.material:[o.material]){
        if(m.map)m.map.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
        if(m.name.startsWith('Granite rectangular paving')){
          m.map=paving;m.color.set(0xffffff);m.roughness=.86;
          m.onBeforeCompile=shader=>{
            shader.vertexShader='varying vec3 vPavingWorld;\n'+shader.vertexShader;
            shader.vertexShader=shader.vertexShader.replace('#include <worldpos_vertex>','#include <worldpos_vertex>\nvPavingWorld=(modelMatrix*vec4(transformed,1.0)).xyz;');
            shader.fragmentShader='varying vec3 vPavingWorld;\n'+shader.fragmentShader;
            shader.fragmentShader=shader.fragmentShader.replace('#include <map_fragment>','diffuseColor *= texture2D(map,vPavingWorld.xz/vec2(3.4,2.72));');
          };
          m.customProgramCacheKey=()=> 'wzms-paving-v1';m.needsUpdate=true;
        }
      }
    });
    scene.add(model);state.ready=true;state.meshes=meshes;state.triangles=triangles;
    $('loading').hidden=true;dirty=true;draco.dispose();
    document.body.dataset.ready='true';
  },event=>{
    const ratio=event.total?event.loaded/event.total:Math.min(.8,event.loaded/12000000);
    $('progress').style.width=`${Math.round(ratio*95)}%`;
    $('loading-text').textContent=ratio>.98?'正在准备三维画面…':`读取模型 ${Math.round(ratio*100)}%`;
  },fail);
  let last=performance.now();
  renderer.setAnimationLoop(now=>{
    const dt=Math.min(.05,(now-last)/1000);last=now;
    if(tween){
      const x=Math.min(1,(now-tween.start)/650);const t=1-(1-x)**3;
      camera.position.lerpVectors(tween.from,tween.to,t);
      controls.target.lerpVectors(tween.targetFrom,tween.targetTo,t);
      dirty=true;if(x===1)tween=null;
    }
    const changed=controls.update(dt);
    if(state.mode==='interactive'&&(dirty||changed||controls.autoRotate)){
      renderer.render(scene,camera);dirty=false;
      state.camera=camera.position.toArray();state.drawCalls=renderer.info.render.calls;
    }
  });
}catch(error){fail(error);}

function resize(){
  if(!renderer)return;
  const {width,height}=$('stage').getBoundingClientRect();
  renderer.setSize(width,height,false);camera.aspect=width/height;camera.updateProjectionMatrix();dirty=true;
  applyView(state.view,true);
}
function applyView(key,instant=false){
  state.view=key;const p=presets[key];
  $('view-label').textContent=p.label;
  $('render-image').src='./assets/'+p.image;
  $('render-image').alt=`南大门${p.label.split(' · ')[0]} Blender 渲染对照`;
  document.querySelectorAll('[data-view]').forEach(b=>{
    const selected=b.dataset.view===key;b.classList.toggle('selected',selected);b.setAttribute('aria-pressed',selected);
  });
  if(!controls)return;
  const damping=controls.enableDamping;
  controls.enableDamping=false;controls.update();controls.enableDamping=damping;
  controls.autoRotate=false;$('rotate').setAttribute('aria-pressed','false');
  camera.fov=THREE.MathUtils.radToDeg(2*Math.atan(36/(1.6*2*p.lens)));
  camera.updateProjectionMatrix();
  const to=new THREE.Vector3(...p.position),targetTo=new THREE.Vector3(...p.target);
  const rect=$('stage').getBoundingClientRect();
  to.sub(targetTo).multiplyScalar(Math.max(1,1.35/(rect.width/rect.height))).add(targetTo);
  if(instant||reduced){camera.position.copy(to);controls.target.copy(targetTo);tween=null;}
  else tween={from:camera.position.clone(),to,targetFrom:controls.target.clone(),targetTo,start:performance.now()};
  controls.update();dirty=true;
}
function setMode(mode){
  state.mode=mode;const render=mode==='rendered';
  document.body.classList.toggle('render-mode',render);
  $('viewport').hidden=render;$('render-image').hidden=!render;
  $('loading').hidden=render||state.ready;
  for(const id of ['interactive','rendered']){$(id).classList.toggle('selected',id===mode);$(id).setAttribute('aria-pressed',id===mode);}
  $('interaction-hint').textContent=render?'Blender 原始渲染 · 选择下方视角查看':'拖动旋转 · 滚轮缩放 · 右键平移 · 按 1–4 切换视角';
  dirty=true;resize();
}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>applyView(b.dataset.view));
$('interactive').onclick=()=>setMode('interactive');$('rendered').onclick=()=>setMode('rendered');
$('reset').onclick=()=>applyView(state.view);
$('rotate').onclick=()=>{if(!controls)return;tween=null;controls.autoRotate=!controls.autoRotate;$('rotate').setAttribute('aria-pressed',controls.autoRotate);dirty=true;};
$('wireframe').onclick=()=>{
  if(!model)return;wireframe=!wireframe;model.traverse(o=>{if(o.isMesh)for(const m of Array.isArray(o.material)?o.material:[o.material])m.wireframe=wireframe;});
  $('wireframe').setAttribute('aria-pressed',wireframe);dirty=true;
};
$('fullscreen').onclick=async()=>{
  try{if(document.fullscreenElement)await document.exitFullscreen();else await $('stage').requestFullscreen();}
  catch{$('interaction-hint').textContent='此浏览器不允许页面全屏，可以使用浏览器的全屏按钮。';}
};
document.addEventListener('keydown',e=>{if(e.ctrlKey||e.metaKey||e.altKey)return;const key=['front','oblique','aerial','detail'][Number(e.key)-1];if(key)applyView(key);});

function makePaving(){
  const canvas=document.createElement('canvas');canvas.width=canvas.height=1024;
  const ctx=canvas.getContext('2d');ctx.fillStyle='#898f8b';ctx.fillRect(0,0,1024,1024);
  let seed=349;const rnd=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
  for(let row=0;row<8;row++)for(let col=-1;col<5;col++){
    const x=col*256+(row%2)*128,y=row*128;const v=Math.floor(166+rnd()*24);
    ctx.fillStyle=`rgb(${v},${v+2},${v-1})`;ctx.fillRect(x+2,y+2,252,124);
    for(let i=0;i<170;i++){
      ctx.fillStyle=rnd()>.5?'#ffffff12':'#252a2210';ctx.fillRect(x+rnd()*250,y+rnd()*124,1+rnd()*3,1+rnd()*3);
    }
  }
  const texture=new THREE.CanvasTexture(canvas);texture.wrapS=texture.wrapT=THREE.RepeatWrapping;
  texture.colorSpace=THREE.SRGBColorSpace;texture.anisotropy=8;return texture;
}
