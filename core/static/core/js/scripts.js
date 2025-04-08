document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggle-password');
    const passwordInput = document.getElementById('id_password');

    if (toggleBtn && passwordInput) {
        toggleBtn.addEventListener('click', function () {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            toggleBtn.textContent = type === 'password' ? 'Показать' : 'Скрыть';
        });
    }
});