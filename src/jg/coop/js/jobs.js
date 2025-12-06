function setupJobsTags() {
  const container = document.querySelector(".jobs-tags");
  if (container) {
    container
      .querySelectorAll(".jobs-tag:not(.disabled)")
      .forEach(function (tag) {
        tag.addEventListener("click", function () {
          tag.classList.toggle("active");
          filterJobs();
        });
        showElement(tag);
      });
    updateJobsTagsUI();
    container.classList.remove("noscript");
  }
  document.querySelectorAll(".jobs-noscript").forEach(function (noscript) {
    noscript.remove();
  });
}

function setupJobs() {
  document.querySelectorAll(".jobs-item.openable").forEach(function (job) {
    job.classList.remove("open");

    const titleLink = job.querySelector(".jobs-title-link");
    const close = job.querySelector(".jobs-close");

    const inside = [close].concat(
      Array.from(
        job.querySelectorAll(".jobs-title-text, .jobs-actions, .jobs-company"),
      ),
    );
    const outside = [titleLink].concat(
      Array.from(job.querySelectorAll(".jobs-open")),
    );

    titleLink.addEventListener("click", function (event) {
      event.preventDefault();
      job.classList.add("open");
      inside.forEach(showElement);
      outside.forEach(hideElement);
    });

    close.addEventListener("click", function () {
      job.classList.remove("open");
      inside.forEach(hideElement);
      outside.forEach(showElement);
    });
  });

  const subscribe = document.querySelector(".jobs-subscribe");
  if (subscribe) {
    subscribe.addEventListener("click", function () {
      hideElement(subscribe);
    });
  }
}

function filterJobs() {
  const activeTags = Array.from(
    document.querySelectorAll(".jobs-tags .jobs-tag.active"),
  );
  const activeTagsByType = activeTags.reduce((mapping, tag) => {
    mapping[tag.dataset.jobsTagType] ||= [];
    mapping[tag.dataset.jobsTagType].push(tag.dataset.jobsTag);
    return mapping;
  }, {});
  const locationSlug = getLocationSlug(window.location);
  if (locationSlug && !activeTagsByType["location"].includes(locationSlug)) {
    activeTagsByType["location"].push(locationSlug);
  }
  Object.values(activeTagsByType).forEach((tags) => tags.sort());

  const url = new URL(window.location.href);
  Array.from(url.searchParams.keys()).forEach((type) =>
    url.searchParams.delete(type),
  );
  Object.entries(activeTagsByType).forEach(([type, tags]) => {
    if (tags.includes(locationSlug)) {
      tags = tags.filter((tag) => tag !== locationSlug);
    }
    if (tags.length === 0) {
      return;
    }
    url.searchParams.set(type, tags.join("|"));
  });
  window.history.pushState({}, "", url);

  const jobs = Array.from(document.querySelectorAll(".jobs-item.tagged"));
  const allJobTags = Array.from(
    document.querySelectorAll(".jobs-item.tagged .jobs-tag"),
  );

  if (Object.keys(activeTagsByType).length === 0) {
    jobs.forEach(showElement);
    allJobTags.forEach((tag) => tag.classList.remove("matching"));
    return;
  }

  allJobTags.forEach((tag) => {
    if (
      activeTagsByType[tag.dataset.jobsTagType]?.includes(tag.dataset.jobsTag)
    ) {
      tag.classList.add("matching");
    } else {
      tag.classList.remove("matching");
    }
  });

  const count = jobs
    .map((job) => {
      const jobTags = Array.from(job.querySelectorAll(".jobs-tag"));
      const jobSlugs = jobTags.map((tag) => tag.dataset.jobsTag);
      const isRelevant = Object.entries(activeTagsByType).every(
        ([type, tags]) => tags.some((tag) => jobSlugs.includes(tag)),
      );
      if (isRelevant) {
        showElement(job);
        return 1;
      }
      hideElement(job);
      return 0;
    })
    .reduce((a, b) => a + b, 0);

  const empty = document.querySelector(".jobs-empty");
  if (count === 0) {
    showElement(empty);
  } else {
    hideElement(empty);
  }
}

function updateJobsTagsUI() {
  const url = new URL(window.location.href);
  const activeSlugsByType = Array.from(url.searchParams.keys()).reduce(
    (mapping, type) => {
      mapping[type] = url.searchParams.get(type).split("|");
      return mapping;
    },
    { location: [] },
  );
  const locationSlug = getLocationSlug(window.location);
  if (locationSlug) {
    activeSlugsByType["location"].push(locationSlug);
  }
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

function showElement(element) {
  element.removeAttribute("hidden");
}

function hideElement(element) {
  element.setAttribute("hidden", "");
}

function getLocationSlug(location) {
  const match = location.pathname.match(/\/jobs\/([^/]+)\/?$/);
  return match ? match[1].replace("-", "") : null;
}

document.addEventListener("DOMContentLoaded", setupJobsTags);
document.addEventListener("DOMContentLoaded", setupJobs);
window.addEventListener("popstate", updateJobsTagsUI);
