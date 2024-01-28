$(document).ready(function() {
    let messageContent = $('.alert').text();
    
    if(messageContent.includes("Tails")) {
        $('#coin').addClass('tails-still');
    }
    else if (messageContent.includes("Heads")){
        $('#coin').removeClass();
    }
    else {
        $('#coin').removeClass();
    }
    
});

function submitForm(option) {
    $('#' + option).prop('checked', true);
    console.log(option);

    $('#coin').removeClass();

    if (option == "id_bet_side_0") {
        console.log("heads");
        $('#coin').addClass('tails');
    } else {
        $('#coin').addClass('heads');
    }
 // 3000ms timeout

    setTimeout(function () {
        $('#coinFlipForm').submit();
    }, 3000);
}

