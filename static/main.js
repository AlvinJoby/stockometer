const divider = document.getElementById("drag-divider");
const mainPanel = document.querySelector(".main-panel");
const returnsPanel = document.querySelector(".returns-panel");
const container = document.querySelector(".front-layout");

let isDragging = false;

divider.addEventListener("mousedown", (e) => {
  isDragging = true;
  document.body.style.cursor = "col-resize";
  document.body.style.userSelect = "none";
});

document.addEventListener("mousemove", (e) => {
  if (!isDragging) return;

  const containerRect = container.getBoundingClientRect();
  const totalWidth = containerRect.width;
  const offsetX = e.clientX - containerRect.left;

  const mainPct = Math.min(Math.max((offsetX / totalWidth) * 100, 70), 85);
  const returnsPct = 100 - mainPct - 0.4;

  mainPanel.style.flex = `0 0 ${mainPct}%`;
  returnsPanel.style.flex = `0 0 ${returnsPct}%`;

  const plotDiv = mainPanel.querySelector(".js-plotly-plot");
  if (plotDiv) Plotly.relayout(plotDiv, { autosize: true });
});

document.addEventListener("mouseup", () => {
  isDragging = false;
  document.body.style.cursor = "";
  document.body.style.userSelect = "";
});
