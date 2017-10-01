$(document).ready(function()
{
    $('#jobSelect').on('change', function ()
    {
        var selectedQuestionId = $("option:selected").val();
        var selectedText = $("option:selected").text();
        $("option:selected").remove();

        $('#selectedQuestionDiv').append('<div class="selectedQuestion">' +
            '<li class="list-group-item">'+selectedText+' <span class="badge">' +
            '<i class="fa fa-trash-o" aria-hidden="true"></i></span></li>' +
            '<input type="hidden" name="question_id" class="question_id" value="'+selectedQuestionId+'">' +
            '</div>');
        $("#jobSelect").prop('selectedIndex',0);
    });

    $('#selectedQuestionDiv').on('click', 'li', function()
    {
        $(this).parent().remove();
        var selectedText = $(this).text();
        var selectedQuestionId = $(this).siblings('.question_id').val();

        $('#jobSelect').append('<option value="'+selectedQuestionId+'">'+selectedText+'</option>');
    });
});