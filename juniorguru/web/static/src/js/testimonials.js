document.addEventListener('DOMContentLoaded', function () {
  if(!document.getElementsByClassName('body__container').length) {
    return;  // turn off on new pages
  }

  const testimonials = document.querySelector('.testimonials');
  const itemList = Array.from(document.querySelectorAll('.testimonials__item'));
  if (!testimonials || !itemList.length) { return; }

  const labels = document.createElement('ul');
  labels.classList.add('testimonials__labels');
  const labelList = [];
  itemList.forEach(function (item, i) {
    const label = document.createElement('li');
    label.textContent = '' + (i + 1);
    label.classList.add('testimonials__label');
    labels.appendChild(label);
    labelList.push(label);
  });
  testimonials.insertBefore(labels, testimonials.firstChild);

  function display(i) {
    labelList.forEach(function (label) { label.classList.remove('testimonials__label--active'); });
    labelList[i].classList.add('testimonials__label--active');
    itemList.forEach(function (item) { item.classList.add('testimonials__item--inactive'); });
    itemList[i].classList.remove('testimonials__item--inactive');
  }

  labelList.forEach(function (label, i) {
    label.addEventListener('click', function () { display(i); });
  });
  display(0);
});
