$(document).ready(function()
{
    $('#role').val(interviewer_role);

    if(is_active == 'True')
    {
        $('#is_active_checkbox').prop('checked', true);
        $("#hidden_is_active").val('True');
    }
    else
    {
        $('#is_active_checkbox').prop('checked', false);
        $("#hidden_is_active").val('False');
    }

    $("#is_active_checkbox").change( function()
    {
          if ( $(this).is(":checked") )
          {
            $("#hidden_is_active").val('True');
          }
          else
          {
             $("#hidden_is_active").val('False');
          }
    });

});