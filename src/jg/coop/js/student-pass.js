const VERIFYING_DURATION_MS = 2000;

function setupStudentPass() {
  const form = document.querySelector("#student-pass-form");
  const input = form?.querySelector("#student-pass-input");
  if (!input) return;

  const verifying = document.querySelector("#student-pass-verifying");
  const ticket = document.querySelector("#student-pass-ticket");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    window.sa_event?.(getStudentPassEventName(form.dataset.slug), {
      course: input.value.trim(),
    });
    form.hidden = true;
    verifying.hidden = false;
    setTimeout(() => {
      verifying.hidden = true;
      ticket.hidden = false;
      ticket.focus();
    }, VERIFYING_DURATION_MS);
  });
}

/**
 * Returns name of the Simple Analytics event to fire when someone claims a pass
 *
 * Event names work better than metadata in Simple Analytics, so the slug
 * of the course provider is part of the name.
 */
export function getStudentPassEventName(slug) {
  return slug ? `student_pass_${slug}` : "student_pass";
}

document.addEventListener("DOMContentLoaded", setupStudentPass);
