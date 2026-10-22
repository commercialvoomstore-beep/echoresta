// Menu mobile
(function(){
  const nav=document.getElementById('nav'), burger=document.querySelector('.burger');
  if(burger) burger.onclick=()=>nav.classList.toggle('open');
  // Sous-menu « Formations » : ouverture au clic sur mobile
  document.querySelectorAll('.has-sub > a').forEach(a=>a.addEventListener('click',e=>{
    if(window.innerWidth<=900){e.preventDefault();a.parentElement.classList.toggle('open');}
  }));
})();

// Carrousel des témoignages
(function(){
  const slides=[...document.querySelectorAll('.slide')];
  if(!slides.length) return;
  let i=0, timer;
  const show=n=>{slides[i].classList.remove('active');i=(n+slides.length)%slides.length;slides[i].classList.add('active');};
  const auto=()=>{clearInterval(timer);timer=setInterval(()=>show(i+1),7000);};
  document.querySelector('.arrow.prev').onclick=()=>{show(i-1);auto();};
  document.querySelector('.arrow.next').onclick=()=>{show(i+1);auto();};
  auto();
})();

// Compteurs animés des chiffres clés
(function(){
  const nums=document.querySelectorAll('.num[data-to]');
  const end=el=>el.dataset.to+(el.dataset.suffix||'');
  const run=el=>{
    const to=+el.dataset.to, suf=el.dataset.suffix||'', t0=performance.now(), d=1600;
    const step=t=>{const p=Math.min((t-t0)/d,1);el.textContent=Math.round(to*(1-Math.pow(1-p,3)))+suf;if(p<1)requestAnimationFrame(step);};
    requestAnimationFrame(step);
  };
  if(!('IntersectionObserver' in window)){nums.forEach(el=>el.textContent=end(el));return;}
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){run(e.target);io.unobserve(e.target);}}),{threshold:.5});
  nums.forEach(el=>io.observe(el));
})();

// Filtres du catalogue des formations
(function(){
  const btns=document.querySelectorAll('.filters button');
  if(!btns.length) return;
  btns.forEach(b=>b.onclick=()=>{
    btns.forEach(x=>x.classList.toggle('active',x===b));
    document.querySelectorAll('.course').forEach(c=>{
      c.style.display=(b.dataset.f==='all'||c.dataset.cat===b.dataset.f)?'':'none';
    });
  });
})();

// Formulaire de contact / inscription
(function(){
  const form=document.getElementById('form-contact');
  if(!form) return;
  // Pré-sélection de la formation via ?formation=cuisine
  const f=new URLSearchParams(location.search).get('formation');
  if(f && form.formation.querySelector(`option[value="${CSS.escape(f)}"]`)){form.formation.value=f;form.objet.value='inscription';}
  form.addEventListener('submit',e=>{
    e.preventDefault();
    if(!form.checkValidity()){form.reportValidity();return;}
    // À brancher sur votre service d'envoi (Formspree, PHP, etc.)
    form.hidden=true;
    document.getElementById('form-ok').hidden=false;
  });
})();

// Recherche
(function(){
  const box=document.getElementById('search'), btn=document.querySelector('.search-btn');
  if(!box||!btn) return;
  const input=document.getElementById('search-input'), list=document.getElementById('search-results');
  const data=window.SEARCH_INDEX||[];
  const norm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
  const render=q=>{
    const terms=norm(q).split(/\s+/).filter(Boolean);
    const hits=terms.length?data.filter(it=>{const h=norm(it.t+' '+it.d+' '+(it.k||''));return terms.every(t=>h.includes(t));}):data;
    list.innerHTML=hits.length?hits.map(it=>`<li><a href="${it.u}"><b>${it.t}</b><span>${it.d}</span></a></li>`).join(''):'<li class="empty">Aucun résultat.</li>';
  };
  const open=()=>{box.hidden=false;render('');input.value='';setTimeout(()=>input.focus(),30);};
  const close=()=>{box.hidden=true;};
  btn.onclick=open;
  box.querySelector('.search-close').onclick=close;
  box.addEventListener('click',e=>{if(e.target===box)close();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')close();});
  input.addEventListener('input',()=>render(input.value));
  input.addEventListener('keydown',e=>{if(e.key==='Enter'){const a=list.querySelector('a');if(a)location.href=a.href;}});
})();
