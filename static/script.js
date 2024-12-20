document.getElementById('dataForm').addEventListener('submit', (event) => {
event.preventDefault();

const enrollNo = document.getElementById('enrollNo').value;
const classNo = document.getElementById('classNo').value;

fetch('/submit_data', {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json'
    },
    body: JSON.stringify({ enrollNo, classNo })
})
.then(response => {
    if (response.ok) {
    alert('Data submitted successfully!');
    // Clear the form fields
    document.getElementById('enrollNo').value = '';
    document.getElementById('classNo').value = '';
    } else {
    alert('Error submitting data. Please try again.');
    }
})
.catch(error => {
    console.error('Error:', error);
    alert('An error occurred. Please try again later.');
});
}); 