document.getElementById("myForm").addEventListener("submit", function(event) {
    // Prevent form submission
    //event.preventDefault();

    // Show the progress bars
    var progressBars = document.querySelectorAll(".progress-bar");
    progressBars.forEach(function(progressBar) {
        progressBar.style.display = "block";
    });

    // Disable the submit button
    var submitButton = document.querySelector(".btn-primary");
    submitButton.disabled = true;

    // Simulate the loading delay (replace with your actual asynchronous request)
    setTimeout(function() {
        // Hide the progress bars
        progressBars.forEach(function(progressBar) {
           progressBar.style.display = "none";
        });

        // Enable the submit button
        submitButton.disabled = false;

        // Optional: Reset the form
        document.getElementById("myForm").reset();
    }, 5000); // Adjust the timeout value or replace with your actual request
});