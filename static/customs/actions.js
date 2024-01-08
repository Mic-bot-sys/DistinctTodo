

function authentication(event){
    event.preventDefault();
    
    const token =  $('input[name="csrfmiddlewaretoken"]').attr('value'); 
    const email = document.querySelector("#email").value;
    const password = document.querySelector("#password").value;

    const btn = document.querySelector("#loginBtn");
    btn.disabled = true
    btn.classList.add("button--loading");

    let obj = {
        email: email, 
        password:  password,
    }

    $.ajax({
        type: 'POST',
        url: '/',
        dataType: 'json',
        data: JSON.stringify(obj),
        headers: {
            'X-CSRFToken': token 
       },
        success: function (result) {
            result.status === '200' 
            ?
            window.location.href = '/home'
            :
            Swal.fire({
                position: "center",
                icon: "error",
                title: "Invalid Credentials!!!",
                text: `The Credentials you have entered is not valid`,
                timer: 2500
              });
            btn.classList.remove("button--loading");
            btn.disabled = false
        },
        error: function(error){
            console.log(error)
        }
    })
    // window.location.href = 'https://www.facebook.com'
}


function registration(event){
    event.preventDefault();

    const btn = document.querySelector("#registerBtn");
    btn.disabled = true
    btn.classList.add("button--loading");
    
    const token =  $('input[name="csrfmiddlewaretoken"]').attr('value'); 
    const email = document.querySelector("#regEmail").value;
    const password = document.querySelector("#regPassword").value;
    const confirmPassword = document.querySelector("#confirmPassword").value;

    if (password !== confirmPassword){
        btn.disabled = false
        btn.classList.remove("button--loading");
        return Swal.fire({
            position: "center",
            icon: "error",
            title: "Password Mismatch!!!",
            text: `Password and Confirm Password does not match`,
            showConfirmButton: false,
            timer: 2500
          });
    }


    let obj = {
        email: email, 
        password:  password,
    }

    $.ajax({
        type: 'POST',
        url: '/register',
        dataType: 'json',
        data: JSON.stringify(obj),
        headers: {
            'X-CSRFToken': token 
       },
        success: function (result) {
            Swal.fire({
                position: "center",
                icon: "success",
                title: "Account Created Successfully!!!",
                text: `Your account has been created Successfully. Kindly Login to access your Dashboard`,
                showConfirmButton: true,
              });

            btn.classList.remove("button--loading");
            btn.disabled = false

            // Clear all the initial Values
            $('#email').val('')
            $('#password').val('')
            $('#confirmPassword').val('')
            // End Clearing the Values

            // This is to navigate to the Login Tab
            $('#nav-login-tab').tab('show')
            // End navigation to the Login Tab
        },
        error: function(error){
            console.log(error)
        }
    })
    // window.location.href = 'https://www.facebook.com'
}


function GetForgotPasswordPartial(){
    $('#authContentId').hide()
    $('#forgotPasswordId').show()
}

function GetAuthenticationSectionPartials(){
    $('#forgotPasswordId').hide()
    $('#authContentId').show()
}