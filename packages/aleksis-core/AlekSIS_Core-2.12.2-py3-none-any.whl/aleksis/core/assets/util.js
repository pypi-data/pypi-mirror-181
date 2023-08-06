window.addEventListener("DOMContentLoaded", function () {
  // Initialize the service worker
  if ("serviceWorker" in navigator) {
    console.debug("Start registration of service worker.");
    navigator.serviceWorker
      .register("/serviceworker.js", {
        scope: "/",
      })
      .then(function () {
        console.debug("Service worker has been registered.");
      })
      .catch(function () {
        console.debug("Service worker registration has failed.");
      });
  }
});
