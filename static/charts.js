function renderBarChart(labels, units, uptimes) {
  new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Units Produced',
          backgroundColor: '#3498db',
          data: units
        },
        {
          label: 'Uptime (hrs)',
          backgroundColor: '#2ecc71',
          data: uptimes
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true }
      }
    }
  });
}

function renderPieChart(labels, values) {
  new Chart(document.getElementById('pieChart'), {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: ['#f44336', '#4caf50', '#2196f3', '#ff9800', '#8e44ad']
      }]
    },
    options: { responsive: true }
  });
}

function renderLineChart(labels, values) {
  new Chart(document.getElementById('lineChart'), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Downtime (hrs)',
        borderColor: '#e74c3c',
        fill: false,
        data: values
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true }
      }
    }
  });
}

function renderSummaryBar(labels, values) {
  new Chart(document.getElementById('summaryBar'), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Units Produced',
        data: values,
        backgroundColor: '#2471a3'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          title: {
            display: true,
            text: 'Units Produced',
            font: {weight: 'bold'}
          }
        },
        x: {
          title: {
            display: true,
            text: 'Day of Week',
            font: {weight: 'bold'}
          }
        }
      }
    }
  });
}
