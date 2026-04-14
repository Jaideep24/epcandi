(function () {
    function initSidebarAnalyticsLink() {
        if (document.body.classList.contains("login")) {
            return;
        }

        var navSidebar = document.getElementById("nav-sidebar");
        if (!navSidebar) {
            return;
        }

        var modules = navSidebar.querySelectorAll(".module");
        var contentModule = null;
        modules.forEach(function (module) {
            if (contentModule) {
                return;
            }
            var section = module.querySelector("caption .section, h2");
            var name = (section && section.textContent ? section.textContent : "").toLowerCase();
            if (name.indexOf("epc") !== -1 && name.indexOf("content") !== -1) {
                contentModule = module;
            }
        });

        if (!contentModule && modules.length) {
            contentModule = modules[modules.length - 1];
        }
        if (!contentModule) {
            return;
        }

        var hasAnalyticsLink = Array.prototype.some.call(contentModule.querySelectorAll("a"), function (link) {
            var href = (link.getAttribute("href") || "").toLowerCase();
            return href.indexOf("/admin/analytics/") !== -1 || (link.textContent || "").trim().toLowerCase() === "analytics";
        });
        if (hasAnalyticsLink) {
            return;
        }

        var tableBody = contentModule.querySelector("table tbody") || contentModule.querySelector("tbody");
        if (!tableBody) {
            var listTarget = contentModule.querySelector("ul, ol");
            if (listTarget) {
                var listItem = document.createElement("li");
                listItem.className = "model-analytics";
                var listLink = document.createElement("a");
                listLink.href = "/admin/analytics/";
                listLink.textContent = "Analytics";
                listItem.appendChild(listLink);
                listTarget.appendChild(listItem);
            }
            return;
        }

        var row = document.createElement("tr");
        row.className = "model-analytics";

        var cell = document.createElement("th");
        cell.scope = "row";

        var link = document.createElement("a");
        link.href = "/admin/analytics/";
        link.textContent = "Analytics";

        cell.appendChild(link);
        row.appendChild(cell);
        tableBody.appendChild(row);
    }

    function initLoginPasswordToggle() {
        if (!document.body.classList.contains("login")) {
            return;
        }

        var toggle = document.querySelector(".epci-password-toggle");
        var passwordInput = document.getElementById("id_password");
        if (!toggle || !passwordInput) {
            return;
        }

        var icon = toggle.querySelector("i");

        function setState(isVisible) {
            passwordInput.type = isVisible ? "text" : "password";
            toggle.setAttribute("aria-pressed", isVisible ? "true" : "false");
            toggle.setAttribute("aria-label", isVisible ? "Hide password" : "Show password");
            if (icon) {
                icon.className = isVisible ? "fa fa-eye-slash" : "fa fa-eye";
            }
        }

        setState(false);
        toggle.addEventListener("click", function () {
            var isVisible = passwordInput.type === "text";
            setState(!isVisible);
        });
    }

    function createButton(label, title, action, commandName) {
        var button = document.createElement("button");
        button.type = "button";
        button.className = "epci-richtext-btn";
        button.innerHTML = label;
        button.title = title;
        if (commandName) {
            button.dataset.command = commandName;
            button.setAttribute("aria-pressed", "false");
        }
        button.addEventListener("click", function () {
            action();
        });
        return button;
    }

    function createSeparator() {
        var sep = document.createElement("span");
        sep.className = "epci-richtext-separator";
        sep.setAttribute("aria-hidden", "true");
        return sep;
    }

    function setButtonActive(button, isActive) {
        button.classList.toggle("is-active", !!isActive);
        if (button.dataset.command) {
            button.setAttribute("aria-pressed", isActive ? "true" : "false");
        }
    }

    function applyEditor(textarea) {
        if (textarea.dataset.epciEnhanced === "1") {
            return;
        }

        var wrapper = document.createElement("div");
        wrapper.className = "epci-richtext-wrap";

        var toolbar = document.createElement("div");
        toolbar.className = "epci-richtext-toolbar";

        var editor = document.createElement("div");
        editor.className = "epci-richtext-editor";
        editor.contentEditable = "true";
        editor.innerHTML = textarea.value || "";

        var stateButtons = {};

        function addStateButton(label, title, commandName) {
            var btn = createButton(label, title, function () {
                document.execCommand(commandName, false, null);
                editor.focus();
                syncButtonStates();
            }, commandName);
            stateButtons[commandName] = btn;
            toolbar.appendChild(btn);
        }

        function syncButtonStates() {
            var selection = window.getSelection();
            var inEditor = selection && selection.rangeCount > 0 && editor.contains(selection.anchorNode);
            if (!inEditor && document.activeElement !== editor) {
                return;
            }

            Object.keys(stateButtons).forEach(function (commandName) {
                var active = false;
                try {
                    active = document.queryCommandState(commandName);
                } catch (e) {
                    active = false;
                }
                setButtonActive(stateButtons[commandName], active);
            });
        }

        addStateButton("B", "Bold", "bold");
        addStateButton("I", "Italic", "italic");
        addStateButton("U", "Underline", "underline");
        toolbar.appendChild(createSeparator());
        addStateButton("&bull;", "Bulleted list", "insertUnorderedList");
        addStateButton("1.", "Numbered list", "insertOrderedList");
        toolbar.appendChild(createSeparator());
        toolbar.appendChild(createButton('<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M10.59 13.41a1 1 0 0 1 0-1.41l3-3a3 3 0 0 1 4.24 4.24l-2.12 2.12a3 3 0 0 1-4.24 0 1 1 0 1 1 1.41-1.41 1 1 0 0 0 1.42 0l2.12-2.12a1 1 0 1 0-1.42-1.41l-3 3a1 1 0 0 1-1.41 0zM13.41 10.59a1 1 0 0 1 0 1.41l-3 3a3 3 0 1 1-4.24-4.24l2.12-2.12a3 3 0 0 1 4.24 0 1 1 0 1 1-1.41 1.41 1 1 0 0 0-1.42 0L7.58 12.17a1 1 0 1 0 1.42 1.41l3-3a1 1 0 0 1 1.41 0z"/></svg>', "Insert link", function () {
            var url = window.prompt("Enter URL");
            if (url) {
                document.execCommand("createLink", false, url);
            }
            editor.focus();
            syncButtonStates();
        }));
        toolbar.appendChild(createButton('<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M4 5h16a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm1 2v9.59l4.3-4.3a1 1 0 0 1 1.4 0l2.3 2.3 2.3-2.3a1 1 0 0 1 1.4 0L19 14.59V7H5zm4 3a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/></svg>', "Insert image", function () {
            var url = window.prompt("Enter image URL");
            if (url) {
                document.execCommand("insertImage", false, url);
            }
            editor.focus();
            syncButtonStates();
        }));
        toolbar.appendChild(createButton('<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M19 20H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h3l1.2-2h5.6L16 6h3a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2zM5 8v10h14V8h-4.2l-1.2-2H10.4L9.2 8H5zm7 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/></svg>', "Upload image", function () {
            var picker = document.createElement("input");
            picker.type = "file";
            picker.accept = "image/*";
            picker.addEventListener("change", function () {
                var file = picker.files && picker.files[0];
                if (!file) {
                    return;
                }
                var reader = new FileReader();
                reader.onload = function (evt) {
                    var dataUrl = evt && evt.target ? evt.target.result : "";
                    if (typeof dataUrl === "string" && dataUrl) {
                        document.execCommand("insertImage", false, dataUrl);
                        textarea.value = editor.innerHTML;
                    }
                    editor.focus();
                    syncButtonStates();
                };
                reader.readAsDataURL(file);
            });
            picker.click();
        }));

        editor.addEventListener("input", function () {
            textarea.value = editor.innerHTML;
            syncButtonStates();
        });
        editor.addEventListener("keyup", syncButtonStates);
        editor.addEventListener("mouseup", syncButtonStates);
        editor.addEventListener("focus", syncButtonStates);
        document.addEventListener("selectionchange", syncButtonStates);

        var form = textarea.closest("form");
        if (form) {
            form.addEventListener("submit", function () {
                textarea.value = editor.innerHTML;
            });
        }

        textarea.style.display = "none";

        wrapper.appendChild(toolbar);
        wrapper.appendChild(editor);
        textarea.parentNode.insertBefore(wrapper, textarea);

        textarea.dataset.epciEnhanced = "1";
    }

    function initEditors() {
        var textareas = document.querySelectorAll("textarea");
        textareas.forEach(function (textarea) {
            if (textarea.name === "csrfmiddlewaretoken") {
                return;
            }
            applyEditor(textarea);
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        initSidebarAnalyticsLink();
        initLoginPasswordToggle();
        initEditors();
    });
})();
