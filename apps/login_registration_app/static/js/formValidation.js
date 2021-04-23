console.log("We're using JQuery!");


$(document).ready(function() {
    $('#form1').submit(function(){
        let first_name = $('#first_name-id').val();
        if (first_name === "") {
            return false;
        }
        if (first_name.length < 2 ) {
            alert('First Name should be at least 2 characters!');
        }
        let last_name = $('#last_name-id').val();
        if (last_name === "") {
            return false;
        }
        if (last_name.length < 2 ) {
            alert('Last Name should be at least 2 characters!');
            return false;
        }
        let password = $('#password-id').val();
        if (password.length <= 8 ) {
            alert('Password should be at least 8 character!');
            return false;
        }
        // let password_login = $('#password-id2').val();
        // if (password_login.length <= 8 ) {
        //     alert('Password might be at least 8 character!');
        //     return false;
        // }

        // alert('¡El usuario fue registrado!');
    });


    //$('#email-id').blur(...arguments) // Este es para una lista
    $('#email-id').focusout(function(){
        verificarEmail();
        validateForm();
    })

});

function validateForm() {
    var email = $('#email-id').val();
    if(email === "") {
     return false;
    }
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
   }

function verificarEmail() {
    //let data = $(this).serialize();
    let data = $('#form1').serialize();
    console.log(data);
    $.ajax({
        type: "POST",
        url: '/verificar_email/',
        data: data
    })
    .done(function(respuesta) {
        alert(respuesta.errors);
        console.log('Success!');
    })
    .fail(function() {
        alert("Error!");
    })
    .always(function() {
        alert("Complete!");
    });
}
