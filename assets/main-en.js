// Menu mobile
(function(){
  const nav=document.getElementById('nav'), burger=document.querySelector('.burger');
  if(burger) burger.onclick=()=>nav.classList.toggle('open');
  // Sous-menu « Formations » : ouverture au clic sur mobile
  document.querySelectorAll('.has-sub > a').forEach(a=>a.addEventListener('click',e=>{
    if(window.innerWidth<=1280){e.preventDefault();a.parentElement.classList.toggle('open');}
  }));
})();

// Dates au format jj/mm/aaaa, quelle que soit la langue du navigateur (saisie au clavier ou calendrier)
(function(){
  const pad=n=>String(n).padStart(2,'0'), versFr=iso=>iso.split('-').reverse().join('/');
  document.querySelectorAll('.date-fr').forEach(box=>{
    const txt=box.querySelector('input[type="text"]'), nat=box.querySelector('.date-native');
    let interne=false;
    const valider=()=>{
      const d=txt.value.replace(/\D/g,'');let iso='', msg='';
      if(d.length===8){
        const j=+d.slice(0,2), m=+d.slice(2,4), a=+d.slice(4), dt=new Date(a,m-1,j);
        if(a<1900||dt.getFullYear()!==a||dt.getMonth()!==m-1||dt.getDate()!==j) msg='This date does not exist: please check the day and month.';
        else{iso=a+'-'+pad(m)+'-'+pad(j);
          if(nat.min&&iso<nat.min) msg='Choose a date from '+versFr(nat.min)+'.';
          else if(nat.max&&iso>nat.max) msg='The date cannot be later than '+versFr(nat.max)+'.';}
      } else if(d.length) msg='Enter the date in the format dd/mm/yyyy.';
      txt.setCustomValidity(msg);
      const v=msg?'':iso;
      if(nat.value!==v){nat.value=v;interne=true;nat.dispatchEvent(new Event('change',{bubbles:true}));interne=false;}
    };
    txt.addEventListener('input',e=>{
      if(!(e.inputType||'').startsWith('delete')){
        const d=txt.value.replace(/\D/g,'').slice(0,8);
        txt.value=d.length>4?d.slice(0,2)+'/'+d.slice(2,4)+'/'+d.slice(4):d.length>2?d.slice(0,2)+'/'+d.slice(2):d;
      }
      valider();
    });
    // Date choisie dans le calendrier du navigateur
    nat.addEventListener('change',()=>{if(!interne){txt.value=nat.value?versFr(nat.value):'';valider();}});
    nat.addEventListener('click',()=>{try{nat.showPicker();}catch(_){}});
    if(txt.form) txt.form.addEventListener('reset',()=>setTimeout(valider,0));
  });
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

// Envoi des formulaires : la fonction /api/envoyer (voir api/envoyer.js) enregistre la demande dans la base Neon
// et l'envoie par e-mail dans la boîte Microsoft 365 de l'école (contact@voomnetformation.ci).
// Si elle échoue, le visiteur peut envoyer la même demande sur WhatsApp (afficherEchec).
const emailDe=champs=>Object.values(champs).find(v=>/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(v).trim()))||'';
// Réponse : {ok, numero, documents} (numero = référence de la demande dans la base) ; {ok:false} en cas d'échec.
// sections : [[titre, [libellés…]], …] pour regrouper les réponses dans les e-mails et le récapitulatif.
// fichiers : [{id, cle}, …] documents déjà envoyés à /api/fichier (fiche candidat).
// Le texte de la case de consentement cochée est enregistré avec la demande.
const consentementDe=form=>{const c=form.querySelector('input[type="checkbox"][required]:not([name])');return c&&c.checked?c.closest('label').textContent.replace(/\s+/g,' ').trim():'';};
const envoyerEmail=(form,sujet,champs,sections=[],fichiers=[])=>fetch('/api/envoyer',{
  method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},
  body:JSON.stringify({sujet,champs,sections,fichiers,formulaire:form.id,replyto:emailDe(champs),page:location.pathname,
    langue:document.documentElement.lang,consentement:consentementDe(form),botcheck:!!(form.elements.botcheck&&form.elements.botcheck.checked)})
}).then(r=>r.ok?r.json():{}).then(d=>d&&d.ok===true?d:{ok:false}).catch(()=>({ok:false}));
// Taille d'un fichier lisible : « 240 Ko », « 1,2 Mo »
const tailleLisible=n=>n<1048576?Math.max(1,Math.round(n/1024))+' KB':(n/1048576).toLocaleString('en-GB',{maximumFractionDigits:1})+' MB';
// Récapitulatif affiché après l'envoi : référence de la demande, puis les réponses regroupées par section
// documents : [{champ, nom, taille, ok}] (fiche candidat), affichés dans une section « Vos documents »
const afficherRecap=(el,champs,sections,numero,documents=[])=>{
  const creer=(balise,classe,texte)=>{const x=document.createElement(balise);if(classe)x.className=classe;if(texte!=null)x.textContent=texte;return x;};
  const vus=new Set(), groupes=[];
  for(const [titre,cles] of sections){const l=cles.filter(k=>champs[k]);l.forEach(k=>vus.add(k));if(l.length)groupes.push([titre,l]);}
  const reste=Object.keys(champs).filter(k=>champs[k]&&!vus.has(k));
  if(reste.length)groupes.push([groupes.length?'Other information':'',reste]);
  el.textContent='';
  if(numero){const ref=creer('div','recap-ref','Your request reference');ref.append(creer('b','','no. '+numero));el.append(ref);}
  for(const [titre,cles] of groupes){
    const s=creer('div','recap-section');if(titre)s.append(creer('h4','',titre));
    const dl=creer('dl');cles.forEach(k=>dl.append(creer('dt','',k),creer('dd','',champs[k])));
    s.append(dl);el.append(s);
  }
  if(documents.length){
    const s=creer('div','recap-section');s.append(creer('h4','','Your documents'));
    const dl=creer('dl');documents.forEach(f=>dl.append(creer('dt','',f.champ),creer('dd',f.ok?'':'recap-ko',f.nom+' · '+(f.ok?tailleLisible(f.taille):'not received'))));
    s.append(dl);el.append(s);
  }
  el.hidden=false;
};
const texteDemande=champs=>Object.entries(champs).filter(([,v])=>v).map(([k,v])=>k+' : '+v).join('\n');
const afficherEchec=(el,form,sujet,texte)=>{
  const wa='https://wa.me/'+form.dataset.wa+'?text='+encodeURIComponent(sujet+'\n\n'+texte);
  el.innerHTML='Sending failed. <a class="link" href="'+wa+'" target="_blank" rel="noopener">Send the request on WhatsApp</a> (message already written) or call us on +225 07 68 84 20 38.';
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
    const champs={'Last name':form.nom.value.trim(),'Phone':form.tel.value.trim(),'E-mail':form.email.value.trim(),
      'Subject':form.objet.selectedOptions[0].textContent,
      'Course':form.formation.value?form.formation.selectedOptions[0].textContent:'I don’t know yet',
      'Message':form.message.value.trim()};
    const sujet='Site EchoResta : '+champs['Subject']+' – '+champs['Last name'];
    const sections=[['Your contact details',['Last name','Phone','E-mail']],['Your request',['Subject','Course','Message']]];
    btn.disabled=true; btn.textContent='Sending…'; err.hidden=true;
    envoyerEmail(form,sujet,champs,sections).then(rep=>{
      btn.disabled=false; btn.textContent='Send my request';
      if(!rep.ok){afficherEchec(err,form,sujet,texteDemande(champs));return;}
      afficherRecap(document.getElementById('contact-recap'),champs,sections,rep.numero);
      form.hidden=true; const box=document.getElementById('form-ok'); box.hidden=false; box.scrollIntoView({block:'start'});
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
    list.innerHTML=hits.length?hits.map(it=>`<li><a href="${it.u}"><b>${it.t}</b><span>${it.d}</span></a></li>`).join(''):'<li class="empty">No results.</li>';
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
      `<p class="quiz-count">Your result</p>`+
      `<div class="quiz-result"><span class="m-ico"><svg class="ic"><use href="#${m.icon}"/></svg></span>`+
      `<div><h3>${m.titre}</h3><p>${m.accroche}</p></div></div>`+
      `<div class="quiz-actions"><a class="btn btn-red" href="formation-${m.slug}">Discover the course</a>`+
      `<button type="button" class="btn btn-outline quiz-restart">Take the test again</button></div>`;
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
  const el=form.elements, date=el.date, heure=el.heure, dateErr=document.getElementById('rdv-date-err');
  const ok=document.getElementById('rdv-ok'), err=document.getElementById('rdv-err'), btn=form.querySelector('.rdv-submit');
  const btnTexte=btn.textContent, premiere=heure.options[0];
  const pad=n=>String(n).padStart(2,'0');
  const demain=new Date(); demain.setDate(demain.getDate()+1);
  date.min=demain.getFullYear()+'-'+pad(demain.getMonth()+1)+'-'+pad(demain.getDate());
  const weekend=v=>{const j=new Date(v+'T12:00:00').getDay();return j===0||j===6;};
  // L'heure se choisit une fois un jour ouvré sélectionné
  const majHeure=()=>{
    const okJour=!!date.value&&!weekend(date.value);
    dateErr.hidden=!(date.value&&weekend(date.value));
    heure.disabled=!okJour; premiere.textContent=okJour?'— Choose a time —':'Choose a date first';
    if(!okJour) heure.value='';
  };
  date.addEventListener('change',majHeure); date.addEventListener('input',majHeure);
  // Formation présélectionnée depuis une fiche métier (?formation=cuisinier)
  const f=new URLSearchParams(location.search).get('formation');
  if(f&&el.formation.querySelector(`option[value="${CSS.escape(f)}"]`)) el.formation.value=f;
  form.addEventListener('submit',e=>{
    e.preventDefault(); err.hidden=true; majHeure();
    if(date.value&&weekend(date.value)){document.getElementById('rdv-date').focus();return;}
    if(!form.checkValidity()){form.reportValidity();return;}
    const tel=el.rdv_tel.value.trim(), ind=el.rdv_tel_ind.value;
    const jour=new Date(date.value+'T12:00:00').toLocaleDateString('en-GB',{weekday:'long',day:'numeric',month:'long',year:'numeric'});
    const champs={'Full name':el.nom.value.trim(),
      'Phone / WhatsApp':ind&&ind!=='Other'&&!tel.startsWith('+')?ind+' '+tel:tel,
      'E-mail':el.email.value.trim(),
      'Preferred course':el.formation.value?el.formation.selectedOptions[0].textContent:'Not specified',
      'Appointment':jour+' at '+heure.value,'Comments or questions':el.message.value.trim()};
    const sujet='Appointment request: '+jour+' at '+heure.value+' – '+champs['Full name'];
    const sections=[['Your contact details',['Full name','Phone / WhatsApp','E-mail']],
                    ['Your appointment',['Appointment','Preferred course','Comments or questions']]];
    btn.disabled=true; btn.textContent='Sending…';
    envoyerEmail(form,sujet,champs,sections).then(rep=>{
      btn.disabled=false; btn.textContent=btnTexte;
      if(!rep.ok){afficherEchec(err,form,sujet,texteDemande(champs));return;}
      afficherRecap(document.getElementById('rdv-recap'),champs,sections,rep.numero);
      form.hidden=true; ok.hidden=false; ok.scrollIntoView({block:'start'});
    });
  });
  document.getElementById('rdv-again').onclick=()=>{ok.hidden=true;form.reset();majHeure();form.hidden=false;form.scrollIntoView({block:'start'});};
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
  const numero=k=>{const n=(el[k].value||'').trim(), ind=el[k+'_ind'].value;return n?(ind&&ind!=='Other'&&!n.startsWith('+')?ind+' '+n:n):'';};
  form.addEventListener('submit',e=>{
    e.preventDefault(); err.hidden=true;
    const paysOk=listesDrapeaux.pays.valide();
    if(!form.checkValidity()){form.reportValidity();return;}
    if(!paysOk){listesDrapeaux.pays.btn.focus();listesDrapeaux.pays.btn.scrollIntoView({block:'center'});return;}
    const val=x=>(x&&x.value||'').trim(), choix=x=>x.value?x.selectedOptions[0].textContent:'';
    const pays=/^Autre/.test(el.pays.value)&&val(el.pays_autre)?val(el.pays_autre):el.pays.value;
    const jour=new Date(el.naissance.value+'T12:00:00').toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric'});
    const champs={'Last name':val(el.nom).toUpperCase(),'First name(s)':val(el.prenoms),
      'Date of birth':jour+' ('+age(el.naissance.value)+' years old)','Place of birth':val(el.lieu_naissance),
      'Country':pays,'Sex':form.querySelector('input[name="sexe"]:checked').value,'Nationality':val(el.nationalite),
      'ID document':[choix(el.piece),val(el.piece_numero)].filter(Boolean).join(' no. '),
      'Address':val(el.adresse),'City / District':val(el.ville),'E-mail':val(el.email),
      'Main phone':numero('tel'),'Secondary phone':numero('tel2'),
      'Level of education':choix(el.niveau),'Latest diploma':val(el.diplome),
      'Course':choix(el.formation),'Current situation':choix(el.situation),'Experience':choix(el.experience)};
    if(!tuteur.hidden) Object.assign(champs,{'Parent or guardian':val(el.tuteur_nom),'Relationship':choix(el.tuteur_lien),'Guardian’s phone':val(el.tuteur_tel)});
    Object.assign(champs,{'Emergency contact':val(el.urgence),'How did you hear about us':choix(el.connu),'Career plan':val(el.motivation)});
    const sujet='Application: '+champs['Course']+' – '+champs['First name(s)']+' '+champs['Last name'];
    const parties=[...form.querySelectorAll('fieldset > legend')].map(l=>{const c=l.cloneNode(true);c.querySelectorAll('small').forEach(x=>x.remove());return c.textContent.replace(/^\s*\d+\.\s*/,'').trim();});
    const sections=[[parties[0],['Last name','First name(s)','Date of birth','Place of birth','Country','Sex','Nationality','ID document']],
      [parties[1],['Address','City / District','E-mail','Main phone','Secondary phone']],[parties[2],['Level of education','Latest diploma']],
      [parties[3],['Course','Current situation','Experience']],[parties[4],['Parent or guardian','Relationship','Guardian’s phone']],
      [parties[5],['Emergency contact','How did you hear about us','Career plan']]].filter(s=>s[0]);
    btn.disabled=true; btn.textContent='Sending…';
    envoyerEmail(form,sujet,champs,sections).then(rep=>{
      btn.disabled=false; btn.textContent='Send my application';
      if(!rep.ok){afficherEchec(err,form,sujet,texteDemande(champs));return;}
      afficherRecap(document.getElementById('ins-recap'),champs,sections,rep.numero);
      form.hidden=true; const box=document.getElementById('ins-ok'); box.hidden=false; box.scrollIntoView({block:'start'});
    });
  });
})();

// Documents des fiches candidat : envoyés un par un à /api/fichier (voir api/fichier.js), avant la fiche elle-même
const MAX_DOCUMENT=4*1024*1024, MAX_DOCUMENTS=6;
const formatAccepte=f=>/^(application\/pdf|application\/msword|application\/vnd\.openxmlformats-officedocument\.wordprocessingml\.document|image\/(jpeg|png|webp|heic|heif))$/.test(f.type)
  ||/\.(pdf|docx?|jpe?g|png|webp|heic|heif)$/i.test(f.name);
// Photo réduite à 1600 px en JPEG (une photo de téléphone passe de 4 Mo à environ 300 Ko) ; les autres fichiers ne changent pas
const reduireImage=f=>new Promise(ok=>{
  if(!/^image\/(jpeg|png|webp)$/.test(f.type)) return ok(f);
  const url=URL.createObjectURL(f), img=new Image();
  img.onload=()=>{
    URL.revokeObjectURL(url);
    const r=Math.min(1,1600/Math.max(img.naturalWidth,img.naturalHeight));
    if(r===1&&f.size<800*1024) return ok(f);
    const c=document.createElement('canvas');c.width=Math.round(img.naturalWidth*r);c.height=Math.round(img.naturalHeight*r);
    const ctx=c.getContext('2d');ctx.fillStyle='#fff';ctx.fillRect(0,0,c.width,c.height);ctx.drawImage(img,0,0,c.width,c.height);
    c.toBlob(b=>ok(b&&b.size<f.size?new File([b],f.name.replace(/\.[^.]+$/,'')+'.jpg',{type:'image/jpeg'}):f),'image/jpeg',0.85);
  };
  img.onerror=()=>{URL.revokeObjectURL(url);ok(f);};
  img.src=url;
});
const envoyerDocument=(f,champ,progres)=>new Promise(ok=>{
  const x=new XMLHttpRequest();
  x.open('POST','/api/fichier');
  x.setRequestHeader('Content-Type','application/octet-stream');
  x.setRequestHeader('X-Nom-Fichier',encodeURIComponent(f.name));
  x.setRequestHeader('X-Champ',encodeURIComponent(champ));
  x.upload.onprogress=e=>{if(e.lengthComputable)progres(Math.round(e.loaded/e.total*100));};
  x.onload=()=>{let r={};try{r=JSON.parse(x.responseText);}catch(_){}ok(x.status===200&&r.ok?r:null);};
  x.onerror=x.ontimeout=()=>ok(null);
  x.timeout=120000;
  x.send(f);
});
// Résultat : [{champ, nom, taille, ok, id, cle}] ; un fichier refusé ou perdu est réessayé une fois
const envoyerDocuments=async(liste,progres)=>{
  const res=[];
  for(const [k,{f,champ}] of liste.entries()){
    let r=null;
    for(let essai=0;essai<2&&!r;essai++) r=await envoyerDocument(f,champ,pc=>progres(k+1,liste.length,pc));
    res.push(r?{champ,nom:r.nom,taille:r.taille,ok:true,id:r.id,cle:r.cle}:{champ,nom:f.name,taille:f.size,ok:false});
  }
  return res;
};

// Fiches de l'espace recrutement (employeurs et candidats) : envoi par e-mail, récapitulatif
(function(){
  document.querySelectorAll('form.fiche').forEach(form=>{
    const merci=form.parentElement.querySelector('[data-merci]'), echec=form.querySelector('[data-echec]'), btn=form.querySelector('[data-envoyer]');
    const btnTexte=btn.textContent;
    // Montants en FCFA : espaces des milliers pendant la saisie
    form.querySelectorAll('[data-fcfa]').forEach(i=>i.addEventListener('input',()=>{const d=i.value.replace(/\D/g,'').slice(0,10);i.value=d?Number(d).toLocaleString('en-GB').replace(/ | /g,' '):'';}));
    // Documents : photos réduites dans le navigateur (envoi plus rapide), format et taille contrôlés dès le choix
    const fichiers=[...form.querySelectorAll('input[type="file"]')];
    const prets=new Map(); // champ → {liste, erreur, attente}
    const majZone=(i,texte,erreur)=>{const zone=form.querySelector(`[data-fichiers="${i.id}"]`);if(zone){zone.textContent=texte;zone.classList.toggle('tw-text-red-700',!!erreur);}};
    fichiers.forEach(i=>i.addEventListener('change',()=>{
      const choisis=[...i.files];
      const attente=Promise.all(choisis.map(reduireImage)).then(liste=>{
        let erreur='';
        if(liste.length>MAX_DOCUMENTS) erreur='Choose 6 files at most.';
        const mauvais=liste.find(f=>!formatAccepte(f)), lourd=liste.find(f=>f.size>MAX_DOCUMENT);
        if(mauvais) erreur='Format not accepted (PDF, Word or image): '+mauvais.name;
        else if(lourd) erreur='File too large (4 MB maximum): '+lourd.name;
        prets.set(i,{liste,erreur});
        majZone(i,erreur||liste.map(f=>f.name+' ('+tailleLisible(f.size)+')').join(', '),erreur);
      });
      prets.set(i,{liste:[],erreur:'',attente});
    }));
    // Groupes de choix obligatoires
    const groupes=[...form.querySelectorAll('[data-groupe]')];
    const groupeOk=g=>!g.dataset.requis||!!g.querySelector('input:checked');
    groupes.forEach(g=>g.addEventListener('change',()=>{if(groupeOk(g))g.querySelector('[data-erreur]').classList.add('tw-hidden');}));
    // Champs conditionnels : data-si="nom=valeur" s'affiche quand ce choix est coché
    const conditions=[...form.querySelectorAll('[data-si]')];
    const majConditions=()=>conditions.forEach(c=>{const [n,v]=c.dataset.si.split('=');
      c.classList.toggle('tw-hidden',![...form.querySelectorAll(`[name="${n}"]`)].some(i=>i.checked&&i.value===v));});
    if(conditions.length){form.addEventListener('change',majConditions);majConditions();}
    const valeurs=()=>{
      const champs={}, vus=new Set(), parSection=new Map();
      const ranger=(x,cle)=>{const s=x.closest('[data-section]');if(!s)return;const t=s.dataset.section;if(!parSection.has(t))parSection.set(t,[]);parSection.get(t).push(cle);};
      [...form.elements].forEach(el=>{
        if(!el.name||el.name==='botcheck'||vus.has(el.name)||(el.type==='hidden'&&!el.dataset.label)||(el.type==='checkbox'&&!el.closest('[data-groupe]'))||el.closest('[data-si].tw-hidden')) return;
        const g=el.closest('[data-groupe]');
        if(g){vus.add(el.name);const v=[...g.querySelectorAll('input:checked')].map(x=>x.value).join(', ');if(v){champs[g.dataset.label]=v;ranger(g,g.dataset.label);}return;}
        if(el.type==='file') return; // documents envoyés à part (voir envoyerDocuments)
        let v=el.tagName==='SELECT'?(el.value?el.selectedOptions[0].textContent:''):el.value.trim();
        if('paysRequis' in el.dataset&&/^Autre/.test(v)){const a=form.elements[el.name+'_autre'];if(a&&a.value.trim())v=a.value.trim();}
        if('paysRequis' in el.dataset) vus.add(el.name+'_autre');
        if(el.dataset.indicatif&&v){const ind=form.elements[el.dataset.indicatif].value;if(ind&&ind!=='Other'&&!v.startsWith('+'))v=ind+' '+v;}
        if('fcfa' in el.dataset&&v){const per=form.elements[el.name+'_periode'];v+=' FCFA'+(per&&per.value?' '+per.value:'');vus.add(el.name+'_periode');}
        if(v){champs[el.dataset.label||el.name]=v;ranger(el,el.dataset.label||el.name);}
      });
      return [champs,[...parSection]];
    };
    form.addEventListener('submit',async e=>{
      e.preventDefault(); echec.classList.add('tw-hidden');
      await Promise.all([...prets.values()].map(x=>x.attente)); // photos en cours de réduction
      const mauvais=groupes.filter(g=>!groupeOk(g));
      mauvais.forEach(g=>g.querySelector('[data-erreur]').classList.remove('tw-hidden'));
      fichiers.filter(i=>i.required&&!i.files.length).forEach(i=>majZone(i,'File required',true));
      const paysKo=[...form.querySelectorAll('[data-pays-requis]')].filter(i=>!listesDrapeaux[i.name].valide());
      if(!form.checkValidity()){form.reportValidity();return;}
      if(paysKo.length){const l=listesDrapeaux[paysKo[0].name];l.btn.scrollIntoView({block:'center'});l.btn.focus();return;}
      if(mauvais.length){mauvais[0].scrollIntoView({block:'center'});return;}
      const fichierKo=fichiers.find(i=>prets.has(i)&&prets.get(i).erreur);
      if(fichierKo){const z=form.querySelector(`[data-fichiers="${fichierKo.id}"]`);(z||fichierKo).scrollIntoView({block:'center'});return;}
      const [champs,sections]=valeurs();
      const nom=champs['Establishment or company']||[champs['First names'],champs['Last name']].filter(Boolean).join(' ');
      const objet=champs['I am looking for']||champs['Job sought']||'';
      const sujet=form.dataset.sujet+' : '+objet+' – '+nom;
      btn.disabled=true; btn.textContent='Sending…';
      // 1. les documents, un par un (4 Mo au plus chacun) ; 2. la fiche, avec les références des documents reçus
      const aEnvoyer=fichiers.flatMap(i=>(prets.has(i)?prets.get(i).liste:[...i.files]).map(f=>({f,champ:i.dataset.label})));
      const docs=await envoyerDocuments(aEnvoyer,(k,n,pc)=>{btn.textContent='Sending your documents… '+k+'/'+n+(pc<100?' ('+pc+' %)':'');});
      btn.textContent='Sending…';
      const rep=await envoyerEmail(form,sujet,champs,sections,docs.filter(x=>x.ok).map(x=>({id:x.id,cle:x.cle})));
      btn.disabled=false; btn.textContent=btnTexte;
      if(!rep.ok){afficherEchec(echec,form,sujet,texteDemande(champs));echec.classList.remove('tw-hidden');return;}
      // Documents non reçus (connexion coupée, base indisponible…) : envoi de secours sur WhatsApp
      if(rep.documents!==undefined&&rep.documents<docs.filter(x=>x.ok).length) docs.forEach(x=>{x.ok=false;});
      const manquants=docs.filter(x=>!x.ok);
      afficherRecap(merci.querySelector('[data-recap]'),champs,sections,rep.numero,docs);
      const wa=merci.querySelector('[data-wa-fichiers]'), alerte=merci.querySelector('[data-docs-manquants]');
      if(wa&&(manquants.length||(fichiers.length&&!docs.length))){
        wa.href='https://wa.me/'+form.dataset.wa+'?text='+encodeURIComponent('Hello EchoResta, here are the supporting documents for my application ('+nom+', '+objet+'): CV, photo and diplomas.');
        wa.classList.remove('tw-hidden'); wa.classList.add('tw-inline-flex');
        const intro=merci.querySelector('h2 + p');
        if(intro&&manquants.length) intro.textContent='Thank you! We have received your form. Our team will review your application and get back to you quickly.';
        if(alerte&&manquants.length){alerte.textContent='Some documents could not be sent: '+manquants.map(x=>x.nom).join(', ')+'. Send them on WhatsApp with the button below.';alerte.classList.remove('tw-hidden');}
      }
      form.classList.add('tw-hidden'); merci.classList.remove('tw-hidden'); merci.scrollIntoView({block:'start'});
    });
  });
})();
