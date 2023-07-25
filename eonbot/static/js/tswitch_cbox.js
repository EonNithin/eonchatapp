function validateForm() {
  var checkbox = document.getElementById("myCheckbox");
  
  if (!checkbox.checked) {
    alert("Please select the checkbox.");
    return false; // Prevent form submission
  }
  
  return true; // Allow form submission
}

