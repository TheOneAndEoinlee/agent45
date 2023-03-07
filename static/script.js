$(document).ready(function() {
	
	var chatWindow = document.getElementById("chat-window");
	chatWindow.scrollTop = chatWindow.scrollHeight;
	
	    
    function sendInput() {
		var inputBox = $('#input-box');
		var input = inputBox.val().trim(); // Remove leading/trailing whitespace

		if (input.length === 0) {
			// Input is empty, do nothing
			return;
		}
		$('#chat-window').prepend('<div class="message sent">' + input.replace(/\n/g, '<br>') + '</div>');
		// Send input to server using AJAX
        $.ajax({
            url: '/process_input',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({input: input}),
            success: function(response) {
                console.log(response);
				
				$('#chat-window').prepend('<div class="message received">' + response.reply.replace(/\n/g, '<br>') + '</div>');
				$('#chat-window').animate({scrollTop: $('#chat-window').prop('scrollHeight')}); // Auto-scroll to bottom
            }
        });

        // Clear input box
        $('#input-box').val('');
    }
	
    // Listen for "Enter" key press on input box
	$('#input-box').on('keydown', function(event) {
    if (event.keyCode == 13) {
        event.preventDefault(); // Prevent default behavior of enter key
    }
});
    $('#input-box').on('keyup', function(event) {
        if (event.keyCode == 13 && !event.shiftKey) {
            event.preventDefault();
			sendInput();
			$('#input-box').val('');
        }
		else if (event.keyCode == 13 && event.shiftKey) {
            // Add newline character to input value
			var inputBox = $(this);
            inputBox.val(inputBox.val() + '\n');

            // Prevent default action of the "Enter" key press
            event.preventDefault();
		}
    });

    // Listen for "Send" button click
    $('#send-button').on('click', function(event) {
        sendInput();
    });
	
	var chatWindow = $('#chat-window');
    // Load existing messages
	  $.ajax({
		url: '/get_all_messages',
		type: 'GET',
		success: function(messages) {
		  // Iterate through each message and prepend it to the chat window
			for (var i = messages.length - 1; i >= 0; i--) {
			var messageClass = messages[i][2] === 'user' ? 'sent' : 'received';
			$('#chat-window').append('<div class="message ' + messageClass + '">' + messages[i][1] + '</div>');
			}
		}
	  });
    
	
	});
	