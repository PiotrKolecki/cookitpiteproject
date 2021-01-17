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

const setRecommendedPosition = () => {
  const recommendedRecipes = document.getElementsByClassName('recommendedRecipes')[0];
  const listHeight = document.getElementsByClassName('recommendedWrapper')[0].offsetHeight;
  
  recommendedRecipes.style.bottom = -listHeight + 'px';
  recommendedRecipes.classList.remove('hide');
}

const toggleRecommended = () => {
  const recommendedRecipes = document.getElementsByClassName('recommendedRecipes')[0];
  const listHeight = document.getElementsByClassName('recommendedWrapper')[0].offsetHeight;

  if (recommendedRecipes.style.bottom !== '0px') {
    recommendedRecipes.style.bottom = 0 + 'px';
  } else {
    recommendedRecipes.style.bottom = -listHeight + 'px';
  }
}

window.addEventListener('load', () => {
  setRecommendedPosition();
});

