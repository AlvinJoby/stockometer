const divider = document.getElementById("drag-divider");
const mainPanel = document.querySelector(".main-panel");
const returnsPanel = document.querySelector(".returns-panel");
const container = document.querySelector(".front-layout");
const pageLoadingOverlay = document.getElementById("page-loading-overlay");
const MINIMUM_PAGE_LOADER_MS = 3000;
const pageLoaderStartedAt = Date.now();

let isDragging = false;

function getPlotDiv() {
  return mainPanel?.querySelector(".js-plotly-plot") ?? null;
}

function syncMainChartLayout() {
  const plotDiv = getPlotDiv();
  if (!plotDiv || typeof Plotly === "undefined") return;

  const chartWidth = mainPanel?.getBoundingClientRect().width ?? window.innerWidth;
  const isMobile = chartWidth <= 768;

  Plotly.relayout(plotDiv, {
    autosize: true,
    margin: isMobile
      ? { l: 8, r: 44, t: 16, b: 32 }
      : { l: 10, r: 54, t: 20, b: 40 },
  });
}

function hidePageLoader() {
  if (!pageLoadingOverlay) return;
  pageLoadingOverlay.classList.add("is-hidden");
  pageLoadingOverlay.setAttribute("aria-hidden", "true");
}

function enterChartLoaderStage() {
  if (!pageLoadingOverlay) return;
  pageLoadingOverlay.classList.add("is-chart-stage");
}

if (divider) {
  divider.addEventListener("mousedown", () => {
    isDragging = true;
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
  });
}

document.addEventListener("mousemove", (e) => {
  if (!isDragging) return;

  const containerRect = container.getBoundingClientRect();
  const totalWidth = containerRect.width;
  const offsetX = e.clientX - containerRect.left;

  const mainPct = Math.min(Math.max((offsetX / totalWidth) * 100, 70), 85);
  const returnsPct = 100 - mainPct - 0.4;

  mainPanel.style.flex = `0 0 ${mainPct}%`;
  returnsPanel.style.flex = `0 0 ${returnsPct}%`;
  syncMainChartLayout();
});

document.addEventListener("mouseup", () => {
  isDragging = false;
  document.body.style.cursor = "";
  document.body.style.userSelect = "";
});

window.addEventListener("load", () => {
  syncMainChartLayout();
  window.requestAnimationFrame(() => {
    window.requestAnimationFrame(() => {
      enterChartLoaderStage();
      const remainingTime = Math.max(0, MINIMUM_PAGE_LOADER_MS - (Date.now() - pageLoaderStartedAt));
      window.setTimeout(() => {
        hidePageLoader();
      }, remainingTime);
    });
  });
});
window.addEventListener("resize", syncMainChartLayout);
