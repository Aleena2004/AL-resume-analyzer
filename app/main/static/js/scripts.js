document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[name="resume"]'); // Target the resume field specifically
    const allowedExtensions = ['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg'];
    const errorDiv = document.createElement('div'); // Create a div for custom error message
    errorDiv.className = 'alert alert-danger mt-2'; // Use Tailwind classes for styling
    const form = fileInput.closest('form');

    fileInput.parentNode.appendChild(errorDiv); // Add error div after the input

    fileInput.addEventListener('change', function() {
        const fileName = fileInput.value.split('\\').pop(); // Get filename from path
        errorDiv.textContent = ''; // Clear previous error

        if (fileName) {
            const fileExtension = fileName.split('.').pop().toLowerCase();
            if (!allowedExtensions.includes(fileExtension)) {
                errorDiv.textContent = 'Invalid file type. Please upload a PDF, Word document, or image file.';
                fileInput.value = ''; // Clear the input
                return; // Prevent further execution
            }
        } else if (fileInput.files.length === 0) {
            errorDiv.textContent = 'Please select a file.';
        }

        // Optionally prevent form submission if invalid (add form submit event listener)
        form.addEventListener('submit', function(event) {
            if (fileInput.value && !allowedExtensions.includes(fileInput.value.split('.').pop().toLowerCase())) {
                event.preventDefault();
                errorDiv.textContent = 'Invalid file type. Please select a valid file.';
            }
        }, { once: true }); // Use once to avoid multiple bindings
    });
});