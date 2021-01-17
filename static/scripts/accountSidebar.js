boldSidebarElement = () => {
   const sidebarElements = {
      ['/CookIT/account/']: 'userData', 
      ['/CookIT/account/identityEdit']: 'editData', 
      ['/CookIT/account/addRecipe']: 'addRecipe', 
      ['/CookIT/account/userRecipes']: 'userRecipes', 
      ['/CookIT/account/userComments']: 'userComments', 
   }

   if(sidebarElements[window.location.pathname]) {
      document.getElementsByClassName(
         sidebarElements[window.location.pathname]
      )[0].classList.add('bold')
   }

   if(window.location.pathname.includes('/CookIT/account/userRecipes/edit-')) {
      document.getElementsByClassName(
         sidebarElements['/CookIT/account/userRecipes']
      )[0].classList.add('bold')
   }

   if(window.location.pathname.includes('/CookIT/account/userComments/edit-')) {
      document.getElementsByClassName(
         sidebarElements['/CookIT/account/userComments']
      )[0].classList.add('bold')
   }
}

window.addEventListener('load', () => {
   boldSidebarElement();
});
