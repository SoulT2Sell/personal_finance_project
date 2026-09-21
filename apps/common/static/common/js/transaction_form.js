document.addEventListener("DOMContentLoaded", () => {
  const select = document.querySelector("[data-account-select]");
  const hint = document.getElementById("account-currency-hint");
  if (!select || !hint) return;

  const updateHint = () => {
    const opt = select.options[select.selectedIndex];
    const currency = opt ? opt.dataset.currency : "";
    hint.textContent = currency ? `ارز این حساب: ${currency}` : "";
  };

  select.addEventListener("change", updateHint);
  updateHint(); // shows the currency immediately on the edit form, where an account is already selected
});
