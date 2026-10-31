/* Pure timeline functions are also available to Node's built-in test runner. */
function timeline(scenes) {
  let total=0;
  const starts=scenes.map(scene=>{const start=total;total+=scene.seconds;return start;});
  return {total,starts,indexAt(time){let i=starts.length-1;while(i>0&&time<starts[i])i--;return i;}};
}
if(typeof module!=='undefined')module.exports={timeline};
if(typeof document!=='undefined'){
  const scenes=JSON.parse(document.getElementById('scene-data').textContent);
  const reel=timeline(scenes), $=id=>document.getElementById(id);
  let elapsed=0, current=-1, playing=false, previous=0;
  let frozen=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const stillCache=new Map();
  const format=t=>Math.floor(t/60)+':'+String(Math.floor(t%60)).padStart(2,'0');
  function still(src){
    if(stillCache.has(src))return stillCache.get(src);
    const xml=new TextDecoder().decode(Uint8Array.from(atob(src.split(',')[1]),c=>c.charCodeAt(0)));
    const doc=new DOMParser().parseFromString(xml,'image/svg+xml');
    doc.querySelectorAll('animate,animateTransform,animateMotion,set').forEach(el=>el.remove());
    const style=doc.createElementNS('http://www.w3.org/2000/svg','style');
    style.textContent='*{animation:none!important;transition:none!important}';
    doc.documentElement.append(style);
    const bytes=new TextEncoder().encode(new XMLSerializer().serializeToString(doc));
    let binary='';for(const byte of bytes)binary+=String.fromCharCode(byte);
    const result='data:image/svg+xml;base64,'+btoa(binary);stillCache.set(src,result);return result;
  }
  function renderArt(){
    const scene=scenes[current], art=document.createElement('div');
    art.className='art'+(scene.images.length>1?' multi':'')+(scene.images.length===4?' four':'');
    for(let i=0;i<scene.images.length;i++){
      const img=document.createElement('img');
      img.src=frozen?still(scene.images[i]):scene.images[i];
      img.alt=scene.title+' — '+scene.assets[i].split('/').pop().replace('.svg','').replaceAll('_',' ');
      art.append(img);
    }
    $('stage').replaceChildren(art);
    document.body.classList.toggle('still',frozen);
    $('motion').setAttribute('aria-pressed',String(frozen));
    $('motion').textContent=frozen?'Animate visuals':'Freeze visuals';
  }
  function render(){
    const index=reel.indexAt(elapsed);
    if(index!==current){
      current=index;const scene=scenes[current];
      $('chapter').textContent=scene.chapter;$('title').textContent=scene.title;$('line').textContent=scene.line;
      $('frame-count').textContent='SCENE '+String(current+1).padStart(2,'0')+' / '+String(scenes.length).padStart(2,'0');
      $('scene-link').hidden=!scene.url;
      if(scene.url){$('scene-link').href=scene.url;$('scene-link').textContent=(scene.link_label||'Explore the project')+' ↗';}
      $('tags').replaceChildren(...(scene.tags||[]).map(tag=>{const el=document.createElement('span');el.className='tag';el.textContent=tag;return el;}));
      $('chapters').querySelectorAll('button').forEach((button,i)=>button.setAttribute('aria-current',String(i===current)));
      const active=$('chapters').children[current];
      // Scroll only the horizontal scene rail, never the document.
      $('chapters').scrollLeft=Math.max(0,active.offsetLeft-$('chapters').offsetLeft-20);
      renderArt();
    }
    $('seek').value=elapsed;
    $('seek').setAttribute('aria-valuetext',format(elapsed)+' of '+format(reel.total));
    $('clock').textContent=format(elapsed)+' / '+format(reel.total);
    $('prev').disabled=current===0;$('next').disabled=current===scenes.length-1;
    $('play').textContent=playing?'Pause reel':elapsed>=reel.total?'Replay résumé':'Play résumé';
  }
  function pause(message){playing=false;previous=0;$('status').textContent=message||'Reel paused.';render();}
  function jump(index){elapsed=reel.starts[Math.max(0,Math.min(scenes.length-1,index))];previous=0;render();}
  $('play').onclick=()=>{if(playing){pause();return;}if(elapsed>=reel.total)elapsed=0;playing=true;previous=0;$('status').textContent='Now playing.';render();};
  $('prev').onclick=()=>jump(current-1);$('next').onclick=()=>jump(current+1);
  $('seek').max=reel.total;$('seek').oninput=()=>{elapsed=Math.max(0,Math.min(reel.total,Number($('seek').value)));previous=0;if(elapsed>=reel.total)pause('End of reel. Your next chapter starts here.');else render();};
  $('motion').onclick=()=>{frozen=!frozen;renderArt();};
  $('fullscreen').hidden=!document.fullscreenEnabled;
  $('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('screen').requestFullscreen();}catch{$('status').textContent='Fullscreen is unavailable in this browser.';}};
  document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Exit fullscreen':'Fullscreen';});
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&playing)pause('Paused while this tab was away.');});
  document.addEventListener('keydown',event=>{if(/^(INPUT|BUTTON|A|TEXTAREA|SELECT)$/.test(event.target.tagName)||event.altKey||event.ctrlKey||event.metaKey)return;if(event.code==='Space'){event.preventDefault();$('play').click();}else if(event.code==='ArrowRight'){event.preventDefault();jump(current+1);}else if(event.code==='ArrowLeft'){event.preventDefault();jump(current-1);}});
  scenes.forEach((scene,index)=>{const button=document.createElement('button'),small=document.createElement('small'),label=document.createElement('span');small.textContent=format(reel.starts[index])+' / '+scene.chapter.split(' / ')[0];label.textContent=scene.title;button.append(small,label);button.onclick=()=>jump(index);$('chapters').append(button);});
  function tick(now){if(playing){if(previous)elapsed=Math.min(reel.total,elapsed+(now-previous)/1000);previous=now;if(elapsed>=reel.total)pause('End of reel. Your next chapter starts here.');else render();}requestAnimationFrame(tick);}
  render();requestAnimationFrame(tick);
}
