boldSidebarElement = () => {
   const sidebarElements = {
      ['/CookIT/account/']: 'userData', 
      ['/CookIT/account/edit']: 'editData', 
      // FIXME: Change to correct path after all views implementation
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
