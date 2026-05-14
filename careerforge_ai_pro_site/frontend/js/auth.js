const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');

if (loginForm) {
    loginForm.addEventListener('submit', (event) => {
        event.preventDefault();
        window.location.href = 'dashboard.html';
    });
}

if (signupForm) {
    signupForm.addEventListener('submit', (event) => {
        event.preventDefault();
        window.location.href = 'profile.html';
    });
}
