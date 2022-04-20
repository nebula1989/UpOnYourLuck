var sms_input = document.getElementById("id_phone_number");
var save_button = document.getElementById("save");
var off_button = document.getElementById('id_two_factor_enabled_0');
var on_button = document.getElementById('id_two_factor_enabled_1');

sms_input.addEventListener('keyup', function (event) {
    check_number(sms_input);
});

off_button.addEventListener('click', function(event) {
    save_button.removeAttribute("disabled");
});

on_button.addEventListener('click', function(event) {
    if (document.getElementById('id_phone_number').value != "") {
        save_button.removeAttribute("disabled");
    }
});

function check_number(number) {
    var regex = /^[+][0-9]+ [(]([0-9]){3}[)] ([0-9]){3}-([0-9]){4}$/g;
    if (regex.test(number.value)) {
        number.classList.remove('is-invalid');
        save_button.removeAttribute("disabled");
        number.classList.add('is-valid');
    }
    else {
        number.classList.remove('is-valid');
        number.classList.add('is-invalid');
        save_button.addAttribute("disabled");
    }
}