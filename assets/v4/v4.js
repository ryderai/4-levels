/* 4Levels — v4 design direction behaviour. Every block checks its elements exist. No libraries. */
document.documentElement.classList.add('js');
(function(){
  'use strict';
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. PHONE MENU — full screen, focus trapped, Escape closes, focus returns */
  var btn = document.getElementById('menuBtn');
  var menu = document.getElementById('menu');
  if(btn && menu){
    var closeBtn = document.getElementById('menuClose');
    var focusables = function(){ return menu.querySelectorAll('a[href],button:not([disabled])'); };
    var open = function(){
      menu.hidden = false; btn.setAttribute('aria-expanded','true');
      document.body.classList.add('menu-open');
      (closeBtn || focusables()[0]).focus();
    };
    var close = function(back){
      menu.hidden = true; btn.setAttribute('aria-expanded','false');
      document.body.classList.remove('menu-open');
      if(back !== false) btn.focus();
    };
    btn.addEventListener('click', open);
    if(closeBtn) closeBtn.addEventListener('click', function(){ close(); });
    menu.addEventListener('keydown', function(e){
      if(e.key === 'Escape'){ e.preventDefault(); close(); return; }
      if(e.key !== 'Tab') return;
      var f = focusables(), first = f[0], last = f[f.length-1];
      if(e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
      else if(!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
    });
    menu.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', function(){ close(false); }); });
    window.addEventListener('resize', function(){ if(window.innerWidth > 860 && !menu.hidden) close(false); });
  }

  /* 2. HEADER — clear over the hero, solid once you scroll */
  var hd = document.getElementById('hd');
  if(hd){ var solid = function(){ hd.classList.toggle('solid', window.scrollY > 40); }; solid(); window.addEventListener('scroll', solid, {passive:true}); }

  /* 2b. PHONE CTA BAR — waits until the hero buttons scroll away, hides at the form */
  var pc = document.getElementById('phoneCta'), heroBtns = document.querySelector('.hero .btn-row'), contact = document.getElementById('contact');
  if(pc && heroBtns && 'IntersectionObserver' in window){
    var heroIn = true, formIn = false;
    var sync = function(){ pc.classList.toggle('away', heroIn || formIn); };
    new IntersectionObserver(function(es){ es.forEach(function(e){ heroIn = e.isIntersecting || e.boundingClientRect.top > 0; sync(); }); }).observe(heroBtns);
    if(contact) new IntersectionObserver(function(es){ es.forEach(function(e){ formIn = e.isIntersecting; sync(); }); }, {threshold:.05}).observe(contact);
  }else if(pc){ pc.classList.remove('away'); }

  /* 3. REVEAL ON SCROLL (content is visible without JS; html.js gates the effect) */
  var rv = document.querySelectorAll('.reveal');
  if(rv.length){
    if(reduced || !('IntersectionObserver' in window)){ rv.forEach(function(el){ el.classList.add('in'); }); }
    else{
      var io = new IntersectionObserver(function(es){
        es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
      }, {threshold:.12, rootMargin:'0px 0px -6% 0px'});
      rv.forEach(function(el){ io.observe(el); });
    }
  }

  /* 5. LEAD FORM — posts to /api/lead. Says "sent" only when the email provider confirmed it.
     Until the form is wired (no client inbox yet) it says so and keeps every answer. */
  var form = document.getElementById('leadForm');
  if(form){
    var started = document.getElementById('startedAt'); started.value = Date.now();
    var msg = document.getElementById('formMsg'), send = document.getElementById('sendBtn');
    form.addEventListener('submit', function(ev){
      ev.preventDefault();
      var name = document.getElementById('f-name'), email = document.getElementById('f-email');
      [name, email].forEach(function(f){ f.removeAttribute('aria-invalid'); });
      var bad = [];
      if(!name.value.trim()) bad.push(name);
      if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value.trim())) bad.push(email);
      if(bad.length){
        bad.forEach(function(f){ f.setAttribute('aria-invalid','true'); });
        msg.className = 'form-msg err';
        msg.textContent = 'Add your name and a working email address first.';
        bad[0].focus(); return;
      }
      var data = {}; new FormData(form).forEach(function(v, k){ data[k] = v; });
      send.disabled = true; send.textContent = 'Sending…';
      fetch('/api/lead', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)})
        .then(function(r){ return r.json().catch(function(){ return {ok:false}; }); })
        .then(function(res){
          if(res.ok){
            msg.className = 'form-msg ok'; msg.textContent = 'Sent. The 4Levels team has your message.';
            form.reset(); started.value = Date.now();
          }else if(res.error === 'NOTCONFIGURED'){
            msg.className = 'form-msg err'; msg.textContent = 'This form is not connected yet, so nothing was sent. Your answers are still here.';
          }else{
            msg.className = 'form-msg err'; msg.textContent = (res.message || 'We could not send that just now.') + ' Your answers are still here.';
          }
        })
        .catch(function(){ msg.className = 'form-msg err'; msg.textContent = 'We could not send that just now. Your answers are still here.'; })
        .finally(function(){ send.disabled = false; send.textContent = 'Send message'; });
    });
  }
})();
