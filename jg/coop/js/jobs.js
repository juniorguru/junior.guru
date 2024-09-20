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
  const activeTagsByType = activeTags.reduce((mapping, tag) => {
    mapping[tag.dataset.jobsTagType] ||= [];
    mapping[tag.dataset.jobsTagType].push(tag.dataset.jobsTag);
    return mapping;
  }, {});
  Object.values(activeTagsByType).forEach((tags) => tags.sort());

  const url = new URL(window.location.href);
  Array.from(url.searchParams.keys()).forEach((type) =>
    url.searchParams.delete(type),
  );
  Object.entries(activeTagsByType).forEach(([type, tags]) => {
    url.searchParams.set(type, tags.join("|"));
  });
  window.history.pushState({}, "", url);

  const jobs = Array.from(document.querySelectorAll(".jobs-item.tagged"));
  if (Object.keys(activeTagsByType).length === 0) {
    jobs.forEach((job) => {
      job.removeAttribute("hidden");
    });
    return;
  }

  const count = jobs
    .map((job) => {
      const jobTags = Array.from(job.querySelectorAll(".jobs-tag"));
      const jobSlugs = jobTags.map((tag) => tag.dataset.jobsTag);
      const isRelevant = Object.entries(activeTagsByType).every(
        ([type, tags]) => tags.some((tag) => jobSlugs.includes(tag)),
      );
      if (isRelevant) {
        job.removeAttribute("hidden");
        return 1;
      }
      job.setAttribute("hidden", "");
      return 0;
    })
    .reduce((a, b) => a + b, 0);

  const empty = document.querySelector(".jobs-empty");
  if (count === 0) {
    empty.removeAttribute("hidden");
  } else {
    empty.setAttribute("hidden", "");
  }
}

function updateJobsUI() {
  const url = new URL(window.location.href);
  const activeSlugsByType = Array.from(url.searchParams.keys()).reduce(
    (mapping, type) => {
      mapping[type] = url.searchParams.get(type).split("|");
      return mapping;
    },
    {},
  );
  const container = document.querySelector(".jobs-tags");
  container.querySelectorAll(".jobs-tag").forEach((tag) => {
    const activeSlugs = activeSlugsByType[tag.dataset.jobsTagType] || [];
    const isActive = activeSlugs.includes(tag.dataset.jobsTag);
    if (isActive) {
      tag.classList.add("active");
    } else {
      tag.classList.remove("active");
    }
  });
  filterJobs();
}

document.addEventListener("DOMContentLoaded", setupJobsTags);
window.addEventListener("popstate", updateJobsUI);
