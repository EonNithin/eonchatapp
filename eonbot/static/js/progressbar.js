
document.getElementById("myForm").addEventListener("submit", function(event) {
    // Prevent form submission
    //event.preventDefault();

    // Hide the form
    document.getElementById("myForm").style.display = "none";

    // Show the progress bars
    var progressBars = document.querySelectorAll(".progress-bar");
    progressBars.forEach(function(progressBar) {
        progressBar.style.display = "block";
    });

    // Animate the progress bars
    var widths = [100, 200, 300]; // Widths of the progress bars
    var progressBarFills = document.querySelectorAll(".progress-fill");

    var animationCount = widths.length;

    widths.forEach(function(width, index) {
        var progressBarFill = progressBarFills[index];
        var currentWidth = 0;
        var interval = setInterval(function() {
            if (currentWidth >= width) {
                clearInterval(interval);
                animationCount--;

                if (animationCount === 0) {
                    // Hide the progress bars after all animations complete
                    progressBars.forEach(function(progressBar) {
                        progressBar.style.display = "none";
                    });
                    // Show the form again
                    document.getElementById("myForm").style.display = "block";
                }
            } else {
                currentWidth++;
                progressBarFill.style.width = currentWidth + "px";
            }
        }, 5); // Adjust the interval to control the animation speed
    });
});
