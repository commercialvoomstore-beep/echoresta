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

// Envoi des formulaires par e-mail (service FormSubmit, sans serveur à gérer).
// En cas d'échec, le visiteur peut envoyer la même demande depuis sa messagerie.
const envoyerEmail=(dest,sujet,champs)=>fetch('https://formsubmit.co/ajax/'+dest,{
  method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},
  body:JSON.stringify(Object.assign({},champs,{_subject:sujet,_template:'table',_replyto:champs['E-mail']||''}))
}).then(r=>r.json()).then(d=>d.success===true||d.success==='true').catch(()=>false);
const texteDemande=champs=>Object.entries(champs).filter(([,v])=>v).map(([k,v])=>k+' : '+v).join('\n');
const lienMail=(dest,sujet,texte)=>'mailto:'+dest+'?subject='+encodeURIComponent(sujet)+'&body='+encodeURIComponent(texte);
const afficherEchec=(el,dest,sujet,texte)=>{
  el.innerHTML='L’envoi n’a pas abouti. <a class="link" href="'+lienMail(dest,sujet,texte)+'">Envoyez la demande depuis votre messagerie</a> ou appelez-nous au +225 07 68 84 20 38.';
  el.hidden=false;
};

// Formulaire de contact / inscription
(function(){
  const form=document.getElementById('form-contact');
  if(!form) return;
  // Pré-sélection de la formation via ?formation=cuisinier
  const f=new URLSearchParams(location.search).get('formation');
  if(f && form.formation.querySelector(`option[value="${CSS.escape(f)}"]`)){form.formation.value=f;form.objet.value='inscription';}
  const btn=form.querySelector('button[type="submit"]'), err=document.getElementById('contact-err');
  form.addEventListener('submit',e=>{
    e.preventDefault();
    if(!form.checkValidity()){form.reportValidity();return;}
    const champs={'Nom':form.nom.value.trim(),'Téléphone':form.tel.value.trim(),'E-mail':form.email.value.trim(),
      'Objet':form.objet.selectedOptions[0].textContent,
      'Formation':form.formation.value?form.formation.selectedOptions[0].textContent:'Je ne sais pas encore',
      'Message':form.message.value.trim()};
    const sujet='Site EchoResta : '+champs['Objet']+' – '+champs['Nom'];
    btn.disabled=true; btn.textContent='Envoi en cours…'; err.hidden=true;
    envoyerEmail(form.dataset.mail,sujet,champs).then(ok=>{
      btn.disabled=false; btn.textContent='Envoyer ma demande';
      if(ok){form.hidden=true;document.getElementById('form-ok').hidden=false;}
      else afficherEchec(err,form.dataset.mail,sujet,texteDemande(champs));
    });
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

// Prise de rendez-vous : la demande est envoyée par e-mail à l'école
(function(){
  const form=document.getElementById('form-rdv');
  if(!form) return;
  const date=form.elements.date, dateErr=document.getElementById('rdv-date-err'), slotErr=document.getElementById('rdv-slot-err');
  const ok=document.getElementById('rdv-ok'), err=document.getElementById('rdv-err'), btn=form.querySelector('.rdv-submit');
  const btnHtml=btn.innerHTML;
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
    dateErr.hidden=!mauvaisJour; slotErr.hidden=!!slot; err.hidden=true;
    if(!form.checkValidity()){form.reportValidity();return;}
    if(mauvaisJour){date.focus();return;}
    const jour=new Date(date.value+'T12:00:00').toLocaleDateString('fr-FR',{weekday:'long',day:'numeric',month:'long',year:'numeric'});
    const champs={'Motif':form.querySelector('input[name="motif"]:checked').value,
      'Formation':el.formation.value?el.formation.selectedOptions[0].textContent:'Je ne sais pas encore',
      'Date souhaitée':jour+', '+slot.value,
      'Nom':el.nom.value.trim(),'Téléphone':el.tel.value.trim(),'E-mail':el.email.value.trim(),
      'Confirmation par':el.confirmation.value,'Message':el.message.value.trim()};
    const sujet='Demande de rendez-vous : '+champs['Motif']+' – '+champs['Nom'];
    btn.disabled=true; btn.textContent='Envoi en cours…';
    envoyerEmail(form.dataset.mail,sujet,champs).then(envoye=>{
      btn.disabled=false; btn.innerHTML=btnHtml;
      if(!envoye){afficherEchec(err,form.dataset.mail,sujet,texteDemande(champs));return;}
      document.getElementById('rdv-recap').textContent=texteDemande(champs);
      form.hidden=true; ok.hidden=false; ok.scrollIntoView({block:'start'});
    });
  });
  document.getElementById('rdv-again').onclick=()=>{ok.hidden=true;form.reset();form.hidden=false;form.scrollIntoView({block:'start'});};
})();

// Listes déroulantes avec drapeaux (pays, indicatif téléphonique)
const listesDrapeaux={};
(function(){
  const sans=t=>t.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
  document.querySelectorAll('.flag-select').forEach(box=>{
    const btn=box.querySelector('.fs-btn'), list=box.querySelector('.fs-list'), input=box.querySelector('input[type="hidden"]');
    const opts=[...list.querySelectorAll('[role="option"]')], courant=btn.querySelector('.fs-current');
    const autre=document.getElementById(box.dataset.field+'-autre-txt'), err=document.getElementById(box.dataset.field+'-err');
    let actif=0, recherche='', minuterie;
    const marquer=i=>{actif=Math.max(0,Math.min(opts.length-1,i));opts.forEach((o,k)=>o.classList.toggle('active',k===actif));
      list.setAttribute('aria-activedescendant',opts[actif].id);opts[actif].scrollIntoView({block:'nearest'});};
    const ouvrir=()=>{list.hidden=false;btn.setAttribute('aria-expanded','true');const sel=opts.findIndex(o=>o.getAttribute('aria-selected')==='true');marquer(sel<0?0:sel);list.focus();};
    const fermer=(focus=true)=>{list.hidden=true;btn.setAttribute('aria-expanded','false');if(focus)btn.focus();};
    const choisir=(i,parUtilisateur=true)=>{const o=opts[i];opts.forEach(x=>x.setAttribute('aria-selected',x===o?'true':'false'));
      input.value=o.dataset.value;courant.innerHTML=o.innerHTML;box.classList.add('filled');if(err)err.hidden=true;
      const estAutre=!o.dataset.tel;
      if(autre){autre.hidden=!estAutre;autre.required=estAutre;if(estAutre&&parUtilisateur)setTimeout(()=>autre.focus(),0);}
      if(parUtilisateur) box.dataset.manuel='1';
      input.dispatchEvent(new CustomEvent('change',{bubbles:true,detail:{tel:o.dataset.tel,autre:estAutre}}));};
    btn.addEventListener('click',()=>list.hidden?ouvrir():fermer());
    btn.addEventListener('keydown',e=>{if(['ArrowDown','ArrowUp'].includes(e.key)){e.preventDefault();ouvrir();}});
    opts.forEach((o,i)=>{o.addEventListener('click',()=>{choisir(i);fermer();});o.addEventListener('mousemove',()=>marquer(i));});
    list.addEventListener('keydown',e=>{
      if(e.key==='ArrowDown'){e.preventDefault();marquer(actif+1);}
      else if(e.key==='ArrowUp'){e.preventDefault();marquer(actif-1);}
      else if(e.key==='Home'){e.preventDefault();marquer(0);}
      else if(e.key==='End'){e.preventDefault();marquer(opts.length-1);}
      else if(e.key==='Enter'||e.key===' '){e.preventDefault();choisir(actif);fermer();}
      else if(e.key==='Escape'||e.key==='Tab'){fermer(e.key==='Escape');}
      else if(e.key.length===1){clearTimeout(minuterie);recherche+=e.key.toLowerCase();minuterie=setTimeout(()=>recherche='',700);
        const k=opts.findIndex(o=>sans(o.textContent).startsWith(sans(recherche))||o.dataset.value.startsWith(recherche));if(k>=0)marquer(k);}
    });
    document.addEventListener('click',e=>{if(!list.hidden&&!box.contains(e.target))fermer(false);});
    const parValeur=v=>{const k=opts.findIndex(o=>o.dataset.value===v);if(k>=0)choisir(k,false);};
    if(box.dataset.default) parValeur(box.dataset.default);
    listesDrapeaux[box.dataset.field]={btn,input,
      valide:()=>{const ok=!!input.value;if(err)err.hidden=ok;return ok;},
      // Change la valeur sans écraser un choix fait à la main par le visiteur
      proposer:v=>{if(!box.dataset.manuel)parValeur(v);}};
  });
})();

// Fiche de candidature (page Inscription)
(function(){
  const form=document.getElementById('form-inscription');
  if(!form) return;
  const el=form.elements, btn=form.querySelector('button[type="submit"]'), err=document.getElementById('ins-err');
  const tuteur=document.getElementById('ins-tuteur'), numFin=form.querySelector('.num-tuteur');
  const NAT=JSON.parse(form.dataset.nationalites);
  const f=new URLSearchParams(location.search).get('formation');
  if(f&&el.formation.querySelector(`option[value="${CSS.escape(f)}"]`)) el.formation.value=f;
  // Date de naissance : pas dans le futur ; parent ou tuteur demandé avant 18 ans
  const pad=n=>String(n).padStart(2,'0'), auj=new Date();
  el.naissance.max=auj.getFullYear()+'-'+pad(auj.getMonth()+1)+'-'+pad(auj.getDate());
  const age=v=>{const d=new Date(v+'T12:00:00');let a=auj.getFullYear()-d.getFullYear();const m=auj.getMonth()-d.getMonth();if(m<0||(m===0&&auj.getDate()<d.getDate()))a--;return a;};
  el.naissance.addEventListener('change',()=>{
    const mineur=!!el.naissance.value&&age(el.naissance.value)<18;
    tuteur.hidden=!mineur; numFin.textContent=mineur?'6':'5';
    tuteur.querySelectorAll('[data-req]').forEach(x=>x.required=mineur);
  });
  // Nationalité remplie automatiquement selon le pays et le sexe (modifiable)
  let natAuto='';
  const remplirNationalite=()=>{
    const sexe=form.querySelector('input[name="sexe"]:checked'), n=NAT[el.pays.value];
    if(!sexe||!n) return;
    if(!el.nationalite.value.trim()||el.nationalite.value===natAuto){natAuto=n[sexe.value];el.nationalite.value=natAuto;}
  };
  form.querySelectorAll('input[name="sexe"]').forEach(r=>r.addEventListener('change',remplirNationalite));
  el.pays.addEventListener('change',e=>{
    remplirNationalite();
    // Indicatif des téléphones calé sur le pays, tant que le visiteur ne l'a pas changé
    if(e.detail&&e.detail.tel) ['tel_ind','tel2_ind'].forEach(k=>listesDrapeaux[k].proposer(e.detail.tel));
  });
  const numero=k=>{const n=(el[k].value||'').trim(), ind=el[k+'_ind'].value;return n?(ind&&ind!=='Autre'&&!n.startsWith('+')?ind+' '+n:n):'';};
  form.addEventListener('submit',e=>{
    e.preventDefault(); err.hidden=true;
    const paysOk=listesDrapeaux.pays.valide();
    if(!form.checkValidity()){form.reportValidity();return;}
    if(!paysOk){listesDrapeaux.pays.btn.focus();listesDrapeaux.pays.btn.scrollIntoView({block:'center'});return;}
    const val=x=>(x&&x.value||'').trim(), choix=x=>x.value?x.selectedOptions[0].textContent:'';
    const pays=/^Autre/.test(el.pays.value)&&val(el.pays_autre)?val(el.pays_autre):el.pays.value;
    const jour=new Date(el.naissance.value+'T12:00:00').toLocaleDateString('fr-FR',{day:'numeric',month:'long',year:'numeric'});
    const champs={'Nom':val(el.nom).toUpperCase(),'Prénom(s)':val(el.prenoms),
      'Date de naissance':jour+' ('+age(el.naissance.value)+' ans)','Lieu de naissance':val(el.lieu_naissance),
      'Pays':pays,'Sexe':form.querySelector('input[name="sexe"]:checked').value,'Nationalité':val(el.nationalite),
      'Pièce d’identité':[choix(el.piece),val(el.piece_numero)].filter(Boolean).join(' n° '),
      'Adresse':val(el.adresse),'Ville / Commune':val(el.ville),'E-mail':val(el.email),
      'Téléphone principal':numero('tel'),'Téléphone secondaire':numero('tel2'),
      'Niveau d’études':choix(el.niveau),'Dernier diplôme':val(el.diplome),
      'Formation':choix(el.formation),'Situation actuelle':choix(el.situation),'Expérience':choix(el.experience)};
    if(!tuteur.hidden) Object.assign(champs,{'Parent ou tuteur':val(el.tuteur_nom),'Lien de parenté':choix(el.tuteur_lien),'Téléphone du tuteur':val(el.tuteur_tel)});
    Object.assign(champs,{'Contact en cas d’urgence':val(el.urgence),'Connu par':choix(el.connu),'Projet professionnel':val(el.motivation)});
    const sujet='Candidature : '+champs['Formation']+' – '+champs['Prénom(s)']+' '+champs['Nom'];
    btn.disabled=true; btn.textContent='Envoi en cours…';
    envoyerEmail(form.dataset.mail,sujet,champs).then(ok=>{
      btn.disabled=false; btn.textContent='Envoyer ma candidature';
      if(!ok){afficherEchec(err,form.dataset.mail,sujet,texteDemande(champs));return;}
      document.getElementById('ins-recap').textContent=texteDemande(champs);
      form.hidden=true; const box=document.getElementById('ins-ok'); box.hidden=false; box.scrollIntoView({block:'start'});
    });
  });
})();
