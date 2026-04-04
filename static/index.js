const input = document.getElementById("symbol-input");
const suggestions = document.getElementById("symbol-suggestions");
const formError = document.getElementById("form-error");
const analyzeForm = document.getElementById("analyze-form");
const loadingOverlay = document.getElementById("loading-overlay");
const errorState = document.body.dataset.errorState;
const ANALYZE_STARTED_AT_KEY = "stockometerAnalyzeStartedAt";

const showLoadingOverlay = () => {
  if (!loadingOverlay) {
    return;
  }
  loadingOverlay.classList.add("is-visible");
  loadingOverlay.setAttribute("aria-hidden", "false");
};

const hideLoadingOverlay = () => {
  if (!loadingOverlay) {
    return;
  }
  loadingOverlay.classList.remove("is-visible");
  loadingOverlay.setAttribute("aria-hidden", "true");
};

const clearAnalyzeState = () => {
  try {
    window.sessionStorage.removeItem(ANALYZE_STARTED_AT_KEY);
  } catch (_error) {
    // Ignore storage failures and fall back to immediate transitions.
  }
};

const scheduleErrorDismiss = () => {
  if (!formError) {
    return;
  }

  window.setTimeout(() => {
    formError.classList.add("is-hidden");
    window.setTimeout(() => {
      formError.remove();
    }, 1200);
  }, 4000);
};

if (formError && loadingOverlay && errorState === "visible") {
  window.requestAnimationFrame(() => {
    window.setTimeout(() => {
      window.setTimeout(() => {
        hideLoadingOverlay();
        clearAnalyzeState();
        window.setTimeout(() => {
          formError.classList.add("is-visible");
          scheduleErrorDismiss();
        }, 220);
      }, 0);
    }, 120);
  });
} else if (formError) {
  clearAnalyzeState();
  formError.classList.add("is-visible");
  scheduleErrorDismiss();
} else {
  clearAnalyzeState();
  hideLoadingOverlay();
}

window.addEventListener("pageshow", () => {
  if (errorState !== "visible") {
    clearAnalyzeState();
    hideLoadingOverlay();
  }
});

if (analyzeForm && loadingOverlay) {
  analyzeForm.addEventListener("submit", () => {
    try {
      window.sessionStorage.setItem(ANALYZE_STARTED_AT_KEY, String(Date.now()));
    } catch (_error) {
      // Ignore storage failures and still show the overlay.
    }
    showLoadingOverlay();
  });
}

if (input && suggestions) {
  let debounceTimer = null;
  let activeIndex = -1;
  let items = [];
  let requestId = 0;

  const closeSuggestions = () => {
    suggestions.hidden = true;
    suggestions.innerHTML = "";
    input.setAttribute("aria-expanded", "false");
    input.removeAttribute("aria-activedescendant");
    activeIndex = -1;
    items = [];
  };

  const setActiveIndex = (nextIndex) => {
    activeIndex = nextIndex;

    const options = suggestions.querySelectorAll(".suggestion");
    options.forEach((option, index) => {
      const isActive = index === activeIndex;
      option.classList.toggle("active", isActive);
      option.setAttribute("aria-selected", isActive ? "true" : "false");
      if (isActive) {
        input.setAttribute("aria-activedescendant", option.id);
        option.scrollIntoView({ block: "nearest" });
      }
    });

    if (activeIndex < 0) {
      input.removeAttribute("aria-activedescendant");
    }
  };

  const chooseSuggestion = (item) => {
    input.value = item.symbol;
    closeSuggestions();
    input.focus();
  };

  const renderStateRow = (message, stateClass) => {
    suggestions.hidden = false;
    input.setAttribute("aria-expanded", "true");
    suggestions.innerHTML = `<div class="suggestion-meta ${stateClass}">${message}</div>`;
    activeIndex = -1;
    items = [];
  };

  const renderSuggestions = (nextItems) => {
    items = nextItems;
    activeIndex = -1;

    if (!items.length) {
      renderStateRow("No matches found", "suggestion-empty");
      return;
    }

    suggestions.hidden = false;
    input.setAttribute("aria-expanded", "true");
    suggestions.innerHTML = items
      .map((item, index) => {
        const optionId = `symbol-suggestion-${index}`;
        const metaLabel = [item.exchange, item.type].filter(Boolean).join(" | ");
        return `
          <button
            id="${optionId}"
            type="button"
            class="suggestion"
            role="option"
            aria-selected="false"
            data-index="${index}"
          >
            <span class="suggestion-label">${item.name}</span>
            <span class="suggestion-symbol">${item.symbol}</span>
            ${metaLabel ? `<span class="suggestion-support">${metaLabel}</span>` : ""}
          </button>
        `;
      })
      .join("");
  };

  const fetchSuggestions = async (query) => {
    const trimmedQuery = query.trim();

    if (trimmedQuery.length < 2) {
      closeSuggestions();
      return;
    }

    const currentRequestId = ++requestId;
    renderStateRow("Searching...", "suggestion-loading");

    try {
      const response = await fetch(`/api/symbols?q=${encodeURIComponent(trimmedQuery)}`);
      const data = response.ok ? await response.json() : [];

      if (currentRequestId !== requestId) {
        return;
      }

      renderSuggestions(Array.isArray(data) ? data.slice(0, 8) : []);
    } catch (_error) {
      if (currentRequestId !== requestId) {
        return;
      }
      closeSuggestions();
    }
  };

  input.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      fetchSuggestions(input.value);
    }, 250);
  });

  input.addEventListener("keydown", (event) => {
    if (suggestions.hidden || !items.length) {
      if (event.key === "Escape") {
        closeSuggestions();
      }
      return;
    }

    if (event.key === "ArrowDown") {
      event.preventDefault();
      setActiveIndex((activeIndex + 1) % items.length);
      return;
    }

    if (event.key === "ArrowUp") {
      event.preventDefault();
      setActiveIndex((activeIndex - 1 + items.length) % items.length);
      return;
    }

    if (event.key === "Enter" && activeIndex >= 0) {
      event.preventDefault();
      chooseSuggestion(items[activeIndex]);
      return;
    }

    if (event.key === "Escape") {
      event.preventDefault();
      closeSuggestions();
    }
  });

  suggestions.addEventListener("mousemove", (event) => {
    const option = event.target.closest(".suggestion");
    if (!option) {
      return;
    }

    setActiveIndex(Number(option.dataset.index));
  });

  suggestions.addEventListener("mousedown", (event) => {
    const option = event.target.closest(".suggestion");
    if (!option) {
      return;
    }

    event.preventDefault();
    chooseSuggestion(items[Number(option.dataset.index)]);
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".autocomplete")) {
      closeSuggestions();
    }
  });
}
