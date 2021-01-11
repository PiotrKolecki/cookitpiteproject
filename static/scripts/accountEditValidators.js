validateEditForm = () => {
    const form = document.getElementsByName('editForm')[0];
    const first_name = document.getElementsByName('first_name')[0].value;
    const last_name = document.getElementsByName('last_name')[0].value;
    const email = document.getElementsByName('email')[0].value;
    const errorDiv = document.getElementsByClassName('errorMsg')[0];
    
    if ( first_name == "" || last_name == "" || email == "") {
        errorDiv.innerHTML = 'Uzupełnij wymagane pola';
    } else {
        if (validateEmail(email)) {
            errorDiv.innerHTML = '';
            form.submit();
        } else {
            errorDiv.innerHTML = 'niepoprawny E-mail';
        }
    }
 }

 function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
  }