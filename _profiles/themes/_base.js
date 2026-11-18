(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var heading = document.querySelector('h1');
  if (heading){
    heading.classList.add('glitch');
    heading.setAttribute('data-text', heading.textContent);
  }

  // scroll-in directions, matching the Cyber Security portfolio
  function mark(selector, direction){
    document.querySelectorAll(selector).forEach(function(el){
      el.classList.add('reveal');
      el.classList.remove('right', 'up');
      if (direction) el.classList.add(direction);
    });
  }
  mark('.hero-grid>div:first-child,.masthead>div:first-child,.hero>div:first-child');
  mark('.avatar,.terminal', 'right');
  mark('h2,.job,.code,.editor .shell,.model,.panel,.contact-list', 'up');
  document.querySelectorAll('.metric,.proj,.cert,.edu,.skill,.suite,.step').forEach(function(el){
    var index = Array.prototype.indexOf.call(el.parentNode.children, el);
    el.classList.add('reveal');
    el.classList.remove('right', 'up');
    if (index % 2) el.classList.add('right');
  });

  var reveals = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)){
    reveals.forEach(function(el){ el.classList.add('is-visible'); });
  } else {
    var seen = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if (entry.isIntersecting){ entry.target.classList.add('is-visible'); seen.unobserve(entry.target); }
      });
    }, { threshold:.08, rootMargin:'0px 0px -5% 0px' });
    reveals.forEach(function(el){ seen.observe(el); });
  }

  // hover-tilt
  if (!reduce && window.matchMedia('(hover:hover)').matches){
    document.querySelectorAll('.avatar,.metric,.job,.proj,.cert,.edu,.skill,.suite,.step,.panel,.code,.editor .shell,.model,.terminal').forEach(function(el){
      el.classList.add('tilt');
      el.addEventListener('pointermove', function(e){
        if (!el.classList.contains('is-visible')) return;
        el.style.transition = 'none';
        var r = el.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        var strength = r.width > 640 ? 3 : 9;
        el.style.transform = 'perspective(900px) rotateX(' + (-py * strength).toFixed(2) + 'deg) rotateY(' + (px * strength).toFixed(2) + 'deg)';
      });
      el.addEventListener('pointerleave', function(){
        el.style.transition = 'transform .3s ease';
        el.style.transform = '';
      });
    });
  }

  // typewriter
  var intro = document.querySelector('.intro');
  if (intro && !reduce){
    var text = intro.textContent, at = 0;
    var cursor = document.createElement('span');
    cursor.className = 'type-cursor';
    cursor.setAttribute('aria-hidden', 'true');
    intro.style.minHeight = intro.offsetHeight + 'px';
    intro.setAttribute('aria-label', text);
    (function type(){
      intro.textContent = text.slice(0, at);
      intro.appendChild(cursor);
      if (at++ < text.length) setTimeout(type, 24);
    })();
  }

  // ambient background canvas, used by each theme
  window.startAmbient = function(draw, fps){
    var canvas = document.getElementById('ambient');
    if (!canvas) return;
    var ctx = canvas.getContext('2d'), width, height, last = 0;
    function size(){
      var ratio = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * ratio;
      canvas.height = height * ratio;
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
      if (reduce) draw(ctx, width, height, 0);
    }
    size();
    window.addEventListener('resize', size);
    if (reduce) return;
    (function loop(time){
      requestAnimationFrame(loop);
      if (document.hidden || time - last < 1000 / fps) return;
      last = time;
      draw(ctx, width, height, time);
    })(0);
  };

  var links = document.querySelectorAll('[data-spy]');
  if (links.length && 'IntersectionObserver' in window){
    var spy = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if (!entry.isIntersecting) return;
        links.forEach(function(link){
          var on = link.getAttribute('href') === '#' + entry.target.id;
          link.classList.toggle('active', on);
          if (on){
            link.setAttribute('aria-current', 'true');
            document.dispatchEvent(new CustomEvent('section-change', { detail:link }));
          } else {
            link.removeAttribute('aria-current');
          }
        });
      });
    }, { rootMargin:'-40% 0px -55% 0px' });
    links.forEach(function(link){
      var target = document.querySelector(link.getAttribute('href'));
      if (target) spy.observe(target);
    });
  }
})();
