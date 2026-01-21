document.addEventListener("DOMContentLoaded", function () {
    const API_URL = "/api";

    // Kullanıcı Kontrolü
    // Kullanıcı Kontrolü
    const currentUsername = localStorage.getItem('username');

    // Eğer kullanıcı adı yoksa hemen yönlendir
    if (!currentUsername) {
        window.location.replace('/giris.html');
        return;
    }

    // Kullanıcı Arayüzü Ayarları (auth.js tarafından yönetiliyor)
    // Bu kısımdaki kodlar auth.js'e taşındı.


    // 1. Profil Bilgilerini Getir
    async function getUserInfo() {
        try {
            const encodedUser = encodeURIComponent(currentUsername);
            const response = await fetch(`${API_URL}/profil/bilgiler?username=${encodedUser}`);
            if (!response.ok) throw new Error('Kullanıcı bilgisi alınamadı');

            const data = await response.json();

            document.getElementById("userName").textContent = data.ad || currentUsername;
            document.getElementById("userEmail").textContent = data.email || "E-posta yok";

        } catch (error) {
            console.error("Kullanıcı bilgisi hatası:", error);
            document.getElementById("userName").textContent = currentUsername;
            document.getElementById("userEmail").textContent = "";
        }
    }

    // 2. İstatistikleri Getir (GERÇEK VERİ)
    async function getStats() {
        try {
            const encodedUser = encodeURIComponent(currentUsername);
            const response = await fetch(`${API_URL}/profil/istatistikler?username=${encodedUser}`);
            if (!response.ok) throw new Error('İstatistik alınamadı');
            const data = await response.json();

            document.getElementById("toplamTahmin").textContent = data.toplam_tahmin;
            document.getElementById("favoriKonu").textContent = data.favori_konu;
            document.getElementById("sonAktivite").textContent = data.son_aktivite;
            document.getElementById("gunlukOrtalama").textContent = data.gunluk_ortalama;
        } catch (error) {
            console.error("İstatistik hatası:", error);
            // Hata durumunda varsayılan değerler
            document.getElementById("toplamTahmin").textContent = "0";
            document.getElementById("favoriKonu").textContent = "-";
            document.getElementById("sonAktivite").textContent = "-";
            document.getElementById("gunlukOrtalama").textContent = "0";
        }
    }

    // 3. Haftalık Grafik (Şimdilik Mock/Basit)
    async function getWeeklyChart() {
        try {
            const response = await fetch(`${API_URL}/profil/grafik/haftalik?username=${currentUsername}`);
            const data = await response.json();

            const canvas = document.getElementById("weeklyChart");
            if (!canvas) return;

            new Chart(canvas.getContext("2d"), {
                type: "bar",
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: "Tahmin Sayısı",
                        data: data.data,
                        backgroundColor: "#4f46e5",
                        borderRadius: 6
                    }]
                },
                options: {
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true } }
                }
            });
        } catch (error) {
            console.error("Grafik hatası:", error);
        }
    }

    // 4. Konu Dağılımı Grafiği (Şimdilik Mock/Basit)
    async function getContentChart() {
        try {
            const response = await fetch(`${API_URL}/profil/grafik/dogru-cevaplar?username=${currentUsername}`);
            const data = await response.json();

            const canvas = document.getElementById("contentChart");
            if (!canvas) return;

            new Chart(canvas.getContext("2d"), {
                type: "doughnut",
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: ["#10b981", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6"]
                    }]
                },
                options: {
                    plugins: { position: 'bottom' }
                }
            });
        } catch (error) {
            console.error("Grafik hatası:", error);
        }
    }

    // 5. Son Aktiviteler (GERÇEK VERİ)
    async function getRecentActivity() {
        try {
            const response = await fetch(`${API_URL}/profil/son-cozulen-sorular?username=${currentUsername}`);
            const items = await response.json();

            const tbody = document.getElementById("recentTableBody");
            let html = "";

            if (items.length === 0) {
                html = '<tr><td colspan="4" class="text-center py-4 text-muted">Henüz aktivite yok.</td></tr>';
            } else {
                items.forEach(item => {
                    html += `
                        <tr>
                            <td class="ps-4 fw-medium text-dark">${item.tarih}</td>
                            <td><span class="badge bg-light text-dark border">${item.konu}</span></td>
                            <td class="text-muted">${item.yil}</td>
                            <td><span class="badge bg-primary-subtle text-primary text-uppercase" style="font-size: 0.75rem;">${item.tur}</span></td>
                        </tr>
                    `;
                });
            }
            tbody.innerHTML = html;
        } catch (error) {
            console.error("Geçmiş hatası:", error);
        }
    }

    // Başlat
    getUserInfo();
    getStats();
    getWeeklyChart();
    getContentChart();
    getRecentActivity();
});
