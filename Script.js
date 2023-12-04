var username = "Guest"
var password = ""




function ConfirmedLoggedIn() {
    console.log("Username: " + username + ", Password: " + password);
    var Div = document.getElementById('Greeting');
    Div.style.display = "flex";
    var Logo = document.getElementById('logo');
    Logo.style.top = "0%";
    document.getElementById("Greet").innerHTML = "Greeting, " + username+ ".";
    document.getElementById("LoginContainer").remove();
}
function checkUserStatus() {
  const token = getCookie('token');
  var readusername = getUsernameFromToken(token);
  if (readusername) {
      username = readusername;
  }
  if (token) {
      ConfirmedLoggedIn();
  } else {
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

function login() {
    event.preventDefault();
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;
    // Send a request to the server
    fetch('http://127.0.0.1:5000/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      })
      .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
      if (data.success) {
          // Store the token securely (e.g., in a cookie)
          console.log('Token value:', data.token);
          document.cookie = `token=${data.token}; path=/`;
          console.log('Cookie set:', document.cookie);
          // alert('Sign-in successful');
          checkUserStatus()
          ConfirmedLoggedIn();
          
      } else {
          alert('Sign-in failed');
      }
  })
  .catch(error => {
      console.error('Error:', error);
      // alert('Failed to fetch. Check the console for details.');
  });;
    
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