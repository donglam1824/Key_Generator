const registerButton = document.getElementById('register-button');
const registerUrl = registerButton.dataset.registerUrl;

registerButton.addEventListener('click', function() {
    window.location.href = registerUrl;
});