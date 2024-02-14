
document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById("myForm");
    if (form) {
        form.addEventListener("submit", validateForm);
    }
});

function autoResize(textarea) {
    textarea.style.height = "auto"; // Reset height to auto
    textarea.style.height = textarea.scrollHeight + "px"; // Set height based on scrollHeight
}

function validateForm(event) {
    var textarea = document.getElementById("myInputText");
    var checkbox = document.getElementById("myCheckbox");
    
    // Trim the value to handle cases where only spaces are entered
    var textValue = textarea.value.trim();

    if (textValue === "") {
        // If the textarea is empty, prevent form submission and alert the user
        alert("Please ask a question related to selected topic in the text field.");
        event.preventDefault(); // Prevent form submission
    }
    else if (!checkbox.checked) {
        alert("Please select the checkbox.");
        event.preventDefault(); // Prevent form submission
    }
    else {
        // Show the progress bars
        var progressBars = document.querySelectorAll(".progress-bar");
        progressBars.forEach(function (progressBar) {
            progressBar.style.display = "block";
        });
        // Disable the submit button
        var submitButton = document.getElementById("btn btn-primary");
        submitButton.disabled = true;
    }
}

function submitForm(){
    // Show the progress bars
    var progressBars = document.querySelectorAll(".progress-bar");
    progressBars.forEach(function (progressBar) {
        progressBar.style.display = "block";
    });

    // Disable the submit button
    var submitButton = document.getElementById("btn btn-primary");
    submitButton.disabled = true;

    // Prevent the default form submission behavior
    event.preventDefault();

    // Simulate a delay to show the progress bars
    setTimeout(function(){
        // Once the progress is shown, submit the form
        document.getElementById("myForm").submit();
    }, 500); // Adjust the delay as needed
}