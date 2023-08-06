import * as m from "../core/component.js";


class EditButtonGroup extends m.Component {
    constructor() {
        super();
    }

    open(ev) {
        ev.stopPropagation();
        ev.preventDefault();

        // this.querySelector('.dropdown-menu').classList.add('show');
        let parent_rect = this.querySelector('.parent').getBoundingClientRect();
        for (let el of this.getElementsByClassName('dropdown-menu')) {
            if (el.classList.contains('show') || ev.target.classList.contains('dropdown-item')) {
                el.classList.remove('show');
            } else {
                el.classList.add('show');
                let rect = el.getBoundingClientRect();
                if (rect.right > window.innerWidth) {
                    let left = rect.width - this.querySelector('button').getBoundingClientRect().width;
                    el.style['left'] = `-${left}px`;
                }

                if (rect.bottom > window.innerHeight) {
                    el.style['top'] = `-${rect.height}px`;
                }
            }
        }
    }

    render() {
        return m.html`
          <div class="parent" style="position: relative; display: inline-block;">
            <div class="btn-group">
              <button type="button" class="btn btn-outline-secondary dropdown-toggle" @click="${this.open}">${this.getAttribute('label')}</button>
            </div>
            <div class="dropdown-menu">${this.$children}</div>
          </div>
        `
    }
}
customElements.define("kr-button-group", EditButtonGroup)
