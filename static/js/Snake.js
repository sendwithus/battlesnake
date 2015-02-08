var Snake = function(config_data) {
  console.log('New snake', config_data);
  this.id = config_data.snake_id;
  this.name = config_data.name;
  // this.headImg = config_data.head_img_url;
  this.headImg = 'http://screenshots.en.sftcdn.net/en/scrn/3332000/3332933/snake-iii-3d-01-100x100.png';
  // this.facing = null,
  // this.status = snakewithus.STATUS.ALIVE;
  // this.message = '';
  // this.stats = { };
  this.color = makeNonGray(generateColor());
  this.img = null;
};

Snake.prototype.getColor = function() {
  return 'rgba('+this.color.join(',')+','+snakewithus.BODY_OPACITY+')';
};

Snake.prototype.getHeadColor = function() {
  return 'rgba('+this.color.join(',')+','+snakewithus.HEAD_OPACITY+')';
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
