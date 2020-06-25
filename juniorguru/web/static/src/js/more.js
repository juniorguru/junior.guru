function onLoad() {
  const sections = Array.from(document.getElementsByClassName('more'));
  sections.forEach(function (section) {
    const p = document.createElement('p');
    p.classList.add('call-to-action');
    p.classList.add('more-action-area');

    const button = document.createElement('span');
    button.textContent = 'Zobrazit víc';
    button.classList.add('legacy-button');
    button.addEventListener('click', function (event) {
      section.removeChild(p);
      section.classList.remove('more-collapsed');
    });
    p.appendChild(button);

    section.classList.add('more-collapsed');
    section.appendChild(p);
  });
  handleHash();
}

function handleHash() {
  if (
    !window.location.hash ||
    !document.querySelector('.more-collapsed ' + window.location.hash)
  ) {
    return;
  }

  const id = ('' + window.location.hash).replace(/^#/, '');
  const element = document.getElementById(id);

  let el = element;
  while (el) {
    console.log(el);
    if (el.className.match('more-collapsed')) {
      const button = el.querySelector('.more-action-area .button');
      console.log(button);
      button.dispatchEvent(new MouseEvent('click'));
      break;
    }
    el = el.parentElement;
  }

  element.scrollIntoView();
}

document.addEventListener('DOMContentLoaded', onLoad);
window.addEventListener('hashchange', handleHash);
