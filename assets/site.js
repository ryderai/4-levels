/* 4Levels Sports Advisory — site behaviour. Every block checks its elements exist,
   so one file serves every page. No libraries. */
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

  /* 2. THE MARK — the 4 rises, the bars punch out. Replays on click or when scrolled back to. */
  var mark = document.getElementById('heroMark');
  if(mark){
    var heroEl = document.querySelector('.hero');
    var play = function(){ mark.classList.remove('play'); void mark.getBoundingClientRect(); mark.classList.add('play'); if(heroEl) heroEl.classList.add('play'); };
    if(!reduced){
      setTimeout(play, 150);
      mark.addEventListener('click', play);
      var away = false;
      new IntersectionObserver(function(es){
        es.forEach(function(e){ if(e.isIntersecting && away){ away = false; play(); } else if(!e.isIntersecting){ away = true; } });
      }, {threshold:.4}).observe(mark);
    }
  }

  /* 2b. PHONE CTA BAR — on the homepage it waits until the hero buttons scroll away */
  var pc = document.getElementById('phoneCta'), heroBtns = document.querySelector('.hero .btn-row');
  if(pc && heroBtns && 'IntersectionObserver' in window){
    new IntersectionObserver(function(es){ es.forEach(function(e){ pc.classList.toggle('away', e.isIntersecting || e.boundingClientRect.top > 0); }); }).observe(heroBtns);
  }else if(pc){ pc.classList.remove('away'); }

  if(mark && reduced){ var h0 = document.querySelector('.hero'); if(h0) h0.classList.add('play'); }

  /* 2c. MARQUEE pause */
  var mq = document.querySelector('.marquee'), mqBtn = document.querySelector('.marquee-pause');
  if(mq && mqBtn){
    mqBtn.addEventListener('click', function(){
      var p = mq.classList.toggle('paused');
      mqBtn.setAttribute('aria-pressed', p ? 'true' : 'false');
      mqBtn.textContent = p ? 'Play' : 'Pause';
      mqBtn.setAttribute('aria-label', p ? 'Play the moving words' : 'Pause the moving words');
    });
  }

  /* 2d. STAIRCASE (services) — the sticky number and bars follow the level you are reading */
  var stairNum = document.getElementById('stairNum');
  var svcs = document.querySelectorAll('.svc[data-level]');
  if(svcs.length){
    var bars = document.querySelectorAll('.stair-bars i'), jumps = document.querySelectorAll('.jump a');
    var setLevel = function(n, el){
      if(stairNum){ stairNum.textContent = '0' + n; document.getElementById('stairName').textContent = el.querySelector('h2').textContent; }
      bars.forEach(function(b, k){ b.classList.toggle('on', k < n); });
      jumps.forEach(function(a, k){ a.classList.toggle('on', k === n - 1); if(k === n - 1) a.setAttribute('aria-current','true'); else a.removeAttribute('aria-current'); });
    };
    setLevel(1, svcs[0]);
    if('IntersectionObserver' in window){
      var so = new IntersectionObserver(function(es){
        es.forEach(function(e){ if(e.isIntersecting) setLevel(+e.target.dataset.level, e.target); });
      }, {rootMargin:'-45% 0px -50% 0px'});
      svcs.forEach(function(s){ so.observe(s); });
    }
  }

  /* 2e. CONTACT PREFILL — the "where are you?" cards send ?i=hs|col|pro|fam */
  var pre = {hs:['An athlete','High school'], col:['An athlete','College'], pro:['An athlete',''], fam:['A parent or family member','']};
  var key = new URLSearchParams(location.search).get('i');
  if(key && pre[key] && document.getElementById('leadForm')){
    var tick = function(name, val){ if(!val) return; document.querySelectorAll('input[name="' + name + '"]').forEach(function(r){ if(r.value === val) r.checked = true; }); };
    tick('I am', pre[key][0]); tick('Level of play', pre[key][1]);
  }

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

  /* 4. THE WIRE — one line draws itself through the four levels as you scroll.
     The path is built from the cards' real positions, so it always connects. */
  var track = document.getElementById('levelsTrack');
  if(track){
    var wire = document.getElementById('wire'), drawEl = document.getElementById('wireDraw'),
        trackEl = document.getElementById('wireTrack'), dot = document.getElementById('wireDot'),
        halo = document.getElementById('wireHalo');
    var cards = [].slice.call(track.querySelectorAll('.lvl')), nodes = [].slice.call(track.querySelectorAll('.node'));
    var totalLen = 0, nodeLens = [];
    var build = function(){
      var tr = track.getBoundingClientRect();
      wire.setAttribute('viewBox','0 0 ' + tr.width + ' ' + tr.height);
      var pts = nodes.map(function(n){ var r = n.getBoundingClientRect(); return {x:r.left - tr.left + r.width/2, y:r.top - tr.top + r.height/2}; });
      var all = [{x:pts[0].x < tr.width/2 ? pts[0].x : tr.width/2, y:-60}].concat(pts, [{x:pts[pts.length-1].x, y:tr.height + 60}]);
      if(window.innerWidth > 860){ all[0].x = tr.width/2; all[all.length-1].x = tr.width/2; }
      var d = 'M ' + all[0].x + ' ' + all[0].y, segEnds = [];
      var probe = document.createElementNS('http://www.w3.org/2000/svg','path');
      for(var i = 1; i < all.length; i++){
        var a = all[i-1], b = all[i], bend = Math.max(50, (b.y - a.y) * .55);
        d += ' C ' + a.x + ' ' + (a.y + bend) + ', ' + b.x + ' ' + (b.y - bend) + ', ' + b.x + ' ' + b.y;
        probe.setAttribute('d', d); segEnds.push(probe.getTotalLength());
      }
      drawEl.setAttribute('d', d); trackEl.setAttribute('d', d);
      totalLen = drawEl.getTotalLength(); nodeLens = segEnds.slice(0, pts.length);
      drawEl.style.strokeDasharray = totalLen;
      drawEl.style.strokeDashoffset = reduced ? 0 : totalLen;
      if(reduced){ cards.forEach(function(c){ c.classList.add('lit'); }); dot.style.display = 'none'; halo.style.display = 'none'; }
    };
    var progress = function(){
      var r = track.getBoundingClientRect(), vh = window.innerHeight;
      return Math.min(1, Math.max(0, (vh * .8 - r.top) / (r.height + vh * .3)));
    };
    var cur = 0, ticking = false;
    var frame = function(){
      var t = progress(); cur += (t - cur) * .12; if(Math.abs(t - cur) < .001) cur = t;
      var len = totalLen * cur; drawEl.style.strokeDashoffset = totalLen - len;
      var p = drawEl.getPointAtLength(len);
      dot.setAttribute('cx', p.x); dot.setAttribute('cy', p.y); halo.setAttribute('cx', p.x); halo.setAttribute('cy', p.y);
      cards.forEach(function(c, i){ c.classList.toggle('lit', len >= nodeLens[i] - 2); });
      if(cur !== t) requestAnimationFrame(frame); else ticking = false;
    };
    var kick = function(){ if(!ticking){ ticking = true; requestAnimationFrame(frame); } };
    if(!reduced){ window.addEventListener('scroll', kick, {passive:true}); window.addEventListener('load', kick); }
    var rt; window.addEventListener('resize', function(){ clearTimeout(rt); rt = setTimeout(function(){ build(); kick(); }, 150); });
    build(); kick();
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ build(); kick(); });
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
