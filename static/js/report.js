function displayImage() {
    var id = document.getElementById("patient_id").value;
    var name = document.getElementById("patient_name").value;
    var name = document.getElementById("symptoms").value;
    var image = document.getElementById("image");

    if (image.complete && image.naturalWidth !== 0) {
        // Image is loaded and displayed
        return true;
    } else {
        alert("Image not found.");
        return false;
    }
}
