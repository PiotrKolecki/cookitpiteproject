const removeComment = (commentIdToRemove) => {
   const buttons = document.getElementsByClassName('remove');

   for (let button of buttons) {
      button.disabled = true;
   }

   const formData = new FormData();

   const csrf_token = getCookie("csrftoken");

   formData.append('commentIdToRemove', commentIdToRemove);
   formData.append('csrfmiddlewaretoken', csrf_token);

   const request = new XMLHttpRequest();

   request.onreadystatechange = () => {
      if (request.readyState == 4 && request.status == 200) {
         window.location.reload();
      }
      if (request.readyState === XMLHttpRequest.DONE) {
         for (let button of buttons) {
            button.disabled = false;
         }
      }
   };
   
   request.open("POST", window.origin + '/CookIT/account/userComments/remove');
   request.setRequestHeader('X-CSRFToken', csrf_token);
   request.send(formData);
}
