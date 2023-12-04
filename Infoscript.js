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

getCookie()

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

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}
function calculateAge(birthdate) {
    var today = new Date();
    var birthDate = new Date(birthdate);
  
    var age = today.getFullYear() - birthDate.getFullYear();
    
    // Check if the birthday hasn't occurred yet this year
    if (
      today.getMonth() < birthDate.getMonth() ||
      (today.getMonth() === birthDate.getMonth() && today.getDate() < birthDate.getDate())
    ) {
      age--;
    }
  
    return age;
}

function formatID(Input) {
    var formattedValue = '';
    var value = Input.replace(/\D/g, '');
    for (var i = 0; i < value.length; i++) {
      if (i === 1 || i === 5 || i === 10 || i === 12) {
        formattedValue += '-';
      }
      formattedValue += value[i];
    }
    return formattedValue;
}

function formatPhoneNumber(phoneNumberInput) {
    let phoneNumber = phoneNumberInput.replace(/\D/g, ''); // Remove non-numeric characters
  
    // Check if the phone number is not empty
    if (phoneNumber.length > 0) {
      // Add hyphens based on the length of the phone number
      if (phoneNumber.length >= 3 && phoneNumber.length <= 6) {
        phoneNumber = phoneNumber.slice(0, 3) + '-' + phoneNumber.slice(3);
      } else if (phoneNumber.length >= 7) {
        phoneNumber = phoneNumber.slice(0, 3) + '-' + phoneNumber.slice(3, 6) + '-' + phoneNumber.slice(6);
      }
  
      // Update the input field with the formatted phone number
      return phoneNumber;
    }
}

var patientID = ""
function GetInfo(){
    Id = new URLSearchParams(window.location.search).get('Id')

    // Make a request to the Flask endpoint
    fetch(`http://127.0.0.1:5000/get_patient_allergies_and_symptoms/${Id}`)
        .then(response => response.json())
        .then(data => {
            // Access the data returned from the server
            const patientinfo = data.info;
            const foodAllergies = data.food_allergies;
            const drugAllergies = data.drug_allergies;
            patientID = patientinfo.patient_id
            LoadTimeline()
            // Use the data as needed
            console.log(patientinfo);
            console.log('Food Allergies:', foodAllergies);
            console.log('Drug Allergies:', drugAllergies);

            document.getElementById('patientName').textContent = 'Name: '+ patientinfo.first_name + ' ' + patientinfo.last_name
            document.getElementById('patientSex').textContent = 'Sex: ' + capitalizeFirstLetter(patientinfo.sex)
            document.getElementById('patientAge').textContent = 'Age: ' + calculateAge(patientinfo.date_of_birth)
            document.getElementById('patientDateOfBirth').textContent = 'Date Of Birth: ' + patientinfo.date_of_birth
            document.getElementById('patientEmail').textContent = 'Email: ' + patientinfo.email
            document.getElementById('patientPhoneNumber').textContent = 'Phone Number: ' + formatPhoneNumber(patientinfo.phone)
            document.getElementById('patientId').textContent = 'ID: ' + formatID(patientinfo.id_number)

            // Get the UL element by its ID
            const allergiesListElement = document.getElementById('foodallergy');

            // Iterate over the data and create list items
            for (const [allergy, symptoms] of Object.entries(foodAllergies)) {
                // Create a new list item
                const listItem = document.createElement('li');

                // Add the allergy name as text content
                listItem.textContent = allergy;

                // Create an inner UL for symptoms
                const symptomsList = document.createElement('ul');

                // Iterate over symptoms and create list items for each
                for (const symptom of symptoms) {
                    const symptomItem = document.createElement('li');
                    symptomItem.textContent = symptom;
                    symptomsList.appendChild(symptomItem);
                }

                // Append the inner UL to the main list item
                listItem.appendChild(symptomsList);

                // Append the list item to the main UL
                allergiesListElement.appendChild(listItem);
            }
            const drugallergiesListElement = document.getElementById('drugallergy');

            // Iterate over the data and create list items
            for (const [allergy, symptoms] of Object.entries(drugAllergies)) {
                // Create a new list item
                const listItem = document.createElement('li');

                // Add the allergy name as text content
                listItem.textContent = allergy;

                // Create an inner UL for symptoms
                const symptomsList = document.createElement('ul');

                // Iterate over symptoms and create list items for each
                for (const symptom of symptoms) {
                    const symptomItem = document.createElement('li');
                    symptomItem.textContent = symptom;
                    symptomsList.appendChild(symptomItem);
                }

                // Append the inner UL to the main list item
                listItem.appendChild(symptomsList);

                // Append the list item to the main UL
                drugallergiesListElement.appendChild(listItem);
            }
        })
        .catch(error => console.error('Error:', error));
}

function formatEventDate(dateString) {
  const date = new Date(dateString);

  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');

  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');

  return `${year}/${month}/${day} ${hours}:${minutes}`;
}

function ChangeDetail(data,eventId){
  document.getElementById("EventDetail").style.display = "block";
  const selectedEvent = data.events.find(event => event.event_id === eventId);
  document.getElementById("EventTitles").textContent = selectedEvent.event_title;
  document.getElementById("EventDates").textContent = formatEventDate(selectedEvent.event_date);
  document.getElementById("EventAppointment").textContent = formatEventDate(selectedEvent.appointment_date);
  document.getElementById("EventRecordTime").textContent = formatEventDate(selectedEvent.record_date);
  document.getElementById("EventCategorys").textContent = capitalizeFirstLetter(selectedEvent.category);
  document.getElementById("EventDescription").textContent = selectedEvent.description;
  document.getElementById("EventMedicine").textContent = selectedEvent.medicine_list;
}


function LoadTimeline(){
  fetch(`http://127.0.0.1:5000/get_patient_timeline/${patientID}`,{method : ["GET"],})
        .then(response => response.json())
        .then(data => {
            console.log(data)
            data.events.forEach(event => {
              // Create the EventSlot div
              const eventSlot = document.createElement('div');
              eventSlot.className = 'EventSlot';
              eventSlot.dataset.eventId = event.event_id

              eventSlot.onclick = function() {
                ChangeDetail(data,event.event_id);
              };
              // Create and set the EventDate element
              const eventDate = document.createElement('h2');
              eventDate.id = 'EventDate';
              eventDate.textContent = formatEventDate(event.event_date); // Assuming event_date is in a suitable format
              eventSlot.appendChild(eventDate);
              
  
              // Create and set the EventTitle element
              const eventTitle = document.createElement('h2');
              eventTitle.id = 'EventTitle';
              eventTitle.textContent = event.event_title;
              eventSlot.appendChild(eventTitle);
  
              // Create and set the EventCategory element
              const eventCategory = document.createElement('h2');
              eventCategory.id = 'EventCategory';
              eventCategory.textContent = capitalizeFirstLetter(event.category);
              eventSlot.appendChild(eventCategory);
  
              // Append the EventSlot to the container
              document.getElementById("TimelineContainer").appendChild(eventSlot);
          });
        })
        .catch(error => console.error('Error:', error));
}


function AddPageOn(){
  var symptomsEditor = document.getElementById("Editor");
  document.getElementById("title").value = "";
  symptomsEditor.style.display = "block";
}

function closeeditor(){
  
  document.getElementById("Editor").style.display = "none";
}

function closedetail(){
  
  document.getElementById("EventDetail").style.display = "none";
}

function CombineDateTime(date,time){
  // Extract date components
  const year = date.getFullYear();
  const month = date.getMonth();
  const day = date.getDate();

  // Extract time components
  const hours = time.getHours();
  const minutes = time.getMinutes();
  const seconds = time.getSeconds();

  // Create a new Date object with combined date and time
  const combinedDateTime = new Date(year, month, day, hours, minutes, seconds);

  return combinedDateTime
}

document.getElementById("addtimelineform").addEventListener("submit", function(event){
  event.preventDefault()
  console.log('triggered')
  savetimeline()
});



function savetimeline(){
  //patientID
  const apdate = new Date(document.getElementById("apdate").value);
  const aptime = new Date(`1970-01-01T${document.getElementById("aptime").value}`);

  const date = new Date(document.getElementById("date").value);
  const time = new Date(`1970-01-01T${document.getElementById("time").value}`);
  Category = document.getElementById("category").value
  EventTitle = document.getElementById("title").value
  Description = document.getElementById("description").value
  Medicine = document.getElementById("medicine").value
  console.log(document.getElementById("apdate").value)
  Appointment = CombineDateTime(apdate,aptime)
  TimeOfEvent = CombineDateTime(date,time)
  RecordDate = new Date()



  fetch('http://127.0.0.1:5000/registertimeline', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      patient_id: patientID,
      category: Category,
      event_title: EventTitle,
      description: Description,
      medicine_list: Medicine,
      appointment_date: Appointment,
      event_date: TimeOfEvent,
      record_date: RecordDate,
    }),
})
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}