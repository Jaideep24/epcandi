(function () {
    "use strict";

    function submitForm(form) {
        if (typeof form.requestSubmit === "function") {
            form.requestSubmit();
            return;
        }
        form.submit();
    }

    function wireAutoFilter(form) {
        var debounceTimer = null;
        var textInputs = form.querySelectorAll('input[type="text"], input[type="search"]');
        var immediateInputs = form.querySelectorAll('select, input[type="checkbox"], input[type="radio"]');

        textInputs.forEach(function (input) {
            input.addEventListener("input", function () {
                window.clearTimeout(debounceTimer);
                debounceTimer = window.setTimeout(function () {
                    submitForm(form);
                }, 250);
            });
        });

        immediateInputs.forEach(function (input) {
            input.addEventListener("change", function () {
                submitForm(form);
            });
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".list-filter-form").forEach(wireAutoFilter);
    });
})();
