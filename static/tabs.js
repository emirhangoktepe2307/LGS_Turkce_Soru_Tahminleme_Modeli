const tabs = document.querySelectorAll(".panel-tab");
const dropdown = document.getElementById("konuSelect");
const btnSoruOlustur = document.getElementById("btnSoruOlustur");
const soruListesi = document.getElementById("soruListesi");
const yilSelect = document.getElementById("yilSelect");

// API URL
const API_URL = "http://localhost:8000/api";

// Aktif soru tipi (başlangıçta cumlede)
let currentSoruTipi = "cumlede";

// Konuları API'den yükle
async function loadTopics(soruTipi) {
    try {
        const response = await fetch(`${API_URL}/konular/${soruTipi}`);
        if (!response.ok) throw new Error("API hatası");

        const data = await response.json();

        dropdown.innerHTML = "";
        data.konular.forEach(konu => {
            dropdown.innerHTML += `<option value="${konu}">${konu}</option>`;
        });

        // URL'de auto=true varsa otomatik seçim ve üretim yap
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('auto') === 'true' && dropdown.options.length > 0) {
            // Rastgele bir konu seç
            const randomIndex = Math.floor(Math.random() * dropdown.options.length);
            dropdown.selectedIndex = randomIndex;

            // URL parametresini temizle (tekrar tekrar çalışmasın)
            window.history.replaceState({}, document.title, window.location.pathname);

            // Kullanıcıya bilgi ver (isteğe bağlı, şimdilik direkt butona basıyoruz)
            console.log("Otomatik soru üretimi başlatılıyor...");

            // Butona tıkla
            btnSoruOlustur.click();
        }

    } catch (error) {
        console.error("Konular yüklenirken hata:", error);
        dropdown.innerHTML = "<option>Hata oluştu</option>";
    }
}

// İlk açılış
loadTopics(currentSoruTipi);

// Tab değişim olayları
tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        // Aktif tab güncelleme
        tabs.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");

        // Soru tipini güncelle
        currentSoruTipi = tab.dataset.type;

        // Konuları yeniden yükle
        loadTopics(currentSoruTipi);
    });
});

// Soru oluştur buton olayı
btnSoruOlustur.addEventListener("click", async () => {
    const konu = dropdown.value;
    const yil = parseInt(yilSelect.value);

    // Yükleniyor durumu
    btnSoruOlustur.textContent = "Oluşturuluyor...";
    btnSoruOlustur.disabled = true;
    soruListesi.innerHTML = "";

    try {
        const payload = {
            konu: konu,
            yil: yil,
            soru_tipi: currentSoruTipi,
            username: localStorage.getItem('username') // Kullanıcı adı eklendi
        };

        const response = await fetch(`${API_URL}/sorular/olustur`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Soru oluşturma hatası");

        const sorular = await response.json();
        renderSorular(sorular);

    } catch (error) {
        console.error("Hata:", error);
        alert("Soru oluşturulurken bir hata meydana geldi!");
    } finally {
        btnSoruOlustur.textContent = "SORULARI GÖR";
        btnSoruOlustur.disabled = false;
    }
});

// Soruları ekrana basma fonksiyonu
function renderSorular(sorular) {
    let html = "";

    sorular.forEach((soru, index) => {
        html += `
        <div class="card mb-4 shadow-sm" style="border-radius: 12px; border: none; background: #fff;">
            <div class="card-header d-flex justify-content-between align-items-center" 
                 style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 12px 12px 0 0; padding: 1rem 1.5rem;">
                <span class="badge bg-primary rounded-pill">Soru ${index + 1}</span>
                <small class="text-muted fw-bold">${soru.konu} (${soru.yil})</small>
            </div>
            <div class="card-body p-4">
                <p class="card-text fs-5 mb-4">${soru.soru_metni}</p>
                <div class="d-grid gap-2">
                    ${soru.secenekler.map(secenek => `
                        <button class="btn btn-outline-dark text-start p-3 fw-medium" style="border-radius: 8px;">
                            ${secenek}
                        </button>
                    `).join('')}
                </div>
                
                <div class="mt-4 pt-3 border-top">
                    <button class="btn btn-success btn-sm" type="button" data-bs-toggle="collapse" data-bs-target="#cevap${soru.id}">
                        Cevabı Gör
                    </button>
                    <div class="collapse mt-2" id="cevap${soru.id}">
                        <div class="card card-body bg-success-subtle border-success text-success fw-bold">
                            Doğru Cevap: ${soru.dogru_cevap}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;
    });

    soruListesi.innerHTML = `<div class="container container-custom pb-5">${html}</div>`;
}
