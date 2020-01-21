function onLoad() {
  const sections = Array.from(document.getElementsByClassName('more'));
  sections.forEach(function (section) {
    const p = document.createElement('p');
    p.classList.add('call-to-action');
    p.classList.add('more-action-area');

    const button = document.createElement('span');
    button.textContent = 'Zobrazit víc';
    button.classList.add('button');
    button.addEventListener('click', function (event) {
      section.removeChild(p);
      section.classList.remove('more-collapsed');
    });
    p.appendChild(button);

    section.classList.add('more-collapsed');
    section.appendChild(p);
  });
}

document.addEventListener('DOMContentLoaded', onLoad);
