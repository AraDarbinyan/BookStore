function changeMainPhoto(thumbnail) {
    document.getElementById('main-book-photo').src = thumbnail.src;
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("registerForm").addEventListener("submit", function (event) {
        let email = document.getElementById("email").value;
        let phone = document.getElementById("phone").value;

        let emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
        let phonePattern = /^\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$/;

        if (!emailPattern.test(email) && !phonePattern.test(phone)) {
            alert("Invalid email and phone formats");
            event.preventDefault();
        }
        else if (!emailPattern.test(email)) {
            alert("Invalid email format");
            event.preventDefault();
        }
        else if (!phonePattern.test(phone)) {
            alert("Invalid phone number");
            event.preventDefault();
        }
    });
});