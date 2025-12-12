const inputVariants = cva(
  "",
  {
    variants: {
        default: "block w-full rounded-md px-3.5 py-2 text-base text-white outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600",
        radio: "peer h-5 w-5 cursor-pointer appearance-none rounded-full border-2 outline-indigo-800 outline-1 border-white checked:bg-indigo-800 transition-all",
        textarea: rva("default", "custom-scrollbar resize-y"),
    }
  }
)

class Input extends HTMLInputElement {
    connectedCallback() {
        setTimeout(() => {
            let variant = (this.getAttribute("type")||"text").toLowerCase();
            variant = ["radio"].includes(variant)?variant:"default";
            let className = cn(this.getAttribute("class")||"", inputVariants(variant));
            this.className = className;
        }, 200);
    }
}

class TextArea extends HTMLTextAreaElement {
    connectedCallback() {
        setTimeout(() => {
            let className = cn(this.getAttribute("class")||"", inputVariants("textarea"));
            this.className = className;
        }, 200);
    }
}

class Select extends HTMLSelectElement {
    connectedCallback() {
                if (this._initialized) return;
        this._initialized = true;

        // queueMicrotask(() => this.init());
        setTimeout(() => this.init(), 200);
    }

    init() {
        const select = this;

        // Hide original select
        select.classList.add("hidden");

        // Wrapper
        const wrapper = document.createElement("div");
        wrapper.className = "relative inline-block w-full";

        // Input (display value)
        const input = document.createElement("input", { is: "input-c" });
        input.type = "text";
        input.className = "w-full p-2 border rounded cursor-pointer";
        input.value = select.options[select.selectedIndex]?.textContent || "";
        input.readOnly = true;
        input.setAttribute("role", "combobox");
        input.setAttribute("aria-expanded", "false");

        // Dropdown list
        const ul = document.createElement("ul");
        ul.className =
            "absolute left-0 custom-scrollbar right-0 bg-primary-800 text-white rounded shadow-lg max-h-60 overflow-auto hidden z-50";
        ul.setAttribute("role", "listbox");

        // Build items
        const items = [];
        [...select.options].forEach((option, index) => {
            const li = document.createElement("li");
            li.className =
                "p-2 cursor-pointer hover:bg-accent focus:bg-accent";
            li.textContent = option.textContent;
            li.setAttribute("role", "option");
            li.dataset.value = option.value;
            li.tabIndex = -1;

            // Selection handler (mousedown = best practice)
            li.addEventListener("mousedown", () => {
                select.value = option.value;
                input.value = option.textContent;
                this.dispatchEvent(new Event("change"));
                closeList();
            });

            ul.appendChild(li);
            items.push(li);
        });

        // Insert elements
        const parent = select.parentElement;
        parent.insertBefore(wrapper, select);
        wrapper.appendChild(select);
        wrapper.appendChild(input);
        wrapper.appendChild(ul);

        // ---- Dropdown Control ----

        let open = false;
        let activeIndex = -1;

        const openList = () => {
            if (open) return;
            open = true;
            ul.classList.remove("hidden");
            input.setAttribute("aria-expanded", "true");
        };

        const closeList = () => {
            if (!open) return;
            open = false;
            ul.classList.add("hidden");
            input.setAttribute("aria-expanded", "false");
            activeIndex = -1;
            clearActive();
        };

        // Keyboard navigation
        input.addEventListener("keydown", (e) => {
            if (e.key === "ArrowDown") {
                e.preventDefault();
                openList();
                moveActive(1);
            } else if (e.key === "ArrowUp") {
                e.preventDefault();
                openList();
                moveActive(-1);
            } else if (e.key === "Enter" && activeIndex >= 0) {
                e.preventDefault();
                items[activeIndex].dispatchEvent(new Event("mousedown"));
            } else if (e.key === "Escape") {
                closeList();
            }
        });
        input.addEventListener("focus", openList);

        // Toggle on click
        input.addEventListener("click", () => {
            if (open) closeList();
            else openList();
        });

        // Close when clicking outside
        document.addEventListener("mousedown", (e) => {
            if (!wrapper.contains(e.target)) closeList();
        });

        // ---- Helpers ----

        const clearActive = () => {
            items.forEach((item) =>
                item.classList.remove("bg-accent")
            );
        };

        const moveActive = (direction) => {
            clearActive();
            activeIndex += direction;

            if (activeIndex < 0) activeIndex = items.length - 1;
            if (activeIndex >= items.length) activeIndex = 0;

            const item = items[activeIndex];
            item.classList.add("bg-accent");

            // Scroll into view smoothly
            item.scrollIntoView({ block: "nearest" });
        };
    }
}

window.customElements.define("input-c", Input, { extends: "input" })
window.customElements.define("select-c", Select, { extends: "select" })
window.customElements.define("textarea-c", TextArea, { extends: "textarea" })