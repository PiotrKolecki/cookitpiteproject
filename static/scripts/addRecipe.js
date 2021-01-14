var ingredients = [];
var steps = [];

const addNewIngredient = () => {
   const ingredientsWrapper = document.getElementsByClassName('ingredientsWrapper')[0];

   const wrapper = document.createElement('div');
   wrapper.classList.add('ingredient');

   const removeBtn = document.createElement('div');
   removeBtn.classList.add('removeBtn');
   removeBtn.onclick = removeIngredient(ingredients.length);
   removeBtn.innerHTML = '❌';

   const input = document.createElement('input');
   input.classList.add('ingredientInput')
   input.setAttribute('name', 'ingredientIpt');
   input.setAttribute('placeholder', '* Składnik');
   input.setAttribute('required', true);
   input.setAttribute('value', '');

   wrapper.appendChild(removeBtn)
   wrapper.appendChild(input)

   ingredients.push(wrapper);

   ingredientsWrapper.appendChild(wrapper);
}

const removeIngredient = (index) => () => {
   const ingredientsWrapper = document.getElementsByClassName('ingredientsWrapper')[0];
   const inputToRemove = ingredients[index];

   ingredientsWrapper.removeChild(inputToRemove);
}

const addNewStep = () => {
   const stepsWrapper = document.getElementsByClassName('stepsWrapper')[0];

   const wrapper = document.createElement('div');
   wrapper.classList.add('step');

   const removeBtn = document.createElement('div');
   removeBtn.classList.add('removeBtn');
   removeBtn.onclick = removeStep(steps.length);
   removeBtn.innerHTML = '❌';

   const input = document.createElement('input');
   input.classList.add('stepInput')
   input.setAttribute('name', 'stepIpt');
   input.setAttribute('placeholder', '* Krok');
   input.setAttribute('required', true);
   input.setAttribute('value', '');

   wrapper.appendChild(removeBtn)
   wrapper.appendChild(input)

   steps.push(wrapper);

   stepsWrapper.appendChild(wrapper);
}

const removeStep = (index) => () => {
   const stepsWrapper = document.getElementsByClassName('stepsWrapper')[0];
   const stepToRemove = steps[index];

   stepsWrapper.removeChild(stepToRemove);
}

validateForm = () => {
   const recipeName = document.getElementsByName('recipeName')[0].value;
   const validationMsg = document.getElementsByClassName('errorMsg')[0];
   
   if (recipeName == "") {
      validationMsg.innerHTML = 'Podaj nazwę przepisu';

      return false;
   }

   const description = document.getElementsByName('description')[0].value;

   if (description == "") {
      validationMsg.innerHTML = 'Uzupełnij opis przepisu';

      return false;
   }

   const ingredientsWrapper = document.getElementsByClassName('ingredientsWrapper')[0];

   if (ingredientsWrapper.children.length === 0) {
      validationMsg.innerHTML = 'Dodaj składniki';

      return false;
   }

   let hasEmptyIngredient = false;

   for (let ingredient of ingredientsWrapper.children) {
      if (ingredient.children[1].value === '') {
         hasEmptyIngredient = true;
         break;
      }
   }

   if (hasEmptyIngredient) {
      validationMsg.innerHTML = 'Uzupełnij składniki';

      return false;
   }

   const stepsWrapper = document.getElementsByClassName('stepsWrapper')[0];

   if (stepsWrapper.children.length === 0) {
      validationMsg.innerHTML = 'Dodaj wymagane kroki';

      return false;
   } 

   let hasEmptyStep = false;

   for (let step of stepsWrapper.children) {
      if (step.children[1].value === '') {
         hasEmptyStep = true;
         break;
      }
   }
   
   if (hasEmptyStep) {
      validationMsg.innerHTML = 'Uzupełnij kroki';

      return false;
   }

   validationMsg.innerHTML = '';
   return true;
}

addRecipe = () => {
   const didPassedValidation = validateForm();

   if(didPassedValidation) {
      const button = document.getElementsByClassName('saveRecipe')[0];
      button.disabled = true;

      const ingredientsWrapper = document.getElementsByClassName('ingredientsWrapper')[0];
      const stepsWrapper = document.getElementsByClassName('stepsWrapper')[0];
      const ingredients = [];
      const steps = [];

      for (let ingredient of ingredientsWrapper.children) {
         ingredients.push(ingredient.children[1].value)
      }

      for (let step of stepsWrapper.children) {
         steps.push(step.children[1].value)
      }

      const formData = new FormData();

      const recipeName = document.getElementsByName('recipeName')[0].value.toUpperCase();
      const description = document.getElementsByName('description')[0].value;
      const category = document.getElementsByName('category')[0].value;
      const ingredientsValue = ingredients.join('|');
      const stepsValue = steps.join('|');
      const csrf_token = getCookie("csrftoken");

      formData.append('category', category);
      formData.append('recipeName', recipeName);
      formData.append('description', description);
      formData.append('ingredients', ingredientsValue);
      formData.append('steps', stepsValue);
      formData.append('csrfmiddlewaretoken', csrf_token);

      const request = new XMLHttpRequest();

      request.onreadystatechange = () => {
         if (request.readyState == 4 && request.status == 200) {
            window.location.reload();
         }
         if (request.readyState === XMLHttpRequest.DONE) {
            button.disabled = false;
         }
      };
      
      request.open("POST", window.origin + '/CookIT/addComment/sendData');
      request.setRequestHeader('X-CSRFToken', csrf_token);
      request.send(formData);
   }
}
