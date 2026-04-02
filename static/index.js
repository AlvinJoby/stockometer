const input = document.getElementById("symbol-input");
const suggestions = document.getElementById("symbol-suggestions");

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
        const exchangeLabel = item.exchange ? ` · ${item.exchange}` : "";
        const typeLabel = item.type ? ` · ${item.type}` : "";
        return `
          <button
            id="${optionId}"
            type="button"
            class="suggestion"
            role="option"
            aria-selected="false"
            data-index="${index}"
          >
            <span class="suggestion-symbol">${item.symbol}</span>
            <span class="suggestion-label">${item.name}${exchangeLabel}${typeLabel}</span>
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
