import 'details-element-polyfill';

function getJobs() {
  return Array.from(document.getElementsByTagName('li'))
    .filter(function (item) {
      const classes = item.getAttribute('class') || '';
      return classes === 'job'
        ? true
        : classes.split(' ').indexOf('job') >= 0;
    });
}

function getDetails(job) {
  return Array.from(job.getElementsByTagName('details'))[0];
}

function getOtherDetails(job) {
  return getJobs()
    .filter(function (otherJob) { return otherJob !== job })
    .map(function (otherJob) { return getDetails(otherJob) });
}

function onDocumentLoad() {
  getJobs().forEach(function (job) {
    const id = job.getAttribute('id');
    const details = getDetails(job);
    details.addEventListener('toggle', function () {
      if (details.open) {
        window.location.hash = '#' + id;
        job.setAttribute('class', 'job job-open');
        getOtherDetails(job).forEach(function (otherDetails) {
          otherDetails.removeAttribute('open');
        });
      } else {
        job.setAttribute('class', 'job');
      }
    });
  });

  if (window.location.hash.match(/^#job\-/)) {
    const id = window.location.hash.replace(/^#/, '');
    getDetails(document.getElementById(id)).setAttribute('open', '');
  }
}

document.addEventListener('DOMContentLoaded', onDocumentLoad);
