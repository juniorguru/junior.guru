document.addEventListener('DOMContentLoaded', function () {
  // if the subnav scrolls horizontally, set it to the middle or to make
  // the active tab visible so it's clear on small screens that users can
  // scroll it and no tabs get hidden
  const subnav = Array.from(document.getElementsByClassName('header__subnav'))[0];
  const activeTab = Array.from(document.getElementsByClassName('header__subnav-tab-control--active'))[0];

  if (subnav && activeTab && subnav.scrollWidth > window.innerWidth) {
    subnav.scrollLeft = Math.max(
      (subnav.scrollWidth - window.innerWidth) / 2,
      activeTab.getBoundingClientRect().left - 10
    );
  }
});
