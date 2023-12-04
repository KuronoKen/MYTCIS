// Function to get the value of a cookie by name
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}
  
function getUsernameFromToken(token) {
    try {
        const decodedToken = JSON.parse(atob(token.split('.')[1]));
        return decodedToken.username;
    } catch (error) {
        console.error('Error decoding token:', error);
        return null;
    }
}

//Redirect Function

function DirectToSearch(){
  location.href = ("Search.html")
}

function Home(){
location.href = ("Index.html")
}

function DirectToContactUs() {
location.href = ("Contact Us.html")
}
function DirectToAdd() {
location.href = ("Add.html")
}


//Form Function

const allergyData = [];
const drugData = [];
var selecting = "";


function formatPhoneNumber() {
    let phoneNumberInput = document.getElementById('phone');
    let phoneNumber = phoneNumberInput.value.replace(/\D/g, ''); // Remove non-numeric characters
  
    // Check if the phone number is not empty
    if (phoneNumber.length > 0) {
      // Add hyphens based on the length of the phone number
      if (phoneNumber.length >= 3 && phoneNumber.length <= 6) {
        phoneNumber = phoneNumber.slice(0, 3) + '-' + phoneNumber.slice(3);
      } else if (phoneNumber.length >= 7) {
        phoneNumber = phoneNumber.slice(0, 3) + '-' + phoneNumber.slice(3, 6) + '-' + phoneNumber.slice(6);
      }
  
      // Update the input field with the formatted phone number
      phoneNumberInput.value = phoneNumber;
    }
}
  
  
function formatID() {
    var formattedValue = '';
    var value = document.getElementById("socialid").value.replace(/\D/g, '');
    for (var i = 0; i < value.length; i++) {
      if (i === 1 || i === 5 || i === 10 || i === 12) {
        formattedValue += '-';
      }
      formattedValue += value[i];
    }
    return document.getElementById("socialid").value=formattedValue;
}
  
function PutNewList(inputelement,inputvalue){
  const newlist = document.createElement("li");
  const node = document.createTextNode(inputvalue);
  newlist.className = "List"
    
  if (inputelement.name == "foodallergy") {
    newlist.onclick = function() {
      showInfo(inputvalue,"food");
    };
    newlist.appendChild(node);
    allergyData.push({
      name: newlist.textContent,
      allergysymptoms: []
    });
    const target = document.getElementById("allergylist");
    target.appendChild(newlist);
  }else if (inputelement.name == "drugallergy") {
      newlist.onclick = function() {
        showInfo(inputvalue,"drug");
      };
      newlist.appendChild(node);
      drugData.push({
        name: newlist.textContent,
        allergysymptoms: []
      });
      const target = document.getElementById("druglist");
      target.appendChild(newlist);
  }else if (inputelement.name == "symptoms") {
    newlist.appendChild(node);
    
    const target = document.getElementById("symptomslist");
    target.appendChild(newlist);
    savesymptoms(inputvalue)
  }    
}

function loadlist(symptom){
  const newlist = document.createElement("li");
  const node = document.createTextNode(symptom);
  newlist.className = "List"
  newlist.appendChild(node);
  const target = document.getElementById("symptomslist");
  target.appendChild(newlist);
}


function showInfo(cause,group) {
  selecting = group;
  var symptomsEditor = document.getElementById("Editor");
  document.getElementById("HeadLine").innerHTML = cause;
  document.getElementById("symptoms").value = "";
  symptomsEditor.style.display = "block";
  loadsymptoms()
 
}

function savesymptoms(symptoms){
  var selectedAllergy = document.getElementById("HeadLine").textContent;
  
        // Find the corresponding allergy in the temporary array
        var selectedAllergyData = ""
        if (selecting == "food"){
          selectedAllergyData = allergyData.find(item => item.name === selectedAllergy);
          console.log("Allergy data:", allergyData);
        }else if(selecting =="drug"){
          selectedAllergyData = drugData.find(item => item.name === selectedAllergy);
          console.log("Drug Allergy data:", drugData);
        }

        // Update the notes in the temporary array
        if (selectedAllergyData) {
            selectedAllergyData.allergysymptoms.push(symptoms)
        }
        
        // Log the allergyData array to the console
        

}


function loadsymptoms(){
  var selectedAllergy = document.getElementById("HeadLine").textContent;
  var selectedAllergyData = ""
  if (selecting == "food"){
    selectedAllergyData = allergyData.find(item => item.name === selectedAllergy);
  }else if(selecting =="drug"){
    selectedAllergyData = drugData.find(item => item.name === selectedAllergy);
  }
  
  var list = document.getElementById("symptomslist")
  list.innerHTML = ""
  if (selectedAllergyData){
    for (symptom of selectedAllergyData.allergysymptoms){
      loadlist(symptom)
    }
  }
 
}


function closeeditor(){
  
  document.getElementById("Editor").style.display = "none";
}
  

// Get the input field
var symptomsInput = document.getElementById("symptoms");


symptomsInput.addEventListener("keypress", function(event) {
      // If the user presses the "Enter" key on the keyboard
      if (event.key === "Enter" && symptomsInput.value.trim() !== "") {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        PutNewList(symptomsInput,symptomsInput.value)
        symptomsInput.value = "";
      }
});

var allergyInput = document.getElementById("foodallergy");
  

allergyInput.addEventListener("keypress", function(event) {
      // If the user presses the "Enter" key on the keyboard
      if (event.key === "Enter" && allergyInput.value.trim() !== "") {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        PutNewList(allergyInput,allergyInput.value)
        allergyInput.value = "";
      }
});


var drugInput = document.getElementById("drugallergy");
  

drugInput.addEventListener("keypress", function(event) {
      // If the user presses the "Enter" key on the keyboard
      if (event.key === "Enter" && drugInput.value.trim() !== "") {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        PutNewList(drugInput,drugInput.value)
        drugInput.value = "";
      }
});


document.getElementById("TheFormInstance").addEventListener("submit", function(event){
  event.preventDefault()
  SaveNewPatience()
});



function SaveNewPatience(){
  patientname = document.getElementById("name").value
  patientsurname = document.getElementById("surname").value
  Sex = document.getElementById("sex").value
  birthday = document.getElementById("birthday").value
  Email = document.getElementById("email").value
  phonenumber = document.getElementById("phone").value.replace(/[^0-9]/g, "");
  socialid = document.getElementById("socialid").value.replace(/[^0-9]/g, "");

  fetch('http://127.0.0.1:5000/registerpatient', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        patient_name: patientname,
        patient_surname: patientsurname,
        sex: Sex,
        date_of_birth: birthday,
        email: Email,
        phone_number: phonenumber,
        social_id: socialid,
        food_allergies: allergyData,
        drug_allergies: drugData,
    }),
})
    .then(response => response.json())
    .then(data => {
        alert('New Patience Saved.')
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}