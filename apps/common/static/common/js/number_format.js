/**
 * Number input helper: adds Persian thousands separators to number inputs
 * while the user types, strips them before form submission, and converts
 * Persian digits to Western digits on submit (so the server receives a
 * plain number).
 */
(function () {
  "use strict";

  var PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
  var SEPARATOR = ",";
  var THOUSANDS_SEP = ",";

  function toWesternDigits(str) {
    if (!str) return "";
    var result = "";
    for (var i = 0; i < str.length; i++) {
      var ch = str[i];
      var idx = PERSIAN_DIGITS.indexOf(ch);
      if (idx >= 0) {
        result += idx;
      } else {
        result += ch;
      }
    }
    return result;
  }

  function formatThousands(value) {
    var parts = value.split(".");
    var intPart = parts[0];
    var decPart = parts.length > 1 ? "." + parts[1] : "";

    var regex = /(-?\d)(?=(\d{3})+(?!\d))/g;
    intPart = intPart.replace(regex, "$1" + THOUSANDS_SEP);

    return intPart + decPart;
  }

  function initField(field) {
    if (field.dataset.thousandsInitialized) return;
    field.dataset.thousandsInitialized = "true";

    field.addEventListener("focus", function () {
      var raw = field.value.replace(new RegExp("\\" + THOUSANDS_SEP, "g"), "");
      field.value = raw;
    });

    field.addEventListener("blur", function () {
      var western = toWesternDigits(field.value).replace(new RegExp("\\" + THOUSANDS_SEP, "g"), "");
      if (western !== "" && !isNaN(Number(western))) {
        field.value = formatThousands(western);
      }
    });

    field.addEventListener("input", function () {
      var western = toWesternDigits(field.value).replace(new RegExp("\\" + THOUSANDS_SEP, "g"), "");
      field.value = formatThousands(western);
    });
  }

  function stripOnSubmit(form) {
    form.addEventListener("submit", function () {
      var fields = form.querySelectorAll("input.number-input");
      fields.forEach(function (field) {
        if (field.dataset.thousandsInitialized) {
          var western = toWesternDigits(field.value).replace(new RegExp("\\" + THOUSANDS_SEP, "g"), "");
          field.value = western;
        }
      });
    });
  }

  function initAll(form) {
    var fields = form.querySelectorAll("input.number-input");
    fields.forEach(initField);
    stripOnSubmit(form);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var forms = document.querySelectorAll("form");
    forms.forEach(initAll);
  });
})();
