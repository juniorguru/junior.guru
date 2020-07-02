function onLoad() {
  const sections = Array.from(document.getElementsByClassName('more'));
  sections.forEach(function (section) {
    const div = document.createElement('div');
    div.classList.add('more-wrapper');
    Array.from(section.childNodes).forEach(function (child) {
      div.appendChild(child);
    });
    section.appendChild(div);

    const p = document.createElement('p');
    p.classList.add('call-to-action');
    p.classList.add('more-action-area');

    const button = document.createElement('span');
    button.textContent = 'Zobrazit víc';
    button.classList.add('legacy-button');
    button.addEventListener('click', function (event) {
      div.removeChild(p);
      div.classList.remove('more-collapsed');
    });
    p.appendChild(button);

    div.classList.add('more-collapsed');
    div.appendChild(p);
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
    // console.log(el);
    if (el.className.match('more-collapsed')) {
      const button = el.querySelector('.more-action-area .button');
      // console.log(button);
      button.dispatchEvent(new MouseEvent('click'));
      break;
    }
    el = el.parentElement;
  }

  element.scrollIntoView();
}

document.addEventListener('DOMContentLoaded', onLoad);
window.addEventListener('hashchange', handleHash);
