document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const alertBox = document.getElementById('alertMessage');
    const btnText = document.getElementById('btnText');
    const btnSpinner = document.getElementById('btnSpinner');
    const btnLogin = document.querySelector('.btn-login');

    // Reset UI
    alertBox.classList.add('d-none');
    alertBox.className = 'alert d-none mt-3'; // reset colors
    btnText.classList.add('d-none');
    btnSpinner.classList.remove('d-none');
    btnLogin.disabled = true;

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            alertBox.className = 'alert alert-success mt-3';
            alertBox.textContent = `🎉 Giriş başarılı! Yönlendiriliyorsunuz...`;
            alertBox.classList.remove('d-none');

            // Store user info if needed (optional)
            localStorage.setItem('username', data.username);

            setTimeout(() => {
                window.location.href = '/index.html';
            }, 1000);
        } else {
            // API Error
            throw new Error(data.detail || 'Giriş başarısız');
        }

    } catch (error) {
        // Network or API Error
        alertBox.className = 'alert alert-danger mt-3';
        alertBox.textContent = `⚠️ Hata: ${error.message}`;
        alertBox.classList.remove('d-none');

        btnText.classList.remove('d-none');
        btnSpinner.classList.add('d-none');
        btnLogin.disabled = false;
    }
});
