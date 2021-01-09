boldSidebarElement = () => {
   const sidebarElements = {
      ['/CookIT/account/']: 'userData', 
      // FIXME: Change to correct path after all views implementation
      ['/']: 'editData', 
      ['/']: 'addRecipe', 
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
