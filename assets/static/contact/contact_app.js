let form = document.getElementById('contact-form');
    let formElements = form.children;
    // console.log(formElements.style);
    for(ele of form.children) {
        ele.style.marginTop = '2%';
    }

function Verify(e) {
    document.getElementById('form-submit').removeAttribute('disabled');
  }