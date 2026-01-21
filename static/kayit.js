document.getElementById('registerForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const alertBox = document.getElementById('alertMessage');
    const btnText = document.getElementById('btnText');
    const btnSpinner = document.getElementById('btnSpinner');
    const btnRegister = document.querySelector('.btn-register');

    // Reset UI
    alertBox.classList.add('d-none');
    alertBox.className = 'alert d-none mt-3'; // reset colors
    btnText.classList.add('d-none');
    btnSpinner.classList.remove('d-none');
    btnRegister.disabled = true;

    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            alertBox.className = 'alert alert-success mt-3';
            alertBox.textContent = `🎉 ${data.message}! Yönlendiriliyorsunuz...`;
            alertBox.classList.remove('d-none');

            setTimeout(() => {
                window.location.href = '/giris.html';
            }, 2000);
        } else {
            // API Error
            throw new Error(data.detail || 'Kayıt başarısız oldu');
        }

    } catch (error) {
        // Network or API Error
        alertBox.className = 'alert alert-danger mt-3';
        alertBox.textContent = `⚠️ Hata: ${error.message}`;
        alertBox.classList.remove('d-none');

        btnText.classList.remove('d-none');
        btnSpinner.classList.add('d-none');
        btnRegister.disabled = false;
    }
});
