/* login verify */
var first_input = document.querySelectorAll('.form-control');
    first_input.forEach(function(element) {
        element.addEventListener('keyup', function(e) {
            if (element.value.length == element.maxLength) {
                $(element).parent().next().find('input').focus();
            }
        })
    })