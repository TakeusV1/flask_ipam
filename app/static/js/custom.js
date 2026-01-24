if (history.scrollRestoration) {
    history.scrollRestoration = 'manual';
}

function instantCenter() {
    const hash = window.location.hash;
    if (!hash) return;

    const targetId = hash.substring(1);
    const element = document.getElementById(targetId);

    if (element) {
        setTimeout(() => {
            const elementRect = element.getBoundingClientRect();
            const absoluteElementTop = elementRect.top + window.scrollY;
            
            const middle = absoluteElementTop - (window.innerHeight / 2) + (elementRect.height / 2);

            window.scrollTo({
                top: middle,
                behavior: 'auto'
            });
        }, 0); 
    }
}

window.addEventListener('load', instantCenter);