function tcmodal_eval(group_id) {
    var checkboxes = document.querySelectorAll("[id^='checkbox-" + group_id + "']");
    var allchecked = true;
    checkboxes.forEach((element) => {
        if (element.checked !== true) allchecked = false;
    });


    var button = document.getElementById('button-' + group_id);
    button.disabled = !allchecked;
}

function tcmodal(group_id) {
    var modal = document.getElementById(group_id);

    if (modal.style.display == "none" || ! modal.style.display ) {
        modal.style.display = "inline";
    } else {
        modal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}
