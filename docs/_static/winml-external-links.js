document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelectorAll(
      'a[href*="/projects/advanced-micro-devices-windows-ml-for-ryzen-ai/"]'
    )
    .forEach(function (link) {
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noopener noreferrer");
    });
});
