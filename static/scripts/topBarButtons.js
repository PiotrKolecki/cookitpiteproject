logout = () => {
   document.cookie = "userSession" +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
   window.location.href = "/CookIT/logout";
}

getCookie = (cname) => {
   var name = cname + "=";
   var decodedCookie = decodeURIComponent(document.cookie);
   var ca = decodedCookie.split(';');
   for(var i = 0; i <ca.length; i++) {
     var c = ca[i];
     while (c.charAt(0) == ' ') {
       c = c.substring(1);
     }
     if (c.indexOf(name) == 0) {
       return c.substring(name.length, c.length);
     }
   }
   return "";
 }

setCorrectButtons =() => {
   const sessionCookie = getCookie("userSession");
   const navButtonsWrapper = document.getElementsByClassName("navButtonsWrapper")[0];
 
   if (!sessionCookie)  {
      navButtonsWrapper.innerHTML = `
         <a class="loginButton" href="/CookIT/login/">Zaloguj się</a>
      `;
   } else {
      navButtonsWrapper.innerHTML = `
         <a class="accountButton" href="/CookIT/account">Twoje konto</a>
         <button class="logoutButton" onclick="logout()">Wyloguj</button>
      `;
   }
}

window.addEventListener('load', () => {
   setCorrectButtons();
});
