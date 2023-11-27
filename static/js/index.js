const animatedDiv = document.querySelector(".page-title");
animatedDiv.textContent = "";

class AnimateText {
  constructor() {
    this.animatedText = "Nfcs Voting Poll";
    this.intervalF;
    this.intervalB;
    this.count = 0;
    this.writeText();
  }

  writeText() {
    this.intervalF = setInterval(() => {
      animatedDiv.textContent += this.animatedText[this.count];
      this.count++;

      if (this.count >= this.animatedText.length) {
        clearInterval(this.intervalF);
        this.deleteText();
      }
    }, 200);
  }

  deleteText() {
    this.intervalB = setInterval(() => {
      this.count--;
      animatedDiv.textContent = this.animatedText.slice(0, this.count);

      if (this.count === 1) {
        clearInterval(this.intervalB);
        this.writeText();
      }
    }, 100);
  }
}

new AnimateText();
