(function(){
  var current = document.getElementById('current-file');
  document.addEventListener('section-change', function(event){
    current.textContent = event.detail.getAttribute('data-file');
    if (event.detail.parentNode.scrollWidth > event.detail.parentNode.clientWidth){
      event.detail.parentNode.scrollLeft = event.detail.offsetLeft - 16;
    }
  });

  // falling code tokens
  var tokens = ['const', 'async', 'await', 'def', 'return', 'import', '=>', '{ }', '</>', '( )', '[ ]', 'git push', 'npm run', 'API', 'class', 'fetch()'];
  var drops = [];
  for (var i = 0; i < 26; i++){
    drops.push({ x:i / 26, y:Math.random(), speed:.0007 + Math.random() * .0012, token:tokens[i % tokens.length] });
  }
  window.startAmbient(function(ctx, width, height){
    ctx.clearRect(0, 0, width, height);
    ctx.font = '13px "JetBrains Mono", monospace';
    drops.forEach(function(drop, index){
      drop.y += drop.speed;
      if (drop.y > 1.05){ drop.y = -.05; drop.token = tokens[Math.floor(Math.random() * tokens.length)]; }
      ctx.fillStyle = index % 3 ? 'rgba(108,182,255,.17)' : 'rgba(201,165,255,.17)';
      ctx.fillText(drop.token, drop.x * width, drop.y * height);
    });
  }, 30);
})();
