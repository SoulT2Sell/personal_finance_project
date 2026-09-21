/**
 * Shared site-wide helpers.
 * Any page can open a confirm modal by adding data-confirm-modal="#modal-id"
 * to a trigger element, and data-confirm-target inside the modal for the
 * <form> that should actually submit on confirm.
 */
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-confirm-modal]").forEach((trigger) => {
    trigger.addEventListener("click", (e) => {
      e.preventDefault();
      const modal = document.querySelector(trigger.dataset.confirmModal);
      if (!modal) return;

      // Let the trigger tell the modal which form to submit / row it refers to.
      if (trigger.dataset.confirmAction) {
        const form = modal.querySelector("[data-confirm-target]");
        if (form) form.setAttribute("action", trigger.dataset.confirmAction);
      }
      if (trigger.dataset.confirmName) {
        const label = modal.querySelector("[data-confirm-name]");
        if (label) label.textContent = trigger.dataset.confirmName;
      }

      modal.classList.add("is-open");
    });
  });

  document.querySelectorAll("[data-close-modal]").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.closest(".modal-overlay")?.classList.remove("is-open");
    });
  });

  document.querySelectorAll(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) overlay.classList.remove("is-open");
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.querySelectorAll(".modal-overlay.is-open").forEach((m) => m.classList.remove("is-open"));
    }
  });
});
