// newEntry.html
document.addEventListener(`DOMContentLoaded`, function(){

    //when submit button is clicked
    let submitButton = document.querySelector(`#newEntrySubmit`);
    submitButton.addEventListener(`click`, function(){
        submitButton.value = `thank you`;
    });
});

// navigation tab for all html pages
document.addEventListener('DOMContentLoaded', function(){
    $(document).ready(function() {
        $("#navTab").load("template.html .theNavbarCode");
    });
});