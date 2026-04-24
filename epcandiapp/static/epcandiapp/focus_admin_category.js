(function () {
  function toggleNewCategoryField() {
    var categorySelect = document.getElementById("id_category");
    var newCategoryInput = document.getElementById("id_new_category");
    if (!categorySelect || !newCategoryInput) {
      return;
    }

    var newCategoryRow = newCategoryInput.closest(".form-row") || newCategoryInput.parentElement;
    if (!newCategoryRow) {
      return;
    }

    var shouldShow = categorySelect.value === "__new__";
    newCategoryRow.style.display = shouldShow ? "" : "none";

    if (!shouldShow) {
      newCategoryInput.value = "";
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var categorySelect = document.getElementById("id_category");
    if (!categorySelect) {
      return;
    }

    categorySelect.addEventListener("change", toggleNewCategoryField);
    toggleNewCategoryField();
  });
})();
