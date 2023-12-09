var textInput = document.getElementById('msg');

$(function () {
    $("#msg").on("input", function () {
        var inputValue = $(this).val();
        // Check if the '@' symbol is present in the input
        if (inputValue.includes('@')) {
            $(this).autocomplete({
                source: function (request, response) {
                    $.ajax({
                        url: "/get_users",
                        dataType: "json",
                        data: { term: request.term },
                        success: function (data) {
                            response(data);
                        }
                    });
                },
                minLength: 2
            });
        }
    });
});

// Prevent clicks on the document from removing focus
document.addEventListener('click', function(event) {
  if (event.target !== textInput) {
    textInput.focus();
  }
});

function saveMessage() {
    var inputMessage = document.getElementById('msg').value;
    if (inputMessage === "logout") {
        localStorage.clear();
    }
    else if(inputMessage === "to?") {
        alert("Current recipient is: "+ currentRecipient);
    }
    else {
        var messages = JSON.parse(localStorage.getItem('storedMessages')) || [];
        messages.push(inputMessage);
        localStorage.setItem('storedMessages', JSON.stringify(messages));
        displayMessages();
    }
}

function displayMessages() {
    var messages = JSON.parse(localStorage.getItem('storedMessages')) || [];
    var messageListDiv = document.getElementById('messageList');
    messageListDiv.innerHTML = '<table>' + messages.map(
        message => '<tr><td><p>'+
        currentUser + '> </p></td><td><p>@'+
         currentRecipient + '</p></td><td><p> '
         + message + '</p></td></tr>'
        ).join('') + '</table>';
}

displayMessages();