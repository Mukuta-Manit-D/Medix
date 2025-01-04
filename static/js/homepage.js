
function updateFileNameDisplay() {
  const fileInput = document.getElementById("image");
  const fileNameDisplay = document.getElementById("fileNameDisplay");

  if (fileInput.files.length > 0) {
    fileNameDisplay.textContent = "Uploaded Successfully";
  } else {
    fileNameDisplay.textContent = "No file chosen";
  }
}

$(

  function () {
    $("#submitBtn").click(function () {
      $("#submitBtn").addClass("onclic", 250, validate);
    });

    function validate() {
      setTimeout(function () {
        $("#submitBtn").removeClass("onclic");
        $("#submitBtn").addClass("validate", 450, callback);
      }, 2250);
    }

    function callback() {
      setTimeout(function () {
        $("#submitBtn").removeClass("validate");
      }, 1250);
    }
  });

function submitImage() {
  const fileInput = document.getElementById('image');
  const saveButton = document.getElementById('submit_button');
  const responseText = document.getElementById('result');

  if (fileInput.files.length > 0) {
    saveButton.disabled = true;
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    fetch('/submit', {
      method: 'POST',
      body: formData,
    })
      .then(response => response.text())
      .then(result => {
        responseText.innerHTML = result;
        saveButton.disabled = false;
      })
      .catch(error => {
        responseText.innerHTML = 'Error occurred while saving the image.';
        saveButton.disabled = false;
      });
  } else {
    responseText.innerHTML = 'Please choose an image first.';
  }
}

function saveImage() {
  const patientName = document.getElementById('patient_name').value;
  const patientId = document.getElementById('patient_id').value;
  const result = document.getElementById('result').innerHTML;
  const image = document.getElementById('image');
  

  if (patientName === '' || patientId === '') {
    alert('Plese fill the Patient ID and Patient Name');
    return;
  }

  if(image.files.length === 0){
    alert("Plese choose an Image First")
    return;
  }

  if(result === ''){
    alert('click of the submit button befor saving the Data')
    return;
  }

  const formData = new FormData();
  formData.append('image', image.files[0]);
  formData.append('patient_id', patientId);
  formData.append('patient_name', patientName);
  formData.append('result', result)

  fetch('/save', {
    method: 'POST',
    body: formData,
  })
    .then(response => response.text())
    .then(result => {
      // document.getElementById('result').innerHTML = result;
      alert(result)
    })
    .catch(error => {
      alert('Error occurred while saving the data')
    });
}


function clearFields(){
  document.getElementById("patient_name").value = "";
  document.getElementById("patient_id").value = "";
  document.getElementById("image").value = "";
  document.getElementById("result").innerHTML = "";
  updateFileNameDisplay();
}


// Add event listener to the file input to trigger the update when a file is chosen
const fileInput = document.getElementById("image");
fileInput.addEventListener("change", updateFileNameDisplay);

// Call the function on page load to set the initial message
updateFileNameDisplay();
