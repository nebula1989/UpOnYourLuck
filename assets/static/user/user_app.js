document.addEventListener('DOMContentLoaded', function() {
        var display = document.getElementById('id_qr_prompt');
        if (display.value == 'true') {
            $('#newMainModal').modal('show');
        }
    });

function printImg(url) {
    var win = window.open('');
    win.document.write('<img src="' + url + '" height="80%" style='+'"' + 'display: block; margin-left: auto; margin-right: auto;'+'" onload="window.print();window.close()" />');
    win.focus();
}




