// Menu mobile
(function(){
  const nav=document.getElementById('nav'), burger=document.querySelector('.burger');
  if(burger) burger.onclick=()=>nav.classList.toggle('open');
  // Sous-menu « Formations » : ouverture au clic sur mobile
  document.querySelectorAll('.has-sub > a').forEach(a=>a.addEventListener('click',e=>{
    if(window.innerWidth<=1100){e.preventDefault();a.parentElement.classList.toggle('open');}
  }));
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

// Test d'orientation « Quel métier est fait pour vous ? »
(function(){
  const card=document.getElementById('quiz-card');
  if(!card||!window.QUIZ||!window.METIERS) return;
  const metiers=window.METIERS, quiz=window.QUIZ;
  const rank=slug=>metiers.findIndex(m=>m.slug===slug);
  let step=0, score={};
  const progress=p=>`<div class="quiz-progress"><span style="width:${p}%"></span></div>`;
  const render=()=>{
    if(step<quiz.length){
      const q=quiz[step];
      card.innerHTML=progress(step/quiz.length*100)+
        `<p class="quiz-count">Question ${step+1} / ${quiz.length}</p><h3>${q.q}</h3>`+
        `<div class="quiz-answers">${q.r.map((r,i)=>`<button type="button" data-i="${i}">${r[0]}</button>`).join('')}</div>`;
      bind();
      if(step>0) card.querySelector('.quiz-answers button').focus();
      return;
    }
    const best=Object.keys(score).sort((a,b)=>score[b]-score[a]||rank(a)-rank(b))[0];
    const m=metiers[rank(best)];
    card.innerHTML=progress(100)+
      `<p class="quiz-count">Votre résultat</p>`+
      `<div class="quiz-result"><span class="m-ico"><svg class="ic"><use href="#${m.icon}"/></svg></span>`+
      `<div><h3>${m.titre}</h3><p>${m.accroche}</p></div></div>`+
      `<div class="quiz-actions"><a class="btn btn-red" href="formation-${m.slug}.html">Découvrir la formation</a>`+
      `<button type="button" class="btn btn-outline quiz-restart">Refaire le test</button></div>`;
    const again=card.querySelector('.quiz-restart');
    again.onclick=()=>{step=0;score={};render();card.querySelector('.quiz-answers button').focus();};
    card.querySelector('.quiz-actions a').focus();
  };
  // Les réponses de la première question sont déjà dans la page
  const bind=()=>card.querySelectorAll('.quiz-answers button').forEach(b=>b.onclick=()=>{
    const pts=quiz[step].r[+b.dataset.i][1];
    for(const k in pts) score[k]=(score[k]||0)+pts[k];
    step++; render();
  });
  bind();
})();

// Prise de rendez-vous : la demande est rédigée puis ouverte dans WhatsApp
(function(){
  const form=document.getElementById('form-rdv');
  if(!form) return;
  const date=form.elements.date, dateErr=document.getElementById('rdv-date-err'), slotErr=document.getElementById('rdv-slot-err');
  const ok=document.getElementById('rdv-ok');
  const pad=n=>String(n).padStart(2,'0');
  const demain=new Date(); demain.setDate(demain.getDate()+1);
  date.min=demain.getFullYear()+'-'+pad(demain.getMonth()+1)+'-'+pad(demain.getDate());
  const weekend=v=>{const j=new Date(v+'T12:00:00').getDay();return j===0||j===6;};
  date.addEventListener('change',()=>{dateErr.hidden=!(date.value&&weekend(date.value));});
  form.addEventListener('change',e=>{if(e.target.name==='creneau') slotErr.hidden=true;});
  // Formation présélectionnée depuis une fiche métier (?formation=cuisinier)
  const f=new URLSearchParams(location.search).get('formation');
  if(f&&form.elements.formation.querySelector(`option[value="${CSS.escape(f)}"]`)) form.elements.formation.value=f;
  form.addEventListener('submit',e=>{
    e.preventDefault();
    const el=form.elements, slot=form.querySelector('input[name="creneau"]:checked');
    const mauvaisJour=!!date.value&&weekend(date.value);
    dateErr.hidden=!mauvaisJour; slotErr.hidden=!!slot;
    if(!form.checkValidity()){form.reportValidity();return;}
    if(mauvaisJour){date.focus();return;}
    const jour=new Date(date.value+'T12:00:00').toLocaleDateString('fr-FR',{weekday:'long',day:'numeric',month:'long',year:'numeric'});
    const formation=el.formation.value?el.formation.selectedOptions[0].textContent:'Je ne sais pas encore';
    const lignes=['Bonjour EchoResta, je souhaite prendre rendez-vous.','',
      'Motif : '+form.querySelector('input[name="motif"]:checked').value,
      'Formation : '+formation,
      'Date souhaitée : '+jour+', '+slot.value,
      'Nom : '+el.nom.value.trim(),
      'Téléphone : '+el.tel.value.trim()];
    if(el.email.value.trim()) lignes.push('E-mail : '+el.email.value.trim());
    lignes.push('Confirmation par : '+el.confirmation.value);
    if(el.message.value.trim()) lignes.push('','Message : '+el.message.value.trim());
    const texte=lignes.join('\n'), lien='https://wa.me/'+form.dataset.wa+'?text='+encodeURIComponent(texte);
    document.getElementById('rdv-recap').textContent=texte;
    document.getElementById('rdv-wa').href=lien;
    form.hidden=true; ok.hidden=false; ok.scrollIntoView({block:'start'});
    window.open(lien,'_blank','noopener');
  });
  document.getElementById('rdv-again').onclick=()=>{ok.hidden=true;form.hidden=false;form.scrollIntoView({block:'start'});};
})();
