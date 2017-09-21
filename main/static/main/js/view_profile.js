$(document).ready(function(){
    $( "#profile_form" ).submit(function(e) {
        var password = $("#id_password");
        var password2 = $("#id_password2");
        if(password.val() != password2.val()) {
            alert('Password confirmation does not match new password.');
            e.preventDefault(e);
        }
    });
});