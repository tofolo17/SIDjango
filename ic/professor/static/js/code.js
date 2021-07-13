function scrollToTop() {
    window.scrollTo({top: 0, behavior: 'smooth'});
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

function copyLink(param) {
    const el = document.createElement('textarea');
    if (param === "updated") {
        el.value = "http://" + "{{ request.get_host }}" + "/simulator/published/{{ token }}";
    } else {
        el.value = "http://" + "{{ request.get_host }}" + "/simulator/published/" + param;
    }
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    window.alert("Link copiado.")
}
