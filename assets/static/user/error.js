/* other form validation stuff */
let err = document.getElementById('error-message');
let errList = err.getElementsByClassName('errorlist');

let errMessage = err.textContent;
// remove first instance of username
if(errMessage.substring(0, 8) == 'username') {
    errMessage = errMessage.substring(8);
}
// remove first instance of password2
else if(errMessage.substring(0, 9) == 'password2') {
    errMessage = errMessage.substring(9);
}
// check if 2 errors
let errMessages = errMessage.split('password2');
if(errMessages.length == 1) {
    errMessages = errMessage.split('usernameA')
    for(let i = 0; i < errMessages.length; i++) {
        errMessages[i] = errMessages[i].trim()
    }
}