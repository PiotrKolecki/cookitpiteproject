boldSidebarElement = () => {
   const sidebarElements = {
      ['/CookIT/account/']: 'userData', 
      ['/CookIT/account/identityEdit']: 'editData', 
      ['/CookIT/account/addRecipe']: 'addRecipe', 
      // FIXME: Change to correct path after all views implementation
      ['/']: 'userRecipes', 
      ['/']: 'userComments', 
   }

   document.getElementsByClassName(
      sidebarElements[window.location.pathname]
   )[0].classList.add('bold')
}

window.addEventListener('load', () => {
   boldSidebarElement();
});
