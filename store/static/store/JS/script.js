function changeMainPhoto(thumbnail) {
    document.getElementById('main-book-photo').src = thumbnail.src;
}

document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", function (event) {
            let email = document.getElementById("email").value;
            let phone = document.getElementById("phone").value;

            let emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
            let phonePattern = /^\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$/;

            if (!emailPattern.test(email) && !phonePattern.test(phone)) {
                alert("Invalid email and phone formats");
                event.preventDefault();
            }
            else if (!emailPattern.test(email)) {
                alert("Invalid email format");
                event.preventDefault();
            }
            else if (!phonePattern.test(phone)) {
                alert("Invalid phone number");
                event.preventDefault();
            }
        });
    }
});

const formatChart = document.getElementById('formatChart');

if (formatChart) {
    new Chart(formatChart, {
        type: 'pie',
        data: {
            labels: formatLabels,
            datasets: [{
                data: formatData
            }]
        }
    });
}


const topBooksChart = document.getElementById('topBooksChart');

if (topBooksChart) {
    new Chart(topBooksChart, {
        type: 'bar',
        data: {
            labels: topBooksLabels,
            datasets: [{
                label: 'Sold copies',
                data: topBooksData
            }]
        }
    });
}

const paymentMethodsChart = document.getElementById('paymentMethodsChart');

if (paymentMethodsChart) {
    new Chart(paymentMethodsChart, {
        type: 'doughnut',
        data: {
            labels: paymentMethodLabels,
            datasets: [{
                data: paymentMethodData
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

const periodTopBooksChartCanvas = document.getElementById('periodTopBooksChart');
const periodSelect = document.getElementById('periodSelect');

if (periodTopBooksChartCanvas && periodSelect) {
    const defaultPeriod = 'day';

    const periodTopBooksChart = new Chart(periodTopBooksChartCanvas, {
        type: 'bar',
        data: {
            labels: periodTopBooksDataByPeriod[defaultPeriod].labels,
            datasets: [{
                label: 'Sold copies',
                data: periodTopBooksDataByPeriod[defaultPeriod].data
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    periodSelect.addEventListener('change', function () {
        const selectedPeriod = this.value;
        const selectedData = periodTopBooksDataByPeriod[selectedPeriod];

        periodTopBooksChart.data.labels = selectedData.labels;
        periodTopBooksChart.data.datasets[0].data = selectedData.data;
        periodTopBooksChart.update();
    });
}
