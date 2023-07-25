function validateForm(event) {
    var checkbox = document.getElementById("myCheckbox");
    event.preventDefault();
    if (!checkbox.checked) {
        alert("Please select the checkbox.");
        return false; // Prevent form submission
    }
    // Show the progress bars
    var progressBars = document.querySelectorAll(".progress-bar");
    progressBars.forEach(function(progressBar) {
        progressBar.style.display = "block";
    });

    // Disable the submit button
    var submitButton = document.querySelector(".btn-primary");
    submitButton.disabled = true;

    // Allow the form submission after a short delay
    setTimeout(function() {
        document.getElementById("myForm").submit();
    }, 500); // Adjust the delay as needed

}

document.getElementById("myForm").addEventListener("submit", validateForm);
