async function submitForm() {
    const jobTitle = document.getElementById('jobTitle').value;
    const jobDescription = document.getElementById('jobDescription').value;
    const fileInput = document.getElementById('fileUpload');
    const file = fileInput.files[0];

    // Create FormData object to send form data including file
    const formData = new FormData();
    formData.append('title', jobTitle);
    formData.append('description', jobDescription);
    formData.append('resume', file);

    try {
        const response = await fetch('http://localhost:8000/inputs', {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            const data = await response.json();
            // Handle successful response, maybe display a success message
            alert('Form submitted successfully!');
            console.log(data);
        } else {
            // Handle error response
            alert('Failed to submit form!');
        }
    } catch (error) {
        // Handle network errors
        console.error('Error:', error);
        alert('Network error occurred!');
    }
}

function clearForm() {
    document.getElementById('jobTitle').value = '';
    document.getElementById('jobDescription').value = '';
    document.getElementById('fileUpload').value = '';
    document.getElementById('result').innerText = '';
}
