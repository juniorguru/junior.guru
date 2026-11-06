function setupJobsTags() {
  const container = document.querySelector(".jobs-filters");
  if (container) {
    container
      .querySelectorAll(".jobs-tag:not(.disabled)")
      .forEach(function (tag) {
        tag.addEventListener("click", function () {
          const isActive = tag.classList.toggle("active");
          tag.setAttribute("aria-pressed", isActive);
          filterJobs({ pushHistory: true });
        });
        showElement(tag);
      });
    updateJobsTagsUI();
    window.addEventListener("popstate", updateJobsTagsUI);
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

function filterJobs({ pushHistory = false } = {}) {
  // Fixed tags are disabled and always active, e.g. the region on /jobs/brno/,
  // so they take part in filtering, but they never get to the URL
  const activeTagsByType = groupTagsByType(
    document.querySelectorAll(".jobs-filters .jobs-tag.active"),
  );
  const selectedTagsByType = groupTagsByType(
    document.querySelectorAll(".jobs-filters .jobs-tag.active:not(.disabled)"),
  );

  const filterTypes = new Set(
    Array.from(
      document.querySelectorAll(".jobs-filters .jobs-tag"),
      (tag) => tag.dataset.jobsTagType,
    ),
  );
  const url = new URL(window.location.href);
  filterTypes.forEach((type) => url.searchParams.delete(type));
  Object.entries(selectedTagsByType).forEach(([type, tags]) => {
    url.searchParams.set(type, tags.join("|"));
  });
  if (pushHistory) {
    window.history.pushState({}, "", url);
  }

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
      const isRelevant = Object.entries(activeTagsByType).every(
        ([type, tags]) =>
          jobTags.some(
            (tag) =>
              tag.dataset.jobsTagType === type &&
              tags.includes(tag.dataset.jobsTag),
          ),
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
    {},
  );
  const container = document.querySelector(".jobs-filters");
  container.querySelectorAll(".jobs-tag:not(.disabled)").forEach((tag) => {
    const activeSlugs = activeSlugsByType[tag.dataset.jobsTagType] || [];
    const isActive = activeSlugs.includes(tag.dataset.jobsTag);
    tag.classList.toggle("active", isActive);
    tag.setAttribute("aria-pressed", isActive);
  });
  filterJobs();
}

function showElement(element) {
  element.removeAttribute("hidden");
}

function hideElement(element) {
  element.setAttribute("hidden", "");
}

function groupTagsByType(tags) {
  const tagsByType = Array.from(tags).reduce((mapping, tag) => {
    mapping[tag.dataset.jobsTagType] ||= [];
    mapping[tag.dataset.jobsTagType].push(tag.dataset.jobsTag);
    return mapping;
  }, {});
  Object.values(tagsByType).forEach((slugs) => slugs.sort());
  return tagsByType;
}

document.addEventListener("DOMContentLoaded", setupJobsTags);
document.addEventListener("DOMContentLoaded", setupJobs);
