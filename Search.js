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

function checkUserSearch() {
    const token = getCookie('token');
    var readusername = getUsernameFromToken(token);
    if (readusername) {
        username = readusername;
    }
    if (token) {
        document.getElementById("Username").innerHTML = "User : "+username
    } else {
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
//EEEEEEE
function formatID() {
    var formattedValue = '';
    var value = document.getElementById("ID").value.replace(/\D/g, '');
    for (var i = 0; i < value.length; i++) {
      if (i === 1 || i === 5 || i === 10 || i === 12) {
        formattedValue += '-';
      }
      formattedValue += value[i];
    }
    return document.getElementById("ID").value=formattedValue;
}

document.getElementById("SearchForm").addEventListener("submit", function(event){
    event.preventDefault()
    console.log('4')
    location.href = ("Information.html?Id="+document.getElementById("ID").value.replace(/\D/g, ''))
});