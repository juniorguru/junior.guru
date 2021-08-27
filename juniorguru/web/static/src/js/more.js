function onLoad() {
  if(!document.getElementsByClassName('body__container').length) {
    return;  // turn off on new pages
  }

  const sections = Array.from(document.getElementsByClassName('more'));
  sections.forEach(function (section) {
    const div = document.createElement('div');
    div.classList.add('more__container');
    Array.from(section.childNodes).forEach(function (child) {
      div.appendChild(child);
    });
    section.appendChild(div);

    const p = document.createElement('p');
    p.classList.add('button-compartment');
    p.classList.add('more__cover');
    p.addEventListener('click', function (event) {
      div.removeChild(p);
      div.classList.remove('more--collapsed');
    });

    const button = document.createElement('span');
    button.textContent = 'Zobrazit víc';
    button.classList.add('button');
    button.classList.add('button--link');
    button.classList.add('more__button');
    p.appendChild(button);

    div.classList.add('more--collapsed');
    div.appendChild(p);
  });
  handleHash();
}

function handleHash() {
  if (
    !window.location.hash ||
    !document.querySelector('.more--collapsed ' + window.location.hash)
  ) {
    return;
  }

  const id = ('' + window.location.hash).replace(/^#/, '');
  const element = document.getElementById(id);

  let el = element;
  while (el) {
    // console.log(el);
    if (el.className.match('more--collapsed')) {
      const button = el.getElementsByClassName('more__button')[0];
      // console.log(button);
      button.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
      break;
    }
    el = el.parentElement;
  }

  element.scrollIntoView();
}

document.addEventListener('DOMContentLoaded', onLoad);
window.addEventListener('hashchange', handleHash);
