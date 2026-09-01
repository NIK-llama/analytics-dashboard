(function() {
    // Analytics API URL - change this when deploying to production!
    const API_URL = "http://localhost:8000/api/events/";

    function trackEvent() {
        const payload = {
            page: window.location.pathname,
            referrer: document.referrer || "",
            session_id: getSessionId(),
            user_agent: navigator.userAgent
        };

        // We use sendBeacon so the request isn't cancelled if the user navigates away
        if (navigator.sendBeacon) {
            navigator.sendBeacon(API_URL, JSON.stringify(payload));
        } else {
            fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
                keepalive: true
            });
        }
    }

    function getSessionId() {
        let sessionId = sessionStorage.getItem("ana_session_id");
        if (!sessionId) {
            sessionId = crypto.randomUUID ? crypto.randomUUID() : 'req-' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem("ana_session_id", sessionId);
        }
        return sessionId;
    }

    // Track page view on load
    if (document.readyState === "complete") {
        trackEvent();
    } else {
        window.addEventListener("load", trackEvent);
    }
})();
