document.addEventListener("DOMContentLoaded", function () {
    const API_URL = "/api";
    const historyTableBody = document.getElementById("historyTableBody");
    const mebQuestionsModal = new bootstrap.Modal(document.getElementById('mebQuestionsModal'));
    const modalBody = document.getElementById("mebQuestionsBody");

    // Geçmişi API'den çek
    async function loadHistory() {
        const currentUsername = localStorage.getItem('username');
        if (!currentUsername) {
            historyTableBody.innerHTML = `<tr><td colspan="5" class="text-center">Geçmişi görmek için giriş yapmalısınız.</td></tr>`;
            return;
        }

        console.log("Fetching history for:", currentUsername);
        try {
            const url = `${API_URL}/profil/son-cozulen-sorular?username=${encodeURIComponent(currentUsername)}`;
            console.log("Request URL:", url);

            const response = await fetch(url);
            if (!response.ok) throw new Error("Geçmiş yüklenemedi");

            const historyData = await response.json();
            renderHistory(historyData);
        } catch (error) {
            console.error(error);
            historyTableBody.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Geçmiş verileri alınamadı.</td></tr>`;
        }
    }

    function renderHistory(data) {
        if (!data || data.length === 0) {
            historyTableBody.innerHTML = `<tr><td colspan="5" class="text-center">Henüz çözülmüş soru yok.</td></tr>`;
            return;
        }

        let html = "";
        data.forEach((item, index) => {
            html += `
                <tr>
                    <td>${item.tarih}</td>
                    <td>${item.konu}</td>
                    <td>${item.tur}</td>
                    <td><span class="badge bg-success">${item.basari || "Başarılı"}</span></td>
                    <td>
                        <button class="btn-meb" onclick="openMebQuestions('${item.konu}')">
                            Çıkmış Soruları Gör
                        </button>
                    </td>
                </tr>
            `;
        });
        historyTableBody.innerHTML = html;
    }

    // Global fonksiyon (onClick için)
    window.openMebQuestions = async function (topic) {
        mebQuestionsModal.show();

        // Loading state
        modalBody.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-danger" role="status" style="width: 3rem; height: 3rem;">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <h5 class="mt-3 text-secondary">"${topic}" konusu için arşiv taranıyor...</h5>
                <p class="text-muted small">Sorular veritabanından getiriliyor.</p>
            </div>
        `;

        try {
            const response = await fetch(`${API_URL}/meb-questions?topic=${encodeURIComponent(topic)}`);
            if (!response.ok) throw new Error("Sorular alınamadı");

            const data = await response.json();
            renderQuestions(data, topic);

        } catch (error) {
            console.error(error);
            modalBody.innerHTML = `
                <div class="text-center py-5 text-danger">
                    <h5>Bir hata oluştu!</h5>
                    <p>Sorular getirilemedi. Lütfen tekrar deneyin.</p>
                </div>
            `;
        }
    }

    function renderQuestions(data, topic) {
        let html = `<div class="container-fluid px-0">`;

        // Veri dizi ise (eski/basit yapı)
        if (Array.isArray(data)) {
            if (data.length === 0) {
                modalBody.innerHTML = `<div class="text-center py-5">Bu konuyla ilgili soru bulunamadı.</div>`;
                return;
            }
            html += renderQuestionList(data);
        }
        // Veri obje ise (kategorili yapı)
        else if (typeof data === 'object') {
            const categories = Object.keys(data);
            if (categories.length === 0) {
                modalBody.innerHTML = `<div class="text-center py-5">Bu konuyla ilgili soru bulunamadı.</div>`;
                return;
            }

            categories.forEach(category => {
                html += `
                    <h5 class="mt-4 mb-3 text-primary border-bottom pb-2">
                        📌 ${category}
                    </h5>
                 `;
                html += renderQuestionList(data[category]);
            });
        }

        html += `</div>`;
        modalBody.innerHTML = html;
    }

    function renderQuestionList(questions) {
        let html = "";
        questions.forEach((q) => {
            // Soru metni içindeki (20xx...) etiketini ayıklayalım
            let badgeText = "MEB Örnek";
            let questionText = q.soru_metni;

            if (questionText.startsWith("(")) {
                const closeParenIndex = questionText.indexOf(")");
                if (closeParenIndex !== -1) {
                    badgeText = questionText.substring(1, closeParenIndex);
                    questionText = questionText.substring(closeParenIndex + 1).trim();
                }
            }

            html += `
                <div class="question-card mb-3">
                    <span class="question-badge">${badgeText}</span>
                    <p class="fs-5 mb-3">${questionText}</p>
                    <div class="d-grid gap-2">
                        ${q.secenekler.map(opt => `
                            <div class="p-2 border rounded bg-white hover-bg-light">
                                ${opt}
                            </div>
                        `).join('')}
                    </div>
                    <div class="mt-3 text-end">
                        <small class="text-success fw-bold">Doğru Cevap: ${q.dogru_cevap}</small>
                    </div>
                </div>
            `;
        });
        return html;
    }

    loadHistory();
});
