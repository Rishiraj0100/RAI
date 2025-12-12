const buttonVariants = cva(
    "p-[10px_18px] transition-all duration-300 ease-in-out rounded-4xl",
    {
        variants: {
            default: rva("primary"),
            nav: 'text-white hover:color-ember-950 text-md hover:bg-primary-600',
            primary: "text-white bg-primary-600 hover:text-white text-xl hover:bg-primary-400 border-2 border-primary-600 hover:border-white",
            inverted: "hover:text-white hover:bg-primary-600 text-white text-xl bg-primary-400 border-2 hover:border-primary-600 border-white"
        }
    }
)

const anchorVariants = cva(
    "",
    {
        variants: {
            default: rva("button"),
            nav: buttonVariants("nav"),
            button: buttonVariants("primary"),
            inverted: buttonVariants("inverted")
        }
    }
)

class Button extends HTMLButtonElement {
    connectedCallback() {
        setTimeout(() => {
            let variant = (this.getAttribute("variant")||"default").toLowerCase();
            let className = cn(this.getAttribute("class")||"", anchorVariants(variant));
            this.className = className;
        }, 200);
    }
}
class Anchor extends HTMLAnchorElement {
    connectedCallback() {
        setTimeout(() => {
            let variant = (this.getAttribute("variant")||"default").toLowerCase();
            let className = cn(this.getAttribute("class")||"", anchorVariants(variant));
            this.className = className;
        }, 200);
    }
}

window.customElements.define("a-c", Anchor, { extends: "a" })
window.customElements.define("button-c", Button, { extends: "button" })