(function(){
  // slow-moving trend lines
  var series = [
    { base:.24, color:'rgba(15,110,102,.2)', amp:46 },
    { base:.52, color:'rgba(180,72,28,.16)', amp:60 },
    { base:.8, color:'rgba(15,110,102,.14)', amp:38 }
  ];
  function valueAt(line, index, x, time){
    return Math.sin(x * .007 + time * .00035 + index * 2) * line.amp + Math.sin(x * .021 + time * .0006 + index) * line.amp * .3;
  }
  window.startAmbient(function(ctx, width, height, time){
    ctx.clearRect(0, 0, width, height);
    series.forEach(function(line, index){
      ctx.strokeStyle = line.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (var x = 0; x <= width; x += 14){
        var y = height * line.base + valueAt(line, index, x, time);
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.fillStyle = line.color;
      for (var px = 70; px < width; px += 140){
        ctx.beginPath();
        ctx.arc(px, height * line.base + valueAt(line, index, px, time), 3.5, 0, 6.28);
        ctx.fill();
      }
    });
  }, 30);
})();
