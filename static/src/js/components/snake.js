/**
 *  Snake class
 */

export default class Snake {

  constructor (config_data) {
    this.id = config_data.name || config_data.id;
    this.name = config_data.name || config_data.id;
    this.headImg = config_data.head_url;
    this.color = config_data.color || 'red';
    this.img = null;
    this._loadImg();
  }

  getColor () {
    return this.color;
  }

  getHeadColor () {
    return this.color;
  }

  _loadImg () {
    if (!this.loadingImage && !this.img) {
      this.loadingImage = true;
      var img = document.createElement('img');
      img.onload = () => {
        this.img = img;
      };
      img.src = this.headImg;
    }

    return this.img;
  }

  getHeadImage () {
    return this._loadImg() || false;
  }

}
