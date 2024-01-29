function togglePopup() {
    var popup = document.getElementById("popup");
    if (popup.style.display === "none" || popup.style.display === "") {
        popup.style.display = "block";
    } else {
        popup.style.display = "none";
    }
}

function closePopup() {
document.getElementById("popup").style.display = "none";
}


function openPopup() {
var popup = document.getElementById('popup');
popup.style.display = 'block';
}

function closePopup() {
var popup = document.getElementById('popup');
popup.style.display = 'none';
}

function confirmReview() {
    var name = document.getElementById('name').value;
    if (!name) {
        alert('Please enter your name.');
    } else {
        // Update the form action to include the name name
        var form = document.getElementById('review-form');
        form.action = form.action + '?name=' + name;
        form.submit();
    }
    closePopup();
}
