document.addEventListener('DOMContentLoaded', function() {
    // Existing functionality to scroll to the bottom
    scrollToBottom();
    if(document.getElementById('responsePagequestionForm')){
        // New functionality for handling form submission
        var form = document.getElementById('responsePagequestionForm');
        var progressBar = document.querySelector('.progress-bar');

        form.addEventListener('submit', function(event) {
            var question = document.getElementById('myInputText').value.trim();

            // Check if the question is empty
            if (!question) {
                // Show an alert if the question is empty
                alert('Please enter a question.');
                event.preventDefault(); // Prevent form submission
            } else {
                // Show the progress bar
                progressBar.style.display = 'block';
            }
        });
        // Get the textarea element
        var textarea = document.getElementById('myInputText');

        // Add an event listener to resize the textarea on input
        textarea.addEventListener('input', function() {
            autoResize(this); // 'this' refers to the textarea
        });
    }
});

function autoResize(textarea) {
    textarea.style.height = "auto"; // Reset height to auto
    textarea.style.height = textarea.scrollHeight + "px"; // Set height based on scrollHeight
}

// Function to scroll to the end of the content inside a div
function scrollToBottom() {
    var container = document.getElementById("response-view-container");
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

// Add any additional event listeners or functionality you need here
// For example, for 'touchstart'
document.addEventListener('touchstart', function(evt) {
    // ... any touchstart-specific code here ...
}, { passive: true });
