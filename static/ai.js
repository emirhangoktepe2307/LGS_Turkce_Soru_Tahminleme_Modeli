document.addEventListener("DOMContentLoaded", function () {
    const btnGenerate = document.getElementById("btnGenerateReport");
    const loadingArea = document.getElementById("loadingArea");
    const reportArea = document.getElementById("reportArea");
    const markdownOutput = document.getElementById("markdownOutput");
    const reportDate = document.getElementById("reportDate");

    const API_URL = "/api";
    const currentUsername = localStorage.getItem('username');

    if (!currentUsername) {
        // Giriş yapmamışsa uyar
        markdownOutput.innerHTML = "<p class='text-danger text-center'>Analiz için lütfen önce giriş yapın.</p>";
        reportArea.classList.remove("d-none");
        btnGenerate.disabled = true;
        return;
    }

    btnGenerate.addEventListener("click", async () => {
        // UI Hazırlığı
        btnGenerate.disabled = true;
        btnGenerate.classList.add('opacity-50');
        loadingArea.classList.remove("d-none");
        reportArea.classList.add("d-none");

        try {
            const response = await fetch(`${API_URL}/ai/report`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username: currentUsername })
            });

            if (!response.ok) throw new Error("Rapor oluşturulamadı");

            const data = await response.json();

            // Raporu göster
            reportDate.textContent = new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' });
            markdownOutput.innerHTML = marked.parse(data.markdown_report);

            loadingArea.classList.add("d-none");
            reportArea.classList.remove("d-none");

            // Scroll to report
            reportArea.scrollIntoView({ behavior: 'smooth', block: 'start' });

        } catch (error) {
            console.error(error);
            loadingArea.classList.add("d-none");
            alert("Bir hata oluştu: " + error.message);
        } finally {
            btnGenerate.disabled = false;
            btnGenerate.classList.remove('opacity-50');
        }
    });
});
