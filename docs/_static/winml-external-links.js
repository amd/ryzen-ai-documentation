document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelectorAll('a[href*="/projects/winml/"]')
    .forEach(function (link) {
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noopener noreferrer");
    });
});
