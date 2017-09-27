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

function configure_editor(selected_language)
{
    var language = selected_language.val()
    var editor = ace.edit("editor");

    if(language == 'java')
        editor.setValue('public class hello {\n' +
            '    public static void main(String []args) {\n' +
            '        System.out.println("Hello World");\n' +
            '    }\n' +
            '}')

    else if(language == 'python')
        editor.setValue('print("Hello World")');

    else if(language == 'javascript')
        editor.setValue('console.log("Hello World");');

    else if(language == 'php')
        editor.setValue('echo "Hello world!";');

    else if(language == 'c_cpp')
        editor.setValue('#include <iostream.h>\n' +
            'main()\n' +
            '{\n' +
            '    cout << "Hello World!";\n' +
            '    return 0;\n' +
            '}');

    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/" + language);
}