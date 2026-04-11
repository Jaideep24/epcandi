(function () {
    var USER_KEY = "epci_user_id";
    var SESSION_KEY = "epci_session_id";
    var SESSION_TS_KEY = "epci_session_ts";
    var SCROLL_MARK_KEY = "epci_scroll_marks";
    var SESSION_TIMEOUT_MS = 30 * 60 * 1000;
    var TRACK_ENDPOINT = "/track/";
    var DOWNLOAD_EXTENSIONS = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".rar", ".csv", ".ppt", ".pptx"];

    function uid(prefix) {
        return prefix + "_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2, 10);
    }

    function getOrCreateUserId() {
        var existing = localStorage.getItem(USER_KEY);
        if (existing) {
            return existing;
        }
        var id = uid("u");
        localStorage.setItem(USER_KEY, id);
        return id;
    }

    function getOrCreateSessionId(now) {
        var sessionId = sessionStorage.getItem(SESSION_KEY);
        var lastTs = Number(sessionStorage.getItem(SESSION_TS_KEY) || "0");
        if (!sessionId || !lastTs || (now - lastTs) > SESSION_TIMEOUT_MS) {
            sessionId = uid("s");
            sessionStorage.setItem(SESSION_KEY, sessionId);
            sessionStorage.setItem(SCROLL_MARK_KEY, "");
        }
        sessionStorage.setItem(SESSION_TS_KEY, String(now));
        return sessionId;
    }

    function parseUtm() {
        var params = new URLSearchParams(window.location.search);
        return {
            utm_source: params.get("utm_source") || "",
            utm_medium: params.get("utm_medium") || "",
            utm_campaign: params.get("utm_campaign") || ""
        };
    }

    function detectDeviceType() {
        var width = window.innerWidth || document.documentElement.clientWidth || 1024;
        if (width <= 768) {
            return "mobile";
        }
        if (width <= 1024) {
            return "tablet";
        }
        return "desktop";
    }

    function detectBrowser(ua) {
        if (ua.indexOf("Edg/") > -1) return "Edge";
        if (ua.indexOf("Chrome/") > -1) return "Chrome";
        if (ua.indexOf("Firefox/") > -1) return "Firefox";
        if (ua.indexOf("Safari/") > -1) return "Safari";
        return "Other";
    }

    function detectOS(ua) {
        if (ua.indexOf("Windows") > -1) return "Windows";
        if (ua.indexOf("Mac OS") > -1) return "macOS";
        if (ua.indexOf("Linux") > -1) return "Linux";
        if (ua.indexOf("Android") > -1) return "Android";
        if (ua.indexOf("iPhone") > -1 || ua.indexOf("iPad") > -1) return "iOS";
        return "Other";
    }

    function buildPayload(eventType, extras) {
        var now = Date.now();
        var ua = navigator.userAgent || "";
        var base = {
            user_id: getOrCreateUserId(),
            session_id: getOrCreateSessionId(now),
            event_type: eventType,
            page_url: window.location.pathname + window.location.search,
            referrer: document.referrer || "",
            language: navigator.language || "",
            device_type: detectDeviceType(),
            browser: detectBrowser(ua),
            operating_system: detectOS(ua)
        };
        var utm = parseUtm();
        base.utm_source = utm.utm_source;
        base.utm_medium = utm.utm_medium;
        base.utm_campaign = utm.utm_campaign;
        if (extras) {
            Object.keys(extras).forEach(function (key) {
                base[key] = extras[key];
            });
        }
        return base;
    }

    function sendEvent(eventType, extras, useBeacon) {
        if (navigator.doNotTrack === "1" || window.doNotTrack === "1") {
            return;
        }
        var payload = buildPayload(eventType, extras || {});
        sessionStorage.setItem(SESSION_TS_KEY, String(Date.now()));
        var body = JSON.stringify(payload);

        if (useBeacon && navigator.sendBeacon) {
            var blob = new Blob([body], { type: "application/json" });
            navigator.sendBeacon(TRACK_ENDPOINT, blob);
            return;
        }

        fetch(TRACK_ENDPOINT, {
            method: "POST",
            credentials: "same-origin",
            headers: { "Content-Type": "application/json" },
            body: body,
            keepalive: true
        }).catch(function () {
            return null;
        });
    }

    function trackScrollDepth() {
        var marks = [25, 50, 75, 100];
        var marked = (sessionStorage.getItem(SCROLL_MARK_KEY) || "").split(",").filter(Boolean);

        function onScroll() {
            var h = document.documentElement;
            var scrollable = Math.max(h.scrollHeight - h.clientHeight, 1);
            var depth = Math.round((window.scrollY / scrollable) * 100);

            marks.forEach(function (mark) {
                if (depth >= mark && marked.indexOf(String(mark)) === -1) {
                    marked.push(String(mark));
                    sessionStorage.setItem(SCROLL_MARK_KEY, marked.join(","));
                    sendEvent("scroll_depth", { scroll_depth: mark });
                }
            });
        }

        window.addEventListener("scroll", onScroll, { passive: true });
    }

    function trackClicks() {
        document.addEventListener("click", function (event) {
            var target = event.target;
            if (!target) return;
            var anchor = target.closest("a");
            if (anchor && anchor.href) {
                var href = (anchor.getAttribute("href") || "").toLowerCase();
                var isDownload = DOWNLOAD_EXTENSIONS.some(function (ext) { return href.indexOf(ext) > -1; });
                if (isDownload || anchor.hasAttribute("download")) {
                    sendEvent("download_click", {
                        event_name: "download_click",
                        metadata: {
                            href: anchor.getAttribute("href") || "",
                            text: (anchor.textContent || "").trim().slice(0, 120)
                        }
                    });
                }
                sendEvent("link_click", {
                    event_name: "link_click",
                    metadata: {
                        href: anchor.getAttribute("href") || "",
                        text: (anchor.textContent || "").trim().slice(0, 120)
                    }
                });
                return;
            }
            var button = target.closest("button,input[type='submit']");
            if (button) {
                sendEvent("button_click", {
                    event_name: "button_click",
                    metadata: {
                        text: ((button.textContent || button.value || "") + "").trim().slice(0, 120)
                    }
                });
            }
        });
    }

    function trackVideoPlays() {
        document.addEventListener("play", function (event) {
            var target = event.target;
            if (!target || !target.tagName || target.tagName.toLowerCase() !== "video") return;
            sendEvent("video_play", {
                event_name: "video_play",
                metadata: {
                    src: target.currentSrc || target.getAttribute("src") || ""
                }
            });
        }, true);
    }

    function trackFirstInputDelay() {
        if (!window.PerformanceObserver) {
            return;
        }
        try {
            var sent = false;
            var observer = new PerformanceObserver(function (entryList) {
                if (sent) {
                    return;
                }
                var first = entryList.getEntries()[0];
                if (!first) {
                    return;
                }
                var fid = Math.round(first.processingStart - first.startTime);
                sendEvent("performance", { fid_ms: fid });
                sent = true;
                observer.disconnect();
            });
            observer.observe({ type: "first-input", buffered: true });
        } catch (e) {
            return;
        }
    }

    function trackForms() {
        document.addEventListener("submit", function (event) {
            var form = event.target;
            if (!form || !form.action) return;
            sendEvent("form_submit", {
                event_name: "form_submit",
                metadata: {
                    action: form.getAttribute("action") || window.location.pathname,
                    method: (form.getAttribute("method") || "GET").toUpperCase()
                }
            });
        });
    }

    function trackPerformance() {
        window.addEventListener("load", function () {
            var navEntries = performance.getEntriesByType("navigation");
            var nav = navEntries && navEntries.length ? navEntries[0] : null;
            var payload = {};
            if (nav) {
                payload.ttfb_ms = Math.round(nav.responseStart);
                payload.duration_ms = Math.round(nav.duration);
            }

            if (window.PerformanceObserver) {
                try {
                    var lcpObserver = new PerformanceObserver(function (entryList) {
                        var entries = entryList.getEntries();
                        var last = entries[entries.length - 1];
                        if (last) {
                            payload.lcp_ms = Math.round(last.startTime);
                        }
                    });
                    lcpObserver.observe({ type: "largest-contentful-paint", buffered: true });
                } catch (e) {
                    return;
                }
            }

            sendEvent("performance", payload);
        });
    }

    function exposeCustomTrackers() {
        window.epciTrackEvent = function (name, metadata) {
            sendEvent("custom_event", {
                event_name: (name || "custom_event").toString().slice(0, 120),
                metadata: metadata || {}
            });
        };
        window.epciTrackConversion = function (name, metadata) {
            sendEvent("conversion", {
                event_name: (name || "conversion").toString().slice(0, 120),
                metadata: metadata || {}
            });
        };
    }

    var pageStart = Date.now();
    sendEvent("page_view");
    trackScrollDepth();
    trackClicks();
    trackForms();
    trackVideoPlays();
    trackFirstInputDelay();
    trackPerformance();
    exposeCustomTrackers();

    window.addEventListener("beforeunload", function () {
        var duration = Date.now() - pageStart;
        sendEvent("session_end", { duration_ms: duration }, true);
    });
})();
