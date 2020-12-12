validateLoginForm = () => {
   const form = document.getElementsByName('loginForm')[0];
   const login = document.getElementsByName('login')[0].value;
   const password = document.getElementsByName('password')[0].value;
   const errorDiv = document.getElementsByClassName('errorMsg')[0];

   if (login == "" || password == "") {
      errorDiv.innerHTML = 'Uzupełnij wymagane pola';
   } else {
      errorDiv.innerHTML = '';

      const xhr = new XMLHttpRequest();
      xhr.open('POST', 'login', true);
      form.submit();
   }
}

validateRegisterForm = () => {
   const form = document.getElementsByName('registerForm')[0];
   const newLogin = document.getElementsByName('newLogin')[0].value;
   const newPassword = document.getElementsByName('newPassword')[0].value;
   const repeatPassword = document.getElementsByName('repeatPassword')[0].value;
   const errorDiv = document.getElementsByClassName('errorMsg')[0];
   
   if (newPassword !== repeatPassword) {
      errorDiv.innerHTML = 'Podane hasła nie są zgodne';
   } else if (newLogin == "" || newPassword == "" || repeatPassword == "") {
      errorDiv.innerHTML = 'Uzupełnij wymagane pola';
   } else {
      errorDiv.innerHTML = '';
      form.submit();
   }
}
