$(document).ready(function(){
    configure_editor();

});


function configure_editor() {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/javascript");
}