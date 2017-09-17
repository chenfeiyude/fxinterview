$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();

    var selected_language = $("#selected_language");
    configure_editor(selected_language);

    $( "#test_code_form" ).submit(function( event ) {
        var editor = ace.edit("editor");
        var answer_content = $("#answer_content");
        answer_content.val(editor.getValue());
    });

    $("#selected_language").change(function(){
        configure_editor($(this));
    });
});

function configure_editor(selected_language) {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/" + selected_language.val());
}