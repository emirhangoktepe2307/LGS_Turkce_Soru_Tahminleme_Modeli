document.addEventListener("DOMContentLoaded", function () {
    const authArea = document.querySelector('.auth-area');
    if (!authArea) return;

    const currentUsername = localStorage.getItem('username');

    if (currentUsername) {
        // Kullanıcı giriş yapmış: Avatar göster
        const firstLetter = currentUsername.charAt(0).toUpperCase();

        authArea.innerHTML = `
            <div class="dropdown">
                <div class="user-avatar-circle" id="userAvatarBtn" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    ${firstLetter}
                </div>
                <ul class="dropdown-menu dropdown-menu-end border-0 shadow-lg rounded-4 mt-2 p-2" aria-labelledby="userAvatarBtn">
                    <li><span class="dropdown-header text-muted fw-bold" style="font-size: 0.8rem;">${currentUsername}</span></li>
                    <li><a class="dropdown-item rounded-3 py-2" href="/profil.html">👤 Profilim</a></li>
                    <li><hr class="dropdown-divider my-1"></li>
                    <li><button class="dropdown-item rounded-3 py-2 text-danger" id="globalLogoutBtn">🚪 Çıkış Yap</button></li>
                </ul>
            </div>
        `;

        // Çıkış Yap butonu işlevi
        const logoutBtn = document.getElementById('globalLogoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                localStorage.removeItem('username');
                window.location.href = '/giris.html';
            });
        }

    } else {
        // Kullanıcı giriş yapmamış: Giriş Yap butonu göster
        // Eğer zaten butonu varsa dokunma (bazı sayfalarda hardcoded olabilir), yoksa ekle
        const content = authArea.innerHTML.trim();
        const hasButton = content.includes('href="/giris.html"') || content.includes('btn-custom-signup');
        const hasAvatar = content.includes('user-avatar-circle');

        if (!hasButton && !hasAvatar) {
            authArea.innerHTML = `<a href="/giris.html" class="btn btn-custom-signup text-nowrap">Giriş Yap</a>`;
        }
    }
});
