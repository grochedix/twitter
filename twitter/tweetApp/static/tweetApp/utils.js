function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const csrftoken = getCookie('csrftoken');
let registerForm = document.getElementById("registerForm")

registerForm.addEventListener("submit", function(event) {
        event.preventDefault();
        let data = {
            "username":document.getElementById("id_username").value,
            "email":document.getElementById("id_email").value,
            "password1":document.getElementById("password1").value,
            "password2":document.getElementById("password2").value,
        }
        fetch('/register/', {
                method: 'post',
                'Accept': 'application/json',
                mode: 'same-origin',
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data),
            }
        ).then(function(response) {
            return response.json();
          }).then(function(data) {
            if (data.error === 'None') {
                window.location.replace('/home/')
            }
            console.log('Response:', data);
          });
    }
)