const setInitialValues = () => {
   const options = document.getElementsByClassName('option');

   for (let option of options) {
      if (Number(option.value) == initialRating) {
         option.selected = true;
         break;
      }
   }
}

window.addEventListener('load', () => {
   setInitialValues();
});

validateForm = () => {
   const comment = document.getElementsByName('comment')[0].value;
   const validationMsg = document.getElementsByClassName('validationMsg')[0];
   
   if (comment == "") {
      validationMsg.innerHTML = 'Pole nie może być puste';

      return false;
   } else {
      validationMsg.innerHTML = '';

      return true;
   }
}

editComment = (commentId) => {
   const didPassedValidation = validateForm();

   if(didPassedValidation) {
      const button = document.getElementsByClassName('editComment')[0];
      button.disabled = true;

      const formData = new FormData();

      const comment = document.getElementsByName('comment')[0];
      const rating = document.getElementsByName('rating')[0];
      const csrf_token = getCookie("csrftoken");

      formData.append('commentId', commentId);
      formData.append('comment', comment.value);
      formData.append('rating', Number(rating.value));
      formData.append('csrfmiddlewaretoken', csrf_token);

      const request = new XMLHttpRequest();

      request.onreadystatechange = () => {
         if (request.readyState == 4 && request.status == 200) {
            window.location.reload();
         } else if (request.readyState === XMLHttpRequest.DONE) {
            button.disabled = false;
         }
      };
      
      request.open("POST", window.origin + '/CookIT/account/userComments/edit/sendData');
      request.setRequestHeader('X-CSRFToken', csrf_token);
      request.send(formData);
   }
}
