
// Event listener for the "Enter" key press in the input field
document.getElementById("myInput").addEventListener("keydown", function(event) {
  if (event.keyCode == 13) {
     if (!event.shiftKey) {
        event.preventDefault();
        validateForm(event); // Call the validateForm function with the event
    }
  }
  else if(event.keyCode == 13 && event.shiftKey){
     // Prevent the default behavior (newline)
     event.preventDefault();

     // Move cursor to the next line
     var textarea = event.target;
     var startPos = textarea.selectionStart;
     var endPos = textarea.selectionEnd;
     var value = textarea.value;
 
     // Insert a newline character at the cursor position
     textarea.value = value.substring(0, startPos) + "\n" + value.substring(endPos, value.length);
 
     // Move the cursor to the next line
     textarea.selectionStart = startPos + 1;
     textarea.selectionEnd = startPos + 1;
  }
});

document.getElementById("selectOption").addEventListener("change", showHideFields);

document.getElementById("myForm").addEventListener("submit", validateForm);

function autoResize(textarea) {
    textarea.style.height = "auto"; // Reset height to auto
    textarea.style.height = textarea.scrollHeight + "px"; // Set height based on scrollHeight
}

function validateForm(event) {
    var checkbox = document.getElementById("myCheckbox");
    var selectOption = document.getElementById("selectOption");
    var labActivityField = document.getElementById("labActivityField");
    
    event.preventDefault();
    if (!checkbox.checked) {
        alert("Please select the checkbox.");
        return false; // Prevent form submission
    }
    if (selectOption.value === "" ){
        alert("Please select a topic from dropdown.");
        return false; // Prevent form submission
    }
    // Check the value of selectOption and set the required attribute accordingly
    if (selectOption.value === 'lab activity') {
        if (labActivityField.value === "" ){
            alert("Please select an activity from list of activities.");
            return false; // Prevent form submission
        }
    }
    // Show the progress bars
    var progressBars = document.querySelectorAll(".progress-bar");
    progressBars.forEach(function (progressBar) {
        progressBar.style.display = "block";
    });

    // Disable the submit button
    var submitButton = document.querySelector(".btn-primary");
    submitButton.disabled = true;

    // Allow the form submission after a short delay
    setTimeout(function () {
        document.getElementById("myForm").submit();
    }, 500); // Adjust the delay as needed
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