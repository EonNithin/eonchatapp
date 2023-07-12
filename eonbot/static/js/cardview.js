// Get the card body element
//var cardBody = document.getElementById('cardBody');
// Scroll the card body to the bottom
//cardBody.scrollTop = cardBody.scrollHeight;

// Scroll to the bottom of the card body
function scrollToBottom() {
  const cardBody = document.getElementById("cardBody");
  if (cardBody) {
    cardBody.scrollTop = cardBody.scrollHeight;
  }
}

// Call scrollToBottom() when the DOM content is loaded
document.addEventListener("DOMContentLoaded", function() {
  scrollToBottom();
});


