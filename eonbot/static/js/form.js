document.getElementById("selectOption").addEventListener("change", showHideFields);

document.getElementById("myForm").addEventListener("submit", validateForm);

function autoResize(textarea) {
    textarea.style.height = "auto"; // Reset height to auto
    textarea.style.height = textarea.scrollHeight + "px"; // Set height based on scrollHeight
}

function validateForm(event) {
    var textarea = document.getElementById("myInputText");
    var checkbox = document.getElementById("myCheckbox");
    var selectOption = document.getElementById("selectOption");
    var labActivityField = document.getElementById("labActivityField");
    
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
    else if (selectOption.value === "" ){
        alert("Please select a topic from dropdown.");
        event.preventDefault();// Prevent form submission
    }
    // Check the value of selectOption and set the required attribute accordingly
    else if (selectOption.value === 'lab activity') {
        labActivityField.required = true;
        if (labActivityField.value === "" ){
            alert("Please select an activity from list of activities.");
            event.preventDefault();// Prevent form submission
        }
    }
    else{
        // Show the progress bars
        var progressBars = document.querySelectorAll(".progress-bar");
        progressBars.forEach(function (progressBar) {
            progressBar.style.display = "block";
        });
        // Disable the submit button
        var submitButton = document.querySelector(".btn-primary");
        submitButton.disabled = true;
        // No need to manually submit the form if not preventing the default behavior
        // Form will submit normally
    }
}

function showHideFields() {
    var selectOption = document.getElementById('selectOption');
    var courseContent = document.getElementById('courseContent');
    var teachingPlan = document.getElementById('teachingPlan');
    var lessonPlan = document.getElementById('lessonPlan');
    var quizgeneration = document.getElementById('quizgeneration');
    var labActivity = document.getElementById('labActivity');

    // Hide all fields initially
    courseContent.style.display = 'none';
    teachingPlan.style.display = 'none';
    lessonPlan.style.display = 'none';
    quizgeneration.style.display = 'none';
    labActivity.style.display = 'none';

    // Show the selected field based on the dropdown value
    if (selectOption.value === 'course content') {
        courseContent.style.display = 'block';
    } else if (selectOption.value === 'teaching plan') {
        teachingPlan.style.display = 'block';
    } else if (selectOption.value === 'lesson plan') {
        lessonPlan.style.display = 'block';
    } else if (selectOption.value === 'quiz generation') {
        quizgeneration.style.display = 'block';
    } else if (selectOption.value === 'lab activity') {
        labActivity.style.display = 'block';
    }
}