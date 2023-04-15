var currentTab = 0;

$('.date').datepicker({
  multidate: true,
	format: 'yyyy-mm-dd'
});


window.addEventListener('DOMContentLoaded', () => {
    showTab(currentTab);
})

function loadImage(element) {
    document.getElementById('image').src = element.value;
}

function textAreaAdjust(element) {
    element.style.height = "1px";
    element.style.height = (25+element.scrollHeight)+"px";
}

function showTab(n) {
    var x = document.getElementsByClassName("tab");
    x[n].style.display = "block";

    if (n == 0)
        document.getElementById("prevBtn").style.display = "none";
    else
        document.getElementById("prevBtn").style.display = "inline";

    if (n == (x.length - 1))
        document.getElementById("nextBtn").innerHTML = "Submit";
    else
        document.getElementById("nextBtn").innerHTML = "Next";

    fixStepIndicator(n)
}

function nextPrev(n) {
  var x = document.getElementsByClassName("tab");

  if (n == 1 && !validateForm()) return false;
  //if(n == 1) document.getElementsByClassName("step")[currentTab].className += " finish";
  
  x[currentTab].style.display = "none";
  currentTab = currentTab + n;
  if (currentTab >= x.length) {
    fixInput();
    document.getElementById("form").submit();
    return false;
  }
  showTab(currentTab);
}

function validateForm() {
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  for (i = 0; i < y.length; i++) {
    if (y[i].value === "" && y[i].required) {
      y[i].className += " invalid";
      valid = false;
    } else if ( y[i].value === "" && y[i].id === "cap" && document.getElementById('GRP').checked) {
      y[i].className += " invalid";
      valid = false;
    } else if ( y[i].value === "" && y[i].id === "dates" && document.getElementById('GRP').checked) {
      y[i].className += " invalid";
      valid = false;
    }
  }
  y = x[currentTab].getElementsByTagName("textarea");
  for (i = 0; i < y.length; i++) {
    if (y[i].value === "" && y[i].required == true) {      
      y[i].className += " invalid";
      valid = false;
    }
  }

  if(!document.getElementById('imgerr').hidden) valid = false;

  if (valid)
    document.getElementsByClassName("step")[currentTab].className += " finish";
  return valid;
}

function fixStepIndicator(n) {
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++)
    x[i].className = x[i].className.replace(" active", "");
  x[n].className += " active";
}

function notInvalid(element) {
    if(element.classList.contains("invalid"))
        element.classList.remove("invalid");
}

function addCountry(element) {
    hidden = document.getElementById("hiddenCountry");
    
    var options = document.getElementById("countries").options;
    var result = false;

    for(var i=0;i<options.length;++i){
        if(element.previousElementSibling.value === options[i].value) {
            result = true;
            break;
        }
    }

    if(!result)
        return false;

    hidden.value = parseInt(hidden.value) + 1;

    let div = document.createElement("div");
    div.classList.add("field-group")

    let field = document.createElement("input");
    field.setAttribute("list","countries");
    field.classList.add("text-field");
    field.placeholder = "Enter a country";
    field.required = true;
    field.setAttribute("oninput","notInvalid(this)");

    let addBtn = document.createElement("button");
    addBtn.innerHTML = "Add";
    addBtn.classList.add("button-submit");
    addBtn.type = "button";
    addBtn.setAttribute("onclick","addCountry(this)");

    let delBtn = document.createElement("button");
    delBtn.innerHTML = "Remove";
    delBtn.classList.add("button-delete");
    delBtn.type = "button";
    delBtn.style.display = "none";
    delBtn.setAttribute("onclick","removeCountry(this)");

    hidden.parentNode.insertBefore(div,hidden);

    div.appendChild(field);
    div.appendChild(addBtn);
    div.appendChild(delBtn);

    element.nextElementSibling.style.display = "block";
    element.style.display = "none";

}

function removeCountry(element) {
  element.parentElement.remove();
  hidden = document.getElementById("hiddenCountry");
  hidden.value = parseInt(hidden.value) - 1;
}

function addTag(element) {
  hidden = document.getElementById("hiddenTag");
  
  var options = document.getElementById("tags").options;
  var result = false;

  for(var i=0;i<options.length;++i){
      if(element.previousElementSibling.value === options[i].value) {
          result = true;
          break;
      }
  }

  if(!result)
      return false;

  hidden.value = parseInt(hidden.value) + 1;

  let div = document.createElement("div");
  div.classList.add("field-group")

  let field = document.createElement("input");
  field.setAttribute("list","tags");
  field.classList.add("text-field");
  field.placeholder = "Add a tag";
  field.required = true;
  field.setAttribute("oninput","notInvalid(this)");

  let addBtn = document.createElement("button");
  addBtn.innerHTML = "Add";
  addBtn.classList.add("button-submit");
  addBtn.type = "button";
  addBtn.setAttribute("onclick","addTag(this)");

  let delBtn = document.createElement("button");
  delBtn.innerHTML = "Remove";
  delBtn.classList.add("button-delete");
  delBtn.type = "button";
  delBtn.style.display = "none";
  delBtn.setAttribute("onclick","removeTag(this)");

  hidden.parentNode.insertBefore(div,hidden);

  div.appendChild(field);
  div.appendChild(addBtn);
  div.appendChild(delBtn);

  element.nextElementSibling.style.display = "block";
  element.style.display = "none";

}

function removeTag(element) {
  element.parentElement.remove();
  hidden = document.getElementById("hiddenTag");
  hidden.value = parseInt(hidden.value) - 1;
}

function addLocation(element) {
  hidden = document.getElementById("hiddenLocation");
  
  var options = document.getElementById("countries").options;
  var result = false;

  for(var i=0;i<options.length;++i){
      if(element.previousElementSibling.value === options[i].value) {
          result = true;
          break;
      }
  }

  if(!result)
      return false;

  hidden.value = parseInt(hidden.value) + 1;

  let div = document.createElement("div");

  let div1 = document.createElement("div");
  div1.classList.add("field-group")
  div1.style.float = "left";
  div1.style.width = "40%";
  div1.style.marginRight = "1em";

  let div2 = document.createElement("div");
  div2.classList.add("field-group")
  div2.style.float = "left";
  div2.style.width = "28.5%";
  div2.style.marginRight = "1em";

  let div3 = document.createElement("div");
  div3.classList.add("field-group")
  div3.style.float = "left";
  div3.style.width = "28.5%";

  let field1 = document.createElement("input");
  field1.setAttribute("list","locations");
  field1.classList.add("text-field");
  field1.placeholder = "Add the location";
  field1.required = true;
  field1.setAttribute("oninput","notInvalid(this)");

  let field2 = document.createElement("input");
  field2.setAttribute("list","regions");
  field2.classList.add("text-field");
  field2.placeholder = "Add the region";
  field2.required = true;
  field2.setAttribute("oninput","notInvalid(this)");

  let field3 = document.createElement("input");
  field3.setAttribute("list","countries");
  field3.classList.add("text-field");
  field3.placeholder = "Add the country";
  field3.required = true;
  field3.setAttribute("oninput","notInvalid(this)");

  let addBtn = document.createElement("button");
  addBtn.innerHTML = "Add";
  addBtn.classList.add("button-submit");
  addBtn.type = "button";
  addBtn.setAttribute("onclick","addLocation(this)");

  let delBtn = document.createElement("button");
  delBtn.innerHTML = "Remove";
  delBtn.classList.add("button-delete");
  delBtn.type = "button";
  delBtn.style.display = "none";
  delBtn.setAttribute("onclick","removeLocation(this)");

  hidden.parentNode.insertBefore(div,hidden);

  div1.appendChild(field1)

  div2.appendChild(field2);

  div3.appendChild(field3);
  div3.appendChild(addBtn);
  div3.appendChild(delBtn);

  div.appendChild(div1);
  div.appendChild(div2);
  div.appendChild(div3);

  element.nextElementSibling.style.display = "block";
  element.style.display = "none";

}

function removeLocation(element) {
  hidden = document.getElementById("hiddenLocation");
  hidden.value = parseInt(hidden.value) - 1;
  element.parentElement.parentElement.remove();
}

function fixCountries() {
    var countries = document.getElementById('countries-form').getElementsByTagName('input');
    let numCountries = parseInt(document.getElementById('hiddenCountry').value);
    let inputs = document.getElementById('countryInputs');
    for(var i=0;i<numCountries;++i)
        inputs.value = inputs.value + countries[i].value + ";";
}

function fixLocations() {
    var locations = document.getElementById('locations-form').getElementsByTagName('input');
    let numLocations = parseInt(document.getElementById('hiddenLocation').value)/3;
    let inputs = document.getElementById('locationInputs');
    for(var i=0;i<numLocations;++i)
        inputs.value = inputs.value + locations[i*3].value + "#" + locations[i*3+1].value + "#" + locations[i*3+2].value + ";";
}

function fixTags() {
    var tags = document.getElementById('tags-form').getElementsByTagName('input');
    let numTags = parseInt(document.getElementById('hiddenTag').value);
    let inputs = document.getElementById('tagInputs');
    for(var i=0;i<numTags;++i){
        inputs.value = inputs.value + tags[i].value + ";";
    }
}

function fixInput() {
    fixCountries();
    fixLocations();
    fixTags();
}


