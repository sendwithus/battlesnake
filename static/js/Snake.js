var Snake = function(config_data) {
  this.id = config_data.id;
  this.name = config_data.name;
  this.headImg = 'http://screenshots.en.sftcdn.net/en/scrn/3332000/3332933/snake-iii-3d-01-100x100.png';
  this.color = config_data.color || 'red';
  this.img = null;
};

Snake.prototype.getColor = function() {
  return this.color;
};

Snake.prototype.getHeadColor = function() {
  return this.color;
};

Snake.prototype._loadImg = function() {
  if (!this.loadingImage && !this.img) {
    this.loadingImage = true;
    var that = this;
    var img = document.createElement('img');
    img.onload = function() {
      that.img = img;
    };
    img.src = this.headImg;
  }

  return this.img;
};

Snake.prototype.getHeadImage = function() {
  return this._loadImg() || false;
};
