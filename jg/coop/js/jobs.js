function setupJobsTags() {
  const container = document.querySelector(".jobs-tags");
  if (container) {
    container.querySelectorAll(".jobs-tag").forEach(function (tag) {
      tag.addEventListener("click", function () {
        tag.classList.toggle("active");
        filterJobs();
      });
    });
    updateJobsUI();
    container.removeAttribute("hidden");
  }
}

function filterJobs() {
  const activeTags = Array.from(document.querySelectorAll(".jobs-tag.active"));

  const activeSlugs = activeTags.map((tag) => tag.dataset.jobsTag);
  updateJobsURL(activeSlugs);

  const jobs = Array.from(document.querySelectorAll(".jobs-item"));
  if (activeSlugs.length === 0) {
    jobs.forEach((job) => {
      job.removeAttribute("hidden");
    });
    return;
  }
  jobs.forEach((job) => {
    const jobTags = Array.from(job.querySelectorAll(".jobs-tag"));
    const jobSlugs = jobTags.map((tag) => tag.dataset.jobsTag);
    if (activeSlugs.every((slug) => jobSlugs.includes(slug))) {
      job.removeAttribute("hidden");
    } else {
      job.setAttribute("hidden", "");
    }
  });
}

function updateJobsURL(tags) {
  const tagsCopy = Array.from(tags);
  tagsCopy.sort();
  const currentURL = new URL(window.location.href);
  const tagsParam = tagsCopy.join('|');
  if (tagsParam) {
    currentURL.searchParams.set('tags', tagsParam);
  } else {
    currentURL.searchParams.delete('tags');
  }
  window.history.pushState({}, '', currentURL);
}

function updateJobsUI() {
  const newURL = new URL(window.location.href);
  const tagsParam = newURL.searchParams.get('tags') || "";
  const tags = tagsParam.split('|');
  const container = document.querySelector('.jobs-tags');
  container.querySelectorAll('.jobs-tag').forEach(tag => {
    if (tags.includes(tag.dataset.jobsTag)) {
      tag.classList.add('active');
    } else {
      tag.classList.remove('active');
    }
  });
  filterJobs();
}

document.addEventListener("DOMContentLoaded", setupJobsTags);
window.addEventListener("popstate", updateJobsUI);
