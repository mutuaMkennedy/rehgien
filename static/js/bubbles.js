class bubble {
  constructor(canvasWidth, canvasHeight) {
    this.maxHeight = canvasHeight;
    this.maxWidth = canvasWidth;
    this.randomise();
  }

  generateDecimalBetween(min, max) {
    return (Math.random() * (min - max) + max).toFixed(2);
  }

  update() {
    this.posX = this.posX - this.movementX;
    this.posY = this.posY - this.movementY;

    if (this.posY < 0 || this.posX < 0 || this.posX > this.maxWidth) {
      this.randomise();
      this.posY = this.maxHeight;
    }
  }

  randomise() {
    this.colour = Math.random() * 190;
    this.size = this.generateDecimalBetween(1, 4);
    this.movementX = this.generateDecimalBetween(-0.4, 0.4);
    this.movementY = this.generateDecimalBetween(0.7, 1);
    this.posX = this.generateDecimalBetween(0, this.maxWidth);
    this.posY = this.generateDecimalBetween(0, this.maxHeight);
  }
}

class background {
  constructor() {
    this.canvas = document.getElementById("ursebdfd");
    if (this.canvas != null) {
      this.ctx = this.canvas.getContext("2d");
      this.canvas.height = window.innerHeight;
      this.canvas.width = window.innerWidth;
      this.bubblesList = [];
    }
    this.generateBubbles();
    this.animate();
  }

  animate() {
    let self = this;
    if (self.ctx != undefined) {
      self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height);
      self.bubblesList.forEach(function(bubble) {
        bubble.update();
        self.ctx.beginPath();
        self.ctx.arc(bubble.posX, bubble.posY, bubble.size, 0, 2 * Math.PI);
        self.ctx.fillStyle = "hsl(179, 82%, 55%, 0.7)";
        self.ctx.fill();
        self.ctx.strokeStyle = "hsl(179, 82%, 55%, 0.7)";
        self.ctx.stroke();
      });

      requestAnimationFrame(this.animate.bind(this));
    }
  }

  addBubble(bubble) {
    return this.bubblesList.push(bubble);
  }

  generateBubbles() {
    let self = this;
    for (let i = 0; i < self.bubbleDensity(); i++) {
      self.addBubble(new bubble(self.canvas.width, self.canvas.height));
    }
  }


    bubbleDensity() {
        if (this.canvas != null) {
          return Math.sqrt((this.canvas.height, this.canvas.width) * 100);
        }
    }
}

  function initialize () {
  new background();
  document.querySelector(".preloader").style.display = "none";
  };
  window.requestAnimFrame = (function() {
  return (
    window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.oRequestAnimationFrame ||
    window.msRequestAnimationFrame ||
    function(callback) {
      window.setTimeout(callback, 1000 / 60);
    }
  );
  });
initialize()
