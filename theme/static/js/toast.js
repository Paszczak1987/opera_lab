(() => {
    const TOAST_SELECTOR = "[data-toast]";
    const PROGRESS_SELECTOR = "[data-toast-progress]";

    const animateToast = (toast) => {
        const lifetime = Number(toast.dataset.toastTimeout) || 10000;
        const progress = toast.querySelector(PROGRESS_SELECTOR);
        let remaining = lifetime;
        let start = performance.now();
        let rafId = null;

        requestAnimationFrame(() => {
            toast.classList.remove("opacity-0", "translate-y-2");
            toast.classList.add("opacity-100", "-translate-y-0");
        });

        const step = (now) => {
            const elapsed = now - start;
            const ratio = Math.max(0, (remaining - elapsed) / lifetime);
            if (progress) {
                progress.style.transform = `scaleX(${ratio})`;
            }
            if (elapsed >= remaining) {
                toast.classList.add("opacity-0", "-translate-y-2");
                cancelAnimationFrame(rafId);
                setTimeout(() => toast.remove(), 300);
                return;
            }
            rafId = requestAnimationFrame(step);
        };

        const startTimer = () => {
            start = performance.now();
            rafId = requestAnimationFrame(step);
        };

        const pauseTimer = () => {
            remaining -= performance.now() - start;
            cancelAnimationFrame(rafId);
        };

        toast.addEventListener("mouseenter", pauseTimer);
        toast.addEventListener("focusin", pauseTimer);
        toast.addEventListener("mouseleave", () => {
            if (remaining > 0) {
                startTimer();
            }
        });
        toast.addEventListener("focusout", () => {
            if (remaining > 0) {
                startTimer();
            }
        });

        startTimer();
    };

    const initToasts = () => {
        document.querySelectorAll(TOAST_SELECTOR).forEach(animateToast);
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initToasts);
    } else {
        initToasts();
    }
})();
