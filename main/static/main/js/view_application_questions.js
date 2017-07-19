$(document).ready(function(){
    configure_editor();

    $( "#application_question_form" ).submit(function( event ) {
        var editor = ace.edit("editor");
        var answer_content = $("#answer_content");
        answer_content.val(editor.getValue());
    });

    count_down_time();
});

function configure_editor() {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/javascript");
}

function count_down_time(estimated_end_time) {
    var estimated_end_time = $("#estimated_end_time").val();

    // Set the date we're counting down to
    var countDownDate = new Date(estimated_end_time).getTime();

    // Update the count down every 1 second
    var x = setInterval(function() {
        // Get todays date and time
        var now = new Date().getTime();

        // Find the distance between now an the count down date
        var distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the result in the element with id="demo"
        $("#timer").html(days + "d " + hours + "h " + minutes + "m " + seconds + "s ");

        // If the count down is finished, write some text
        if (distance < 0) {
            clearInterval(x);
            $("#timer").html("EXPIRED");
        }
    }, 1000);
}