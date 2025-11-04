(() => {
    const lockedClasses = ["cursor-not-allowed"];

    const sortSelect = (selectElement) => {
        const options = Array.from(selectElement.options);
        options.sort((a, b) => a.text.localeCompare(b.text, "pl", { sensitivity: "base" }));
        selectElement.innerHTML = "";
        options.forEach((option) => {
            selectElement.add(option);
        });
    };

    const hasMovableSelection = (selectElement) =>
        Array.from(selectElement.selectedOptions).some((option) => option.dataset.locked !== "true");

    const applyLockedState = (option, shouldLock) => {
        const lockState = shouldLock ? "true" : "false";
        option.dataset.locked = lockState;
        option.disabled = shouldLock;
        lockedClasses.forEach((cls) => option.classList.toggle(cls, shouldLock));
    };

    const ensureFormSubmitHandler = (form) => {
        if (!form || form.dataset.dualListSubmitBound === "true") {
            return;
        }
        form.addEventListener("submit", () => {
            form.querySelectorAll('select[data-role="selected"]').forEach((select) => {
                Array.from(select.options).forEach((option) => {
                    option.selected = true;
                });
            });
        });
        form.dataset.dualListSubmitBound = "true";
    };

    const initDualList = (container) => {
        const available = container.querySelector('select[data-role="available"]');
        const selected = container.querySelector('select[data-role="selected"]');
        if (!available || !selected) {
            return;
        }

        const addButton = container.querySelector('[data-action="add"]');
        const removeButton = container.querySelector('[data-action="remove"]');
        const form = container.closest("form");
        ensureFormSubmitHandler(form);

        const updateButtonsState = () => {
            if (addButton) {
                addButton.disabled = !hasMovableSelection(available);
            }
            if (removeButton) {
                removeButton.disabled = selected.selectedOptions.length === 0;
            }
        };

        const moveOptions = (source, target, selectInTarget) => {
            const movable = Array.from(source.selectedOptions).filter((option) => option.dataset.locked !== "true");
            if (!movable.length) {
                return;
            }

            movable.forEach((option) => {
                option.selected = Boolean(selectInTarget);
                target.add(option);

                const assignedAnywhere = option.dataset.assignedAnywhere === "true";
                if (target === selected) {
                    applyLockedState(option, false);
                    option.classList.remove("option-assigned");
                    option.classList.add("option-available");
                } else {
                    const shouldLock = option.dataset.originalLocked === "true";
                    applyLockedState(option, shouldLock);
                    option.classList.toggle("option-assigned", assignedAnywhere);
                    option.classList.toggle("option-available", !assignedAnywhere);
                }
            });

            sortSelect(target);
            sortSelect(source);
            updateButtonsState();
        };

        addButton?.addEventListener("click", () => moveOptions(available, selected, true));
        removeButton?.addEventListener("click", () => moveOptions(selected, available, false));

        available.addEventListener("dblclick", (event) => {
            if (event.target instanceof HTMLOptionElement && event.target.dataset.locked !== "true") {
                moveOptions(available, selected, true);
            }
        });
        selected.addEventListener("dblclick", (event) => {
            if (event.target instanceof HTMLOptionElement) {
                moveOptions(selected, available, false);
            }
        });

        available.addEventListener("change", updateButtonsState);
        selected.addEventListener("change", updateButtonsState);
        updateButtonsState();
    };

    const initDualLists = () => {
        document.querySelectorAll("[data-dual-list]").forEach((container) => initDualList(container));
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initDualLists);
    } else {
        initDualLists();
    }
})();
