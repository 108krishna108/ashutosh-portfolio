(function(){
  var bar = document.getElementById('progress');
  var ticking = false;
  function update(){
    var max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(window.scrollY / max, 1) : 0) + ')';
    ticking = false;
  }
  window.addEventListener('scroll', function(){
    if (!ticking){ ticking = true; requestAnimationFrame(update); }
  }, { passive:true });
  update();

  document.addEventListener('section-change', function(event){
    var nav = event.detail.parentNode;
    if (nav.scrollWidth > nav.clientWidth) nav.scrollLeft = event.detail.offsetLeft - nav.offsetLeft - 16;
  });

  // rising pass marks
  var marks = [];
  for (var i = 0; i < 30; i++){
    marks.push({ x:Math.random(), y:Math.random(), speed:.0006 + Math.random() * .001, size:12 + Math.random() * 12, amber:i % 4 === 0 });
  }
  window.startAmbient(function(ctx, width, height){
    ctx.clearRect(0, 0, width, height);
    marks.forEach(function(mark){
      mark.y -= mark.speed;
      if (mark.y < -.05){ mark.y = 1.05; mark.x = Math.random(); }
      ctx.font = mark.size + 'px "Fira Code", monospace';
      ctx.fillStyle = mark.amber ? 'rgba(245,165,36,.2)' : 'rgba(94,234,212,.2)';
      ctx.fillText('✓', mark.x * width, mark.y * height);
    });
  }, 30);
})();
