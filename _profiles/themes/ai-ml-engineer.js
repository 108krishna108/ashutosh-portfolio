(function(){
  var canvas = document.getElementById('net');
  var ctx = canvas.getContext('2d');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nodes = [], width, height, ratio;

  function size(){
    ratio = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    var count = Math.round(Math.min(70, width * height / 22000));
    nodes = [];
    for (var i = 0; i < count; i++){
      nodes.push({ x:Math.random() * width, y:Math.random() * height, vx:(Math.random() - .5) * .28, vy:(Math.random() - .5) * .28, phase:Math.random() * 6.28 });
    }
  }

  function draw(time){
    ctx.clearRect(0, 0, width, height);
    var reach = 150;
    for (var i = 0; i < nodes.length; i++){
      var a = nodes[i];
      if (!reduce){
        a.x += a.vx; a.y += a.vy;
        if (a.x < 0 || a.x > width) a.vx *= -1;
        if (a.y < 0 || a.y > height) a.vy *= -1;
      }
      for (var j = i + 1; j < nodes.length; j++){
        var b = nodes[j], dx = a.x - b.x, dy = a.y - b.y, d = Math.sqrt(dx * dx + dy * dy);
        if (d > reach) continue;
        ctx.strokeStyle = 'rgba(167,139,250,' + (.2 * (1 - d / reach)) + ')';
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        if (!reduce && (i + j) % 9 === 0){
          var t = (time / 2600 + a.phase) % 1;
          ctx.fillStyle = 'rgba(103,232,249,.75)';
          ctx.beginPath(); ctx.arc(a.x - dx * t, a.y - dy * t, 1.6, 0, 6.28); ctx.fill();
        }
      }
      ctx.fillStyle = i % 4 === 0 ? 'rgba(244,114,182,.7)' : 'rgba(167,139,250,.75)';
      ctx.beginPath(); ctx.arc(a.x, a.y, 2.1, 0, 6.28); ctx.fill();
    }
    if (!reduce) requestAnimationFrame(draw);
  }

  size();
  window.addEventListener('resize', function(){ size(); if (reduce) draw(0); });
  draw(0);
})();
