const imgInput = document.getElementById('id_profile_img')
const imgLabel = document.getElementById('img-label');


imgInput.addEventListener('change', (e) => {
    const profileImg = document.getElementById('current_profile_img');
    console.log(e.srcElement.files[0].size);
    if(e.srcElement.files[0].size > 5000000) {
        // display error to user
        imgLabel.style.display =  'block';
        imgLabel.style.color = 'red'
        imgLabel.setAttribute('aria-live', 'polite')
        // remove imgInput
        imgInput.value = '';
    }
    else {
        imgLabel.style.color = '#CDD1CC';
        imgLabel.style.display =  'none';
        var reader = new FileReader();

        reader.readAsDataURL(e.srcElement.files[0]);
        reader.onload = function() {
        let fileContent = reader.result;

        profileImg.src = fileContent;
        // profileImg.style.maxHeight = '90%'
        // profileImg.style.maxWidth = '80%'
        imgLabel.setAttribute('aria-live', 'off')

    }
    }

})