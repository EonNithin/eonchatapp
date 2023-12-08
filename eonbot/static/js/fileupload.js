function displayUploadedFiles(input) {
    var fileListContainer = document.getElementById('fileList');
    fileListContainer.innerHTML = ''; // Clear previous file list

    var files = input.files;
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
    
        var listItem = document.createElement('div');
        listItem.classList.add('file-item'); // Add a class for styling
    
        // Display file name
        var fileNameElement = document.createElement('span');
        fileNameElement.textContent = 'File Name: ' + file.name;
        listItem.appendChild(fileNameElement);
    
        // Display file size
        var fileSizeElement = document.createElement('span');
        fileSizeElement.textContent = 'File Size: ' + file.size + ' bytes';
        listItem.appendChild(fileSizeElement);
    
        // Assign a unique identifier to each file item
        var fileId = 'file_' + i;
        listItem.setAttribute('id', fileId);
    /*
        // Add a remove button
        var removeButton = document.createElement('button');
        removeButton.textContent = 'x';
        removeButton.dataset.fileId = fileId;
    
        removeButton.addEventListener('click', function(event) {
            var fileIdToRemove = event.target.dataset.fileId;
            var itemToRemove = document.getElementById(fileIdToRemove);
            if (itemToRemove) {
                itemToRemove.remove();
            }
        });
        listItem.appendChild(removeButton);
    */
        fileListContainer.appendChild(listItem);
    }
}