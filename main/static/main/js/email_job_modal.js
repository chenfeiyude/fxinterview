$(document).ready(function()
{
    $('[data-toggle="modal"]').on('click', function()
    {
        var job_id = $(this).parent().children('input').val();
         $(' #email_job_id').val(job_id);
    });
});