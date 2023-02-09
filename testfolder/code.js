// newEntry.html
document.addEventListener(`DOMContentLoaded`, function(){

    //when submit button is clicked
    let submitButton = document.querySelector(`#newEntrySubmit`);
    submitButton.addEventListener(`click`, function(){
        submitButton.value = `thank you`;
    });
});