$(document).ready(function()
{
    $('[data-toggle="modal"]').on('click', function()
    {
        var job_id = $(this).parent().children('input').val();
        $('#interviewee_email_input').val('');
        $(' #email_job_id').val(job_id);
        $(' #datepicker').val('');
    });

    $( "#datepicker" ).datepicker({
        dateFormat: 'yy-mm-dd',
        minDate: 0
    });

    $("#send_btn").click(function()
    {
        $( "#job_invitation_form" ).submit();
    });

    $('#job_invitation_form').submit(function (e)
    {
        var interviewee_email = $('#interviewee_email_input').val();
        var estimated_time = $('#eta_input').val();

        if(interviewee_email == '')
        {
            alert("Please type in interviewee email");
            e.preventDefault();
            return;
        }

        if(!isValidEmailAddress(interviewee_email))
        {
             alert("Please type in a valid email address");
             e.preventDefault();
             return;
        }
    });

    function isValidEmailAddress(emailAddress)
    {
        var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
        return pattern.test(emailAddress);
    };
});