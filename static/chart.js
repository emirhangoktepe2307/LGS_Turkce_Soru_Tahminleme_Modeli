document.addEventListener("DOMContentLoaded", function () {

    const canvas = document.getElementById("weeklyChart");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"],
            datasets: [
                {
                    label: "Çözülen Soru",
                    data: [12, 9, 7, 14, 18, 5, 8],
                    borderColor: "#EF4444",
                    backgroundColor: "rgba(239,68,68,0.15)",
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                },
            ],
        },
        options: {
            plugins: {
                legend: { display: false },
            },
            scales: {
                y: { beginAtZero: true },
            },
        },
    });

    const canvasCorrect = document.getElementById("correctAnswersChart");
    if (canvasCorrect) {
        const ctxCorrect = canvasCorrect.getContext("2d");
        new Chart(ctxCorrect, {
            type: "line",
            data: {
                labels: ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"],
                datasets: [
                    {
                        label: "Doğru Çözülen",
                        data: [10, 8, 6, 12, 15, 4, 7], // Sample data slightly lower than total
                        borderColor: "#10B981", // Green color
                        backgroundColor: "rgba(16, 185, 129, 0.15)",
                        borderWidth: 3,
                        tension: 0.4,
                        fill: true,
                    },
                ],
            },
            options: {
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    y: { beginAtZero: true },
                },
            },
        });
    }
});
