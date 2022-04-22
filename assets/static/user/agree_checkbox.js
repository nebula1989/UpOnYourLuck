const userField = document.getElementById('id_username');
const fNameField = document.getElementById('id_first_name');
const lNameField = document.getElementById('id_last_name');
const emailField = document.getElementById('id_email');
const pwField = document.getElementById('id_password1');
const pw2Field = document.getElementById('id_password2');
const fields = [userField, fNameField, lNameField, emailField, pwField, pw2Field]

// errors
const userErr = document.getElementById('username-err-msg')



const labelsArray = document.getElementsByTagName('label')
const agreeLabel = labelsArray[labelsArray.length-1];
const agreeInputCheck = document.getElementById('form2Example3cg');
const registerBtn = document.getElementsByTagName('button')[1];

userField.blur()


/* Add functionality to make clicking Agreement text check */
agreeLabel.addEventListener('click', () => {
    if(!agreeInputCheck.checked) {
        agreeInputCheck.checked = true;
    }
    else {
        agreeInputCheck.checked = false;
    }
})


    function changeFieldToError(domEle) {
        domEle.style.borderColor = '#dc3545';
        domEle.style.backgroundImage = "url(\"data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e\")";
        domEle.addEventListener('focus', () => {
            domEle.style.boxShadow = '0 0 0 0.25rem rgb(220 53 69 / 25%)'

            })
            domEle.addEventListener('blur', () => {
                domEle.style.boxShadow = 'none'

            })
            domEle.focus();
    }

    function changeFieldToValid(domEle) {
        domEle.style.borderColor = '#198754';
        domEle.style.backgroundImage = "url(\"data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 8'%3e%3cpath fill='%23198754' d='M2.3 6.73L.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1z'/%3e%3c/svg%3e\")"

        domEle.addEventListener('focus', () => {
            domEle.style.boxShadow = '0 0 0 0.25rem rgb(25 135 84 / 25%)'

            })
            domEle.addEventListener('blur', () => {
                domEle.style.boxShadow = 'none'

            })
            domEle.focus();
    }

    function addPasswordError(err) {
        let pwErrMsgDiv = document.createElement('div');
        pwErrMsgDiv.classList.add('form-check')
        pwErrMsgDiv.classList.add('d-flex')
        pwErrMsgDiv.classList.add('justify-content-center')
        pwErrMsgDiv.classList.add('mb-1')
        pwErrMsgDiv.setAttribute("aria-live", "polite")
        pwErrMsgDiv.id = 'pw2-err-msg'
        pwErrMsgDiv.innerText = err
        document.getElementById('tos-div').insertAdjacentElement('beforebegin', pwErrMsgDiv);
    }

function addUserErr(msg) {
    userErr.textContent = msg
    changeFieldToError(userField);
    userErr.setAttribute('aria-live', 'polite');
    userField.addEventListener('input', () => {
        changeFieldToValid(userField);
        userField.style.boxShadow = '0 0 0 0.25rem rgb(25 135 84 / 25%)'
        userErr.style.display = 'none'
        userErr.setAttribute('aria-live', 'off');
    })
}

if(errMessages) {
    // Check for error messages for username
    console.log(errMessages);
    if(errMessages[0].startsWith('A user')) {
        // set the field to invalid basically
        addUserErr(errMessages[0])
    }
    else if(errMessages[0].startsWith("This password") || errMessages[0].startsWith("The two password")) {
        // might need to add more here, if not keeping the default red styles
        pwField.focus();
        addPasswordError(errMessages[0])


    }
    if(errMessages.length == 2 && (errMessages[1].startsWith("This password") || errMessages[1].startsWith("The two password fields didn't match"))) {
        addPasswordError(errMessages[1]);
    }
    if(errMessages.length == 2 && errMessages[1].startsWith("user")) {
        addUserErr(errMessages[1]);
    }

}

function displayUsernameError() {
    const userField = document.getElementById('id_username')
    userField.classList.add('form-is-invalid');

}