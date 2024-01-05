
document.addEventListener('DOMContentLoaded', (event) => {
    scrollToBottom();
});

// Function to scroll to the end of the content inside a div
function scrollToBottom() {
    var container = document.getElementById("response-view-container");
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

// Add event listener for 'touchstart', if there's more functionality you need to add
// This example function doesn't do anything, it's for illustrative purposes
document.addEventListener('touchstart', function(evt) {
    // ... any touchstart-specific code here ...
}, { passive: true });  // Mark the event listener as passive

