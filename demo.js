
// 将base64图片绘制到canvas中的函数
function drawBase64ImageToCanvas(canvasId, base64Image) {
  // 获取canvas上下文
  const ctx = uni.createCanvasContext(canvasId);
  
  // 直接使用base64图片数据
  const imageUrl = 'data:image/png;base64,' + base64Image;
  
  // 使用uni.getImageInfo获取图片信息
  uni.getImageInfo({
    src: imageUrl,
    success: function(res) {
      // 清空canvas
      ctx.clearRect(0, 0, res.width, res.height);
      
      // 绘制图片到canvas
      ctx.drawImage(res.path, 0, 0, res.width, res.height);
      
      // 执行绘制
      ctx.draw();
    },
    fail: function(err) {
      console.error('Failed to load image:', err);
    }
  });
}

// 使用示例
// const canvasId = 'myCanvas';
// const base64Image = 'your_base64_image_string_here';
// drawBase64ImageToCanvas(canvasId, base64Image);
