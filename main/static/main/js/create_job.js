$(document).ready(function()
{
    $('#jobSelect').on('change', function ()
    {
        var selectedQuestionId = $("option:selected").val();
        var selectedText = $("option:selected").text();
        $("option:selected").remove();

        $('#selectedQuestionDiv').append('<div>' +
            '<a href="">'+selectedText+'</a>' +
            '<input type="hidden" name="question_id" class="question_id" value="'+selectedQuestionId+'">' +
            '<input type="button" class="btn btn-danger" value="Remove" />' +
            '</div>');

        $("#jobSelect").prop('selectedIndex',0);
    });

    $('#selectedQuestionDiv').on('click', 'input.btn', function()
    {
        $(this).parent().remove();
        var selectedText = $(this).siblings('a').text();
        var selectedQuestionId = $(this).siblings('.question_id').val();
        $('#jobSelect').append('<option value="'+selectedQuestionId+'">'+selectedText+'</option>');
    });
});