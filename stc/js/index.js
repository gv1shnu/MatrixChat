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