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
});