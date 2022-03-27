let form = document.getElementById('contact-form');
    let formElements = form.children;
    // console.log(formElements.style);
    for(ele of form.children) {
        ele.style.marginTop = '2%';
    }


let updateUsername = (username) => {
    document.getElementById('id_username').value = document.getElementById('username_field').innerText
}

let updateEmail = (email) => {
    document.getElementById('id_email').value = document.getElementById('email_field').innerText
}

updateUsername()
updateEmail()
