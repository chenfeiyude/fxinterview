$(document).ready(function(){
    configure_editor();

    $( "#application_question_form" ).submit(function( event ) {
        var editor = ace.edit("editor");
        var answer_content = $("#answer_content");
        answer_content.val(editor.getValue());
    });
});


function configure_editor() {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/javascript");
}