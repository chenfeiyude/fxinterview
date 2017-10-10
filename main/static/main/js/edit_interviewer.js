$(document).ready(function()
{
    $('#role').val(interviewer_role);

    if(is_active == 'True'){
        $('#is_active').prop('checked', true);
    }

    $("#is_active").change( function()
    {
          if ( $(this).is(":checked") )
          {
            $("#hidden_is_active").prop('disabled', true);
          }
          else if ( $(this).not(":checked") )
          {
            $("#hidden_is_active").prop('disabled', false);
          }
    });

});