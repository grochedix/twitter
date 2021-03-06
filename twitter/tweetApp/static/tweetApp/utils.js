

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

const django_ajax_headers = {
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFToken': csrftoken
}

let registerForm = document.getElementById("registerForm");

registerForm.addEventListener("submit", async function(event) {
        event.preventDefault();
        if (document.getElementById("registerError") !== null) {
            document.getElementById("registerError").remove();
        }
        let data = {
            "username":document.getElementById("id_username").value,
            "email":document.getElementById("id_email").value,
            "password1":document.getElementById("password1").value,
            "password2":document.getElementById("password2").value,
        }
        await fetch('/register/', {
                method: 'post',
                mode: 'same-origin',
                headers: django_ajax_headers,
                body: JSON.stringify(data),
            }
        ).then(function(response) {
            return response.json();
          }).then(function(data) {
            if (data.error === 'None') {
                window.location.replace('/home/?success_registration=t');
                return;
            } else {
                document.getElementById("register_body").insertAdjacentHTML('beforeend', '<div id="registerError"></div>');
                for (var property in data) {
                    if (data.hasOwnProperty(property)) {
                        for (var property2 in data[property]) {
                            if (data[property].hasOwnProperty(property2)) {
                                for (let i=0 ; i<data[property][property2].length ; i++) {
                                    document.getElementById("registerError").insertAdjacentHTML('beforeend', `<p style="color:red"><em>${data[property][property2][i]}</em></p>` );
                                }
                                 }
                        }}
                  }
            }
          });
    }
)

let loginForm = document.getElementById("loginForm");

loginForm.addEventListener('submit', async event => {
    event.preventDefault();
    if (document.getElementById("loginError") !== null) {
        document.getElementById("loginError").remove();
    }
    data = {
        'username':document.getElementById('login_username').value,
        'password':document.getElementById('login_password').value,
    }
    await fetch('/login/', {
            method: 'post',
            mode: 'same-origin',
            headers: django_ajax_headers,
            body: JSON.stringify(data),
        }
    ).then(function(response) {
        return response.json();
    }).then(function(data) {
    if (data.error === 'None') {
        let urlParams = new URLSearchParams(window.location.search);
        let next = urlParams.get('next');
        if (next !== null) {
            window.location.replace(next);
            return
        }
        window.location.replace('/home/');
        return;
    } else {
        document.getElementById("login_body").insertAdjacentHTML('beforeend', '<div id="loginError"></div>');
        document.getElementById("loginError").insertAdjacentHTML('beforeend', `<p style="color:red"><em>${data["error"]}</em></p>` );                               
    }
})
})

