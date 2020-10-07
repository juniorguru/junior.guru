import onScroll from './onScroll';

let content;
let header;
let logosBar;
let toc;

function activateStickyLogoBar() {
  if (content) {
    content.classList.add('content--target-offset-logos');
  }
  if (header) {
    header.classList.add('header--opaque');
    if (logosBar) {
      logosBar.classList.add('logos--bar-sticky');
      logosBar.style.top = (header.getBoundingClientRect().bottom - header.getBoundingClientRect().top) + 'px';
    }
  }
  if (toc) {
    toc.classList.add('toc--target-offset-logos');
  }
}

function activateLogoBarShadow() {
  if (header && logosBar) {
    if (header.getBoundingClientRect().bottom >= logosBar.getBoundingClientRect().top) {
      logosBar.classList.add('logos--bar-sticky-detached');
    } else {
      logosBar.classList.remove('logos--bar-sticky-detached');
    }
  }
}

document.addEventListener('DOMContentLoaded', function () {
  content = Array.from(document.getElementsByClassName('content'))[0];
  header = Array.from(document.getElementsByClassName('header'))[0];
  logosBar = Array.from(document.getElementsByClassName('logos--bar'))[0];
  toc = Array.from(document.getElementsByClassName('toc'))[0];
  activateStickyLogoBar();
});

window.addEventListener('resize', activateStickyLogoBar);

document.addEventListener('DOMContentLoaded', activateLogoBarShadow);

window.addEventListener('resize', activateLogoBarShadow);

onScroll(activateLogoBarShadow);
