// GitHub PR Statistics Tool - Frontend JavaScript

let currentResults = null;

// DOM Elements
const configSection = document.getElementById('config-section');
const loadingSection = document.getElementById('loading-section');
const errorSection = document.getElementById('error-section');
const resultsSection = document.getElementById('results-section');

const configForm = document.getElementById('config-form');
const toggleTokenBtn = document.getElementById('toggle-token');
const tokenInput = document.getElementById('token');
const loadingMessage = document.getElementById('loading-message');
const errorMessage = document.getElementById('error-message');
const retryBtn = document.getElementById('retry-btn');
const newAnalysisBtn = document.getElementById('new-analysis-btn');

const statsTable = document.getElementById('stats-tbody');
const statsTfoot = document.getElementById('stats-tfoot');
const toggleDetailsBtn = document.getElementById('toggle-details-btn');
const detailsList = document.getElementById('details-list');
const exportJsonBtn = document.getElementById('export-json-btn');
const exportCsvBtn = document.getElementById('export-csv-btn');

// Show/Hide password toggle
toggleTokenBtn.addEventListener('click', () => {
    if (tokenInput.type === 'password') {
        tokenInput.type = 'text';
        toggleTokenBtn.textContent = '🙈';
    } else {
        tokenInput.type = 'password';
        toggleTokenBtn.textContent = '👁️';
    }
});

// Form submission
configForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    await analyzeData();
});

// Retry button
retryBtn.addEventListener('click', () => {
    showSection('config');
});

// New analysis button
newAnalysisBtn.addEventListener('click', () => {
    configForm.reset();
    showSection('config');
});

// Toggle details
toggleDetailsBtn.addEventListener('click', () => {
    if (detailsList.classList.contains('hidden')) {
        detailsList.classList.remove('hidden');
        toggleDetailsBtn.textContent = 'Hide Detailed PR List';
    } else {
        detailsList.classList.add('hidden');
        toggleDetailsBtn.textContent = 'Show Detailed PR List';
    }
});

// Export buttons
exportJsonBtn.addEventListener('click', () => {
    if (!currentResults) return;
    const blob = new Blob([JSON.stringify(currentResults, null, 2)], { type: 'application/json' });
    downloadFile(blob, 'pr-statistics.json');
});

exportCsvBtn.addEventListener('click', () => {
    if (!currentResults) return;
    const csv = convertToCSV(currentResults);
    const blob = new Blob([csv], { type: 'text/csv' });
    downloadFile(blob, 'pr-statistics.csv');
});

// Functions
function showSection(section) {
    configSection.classList.add('hidden');
    loadingSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    resultsSection.classList.add('hidden');

    switch(section) {
        case 'config':
            configSection.classList.remove('hidden');
            break;
        case 'loading':
            loadingSection.classList.remove('hidden');
            break;
        case 'error':
            errorSection.classList.remove('hidden');
            break;
        case 'results':
            resultsSection.classList.remove('hidden');
            break;
    }
}

async function analyzeData() {
    const formData = new FormData(configForm);

    const token = formData.get('token').trim();
    const repository = formData.get('repository').trim();
    const usersText = formData.get('users').trim();
    const startDate = formData.get('start_date');
    const endDate = formData.get('end_date');

    // Parse users (one per line)
    const users = usersText.split('\n')
        .map(u => u.trim())
        .filter(u => u.length > 0);

    if (users.length === 0) {
        showError('Please enter at least one GitHub username');
        return;
    }

    const requestData = {
        token: token,
        users: users,
        repository: repository || undefined,
        start_date: startDate || undefined,
        end_date: endDate || undefined
    };

    showSection('loading');
    loadingMessage.textContent = 'Fetching PR data...';

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.details || data.error || 'Unknown error occurred');
        }

        currentResults = data;
        displayResults(data);
        showSection('results');

    } catch (error) {
        showError(error.message);
    }
}

function showError(message) {
    errorMessage.textContent = message;
    showSection('error');
}

function displayResults(data) {
    // Clear previous results
    statsTable.innerHTML = '';
    statsTfoot.innerHTML = '';
    detailsList.innerHTML = '';
    detailsList.classList.add('hidden');
    toggleDetailsBtn.textContent = 'Show Detailed PR List';

    if (!data.summary || data.summary.length === 0) {
        statsTable.innerHTML = '<tr><td colspan="4" style="text-align: center;">No PRs found</td></tr>';
        return;
    }

    // Populate summary table
    data.summary.forEach(stat => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${escapeHtml(stat.user)}</td>
            <td>${stat.total_prs}</td>
            <td>${stat.avg_lines_per_pr.toFixed(1)}</td>
            <td>${stat.total_lines.toLocaleString()}</td>
        `;
        statsTable.appendChild(row);
    });

    // Add totals row
    const totalPRs = data.total_prs;
    const totalLines = data.summary.reduce((sum, s) => sum + s.total_lines, 0);
    const overallAvg = totalPRs > 0 ? totalLines / totalPRs : 0;

    const footerRow = document.createElement('tr');
    footerRow.innerHTML = `
        <td><strong>TOTAL</strong></td>
        <td><strong>${totalPRs}</strong></td>
        <td><strong>${overallAvg.toFixed(1)}</strong></td>
        <td><strong>${totalLines.toLocaleString()}</strong></td>
    `;
    statsTfoot.appendChild(footerRow);

    // Populate detailed PR list
    if (data.prs && data.prs.length > 0) {
        const sortedPRs = [...data.prs].sort((a, b) =>
            new Date(b.merged_at) - new Date(a.merged_at)
        );

        sortedPRs.forEach(pr => {
            const prItem = document.createElement('div');
            prItem.className = 'pr-item';
            prItem.innerHTML = `
                <h4>#${pr.number} - ${escapeHtml(pr.title)}</h4>
                <p><strong>Author:</strong> ${escapeHtml(pr.author)}</p>
                <p><strong>Merged:</strong> ${new Date(pr.merged_at).toLocaleString()}</p>
                <p><strong>Lines:</strong> +${pr.additions} -${pr.deletions} (total: ${pr.total_lines})</p>
                <p><a href="${escapeHtml(pr.url)}" target="_blank">View on GitHub →</a></p>
            `;
            detailsList.appendChild(prItem);
        });
    }

    // Draw chart (placeholder for now - will be implemented with Chart.js)
    drawChart(data.summary);
}

let chartInstance = null;

function drawChart(summary) {
    const canvas = document.getElementById('pr-chart');

    // Destroy previous chart if exists
    if (chartInstance) {
        chartInstance.destroy();
    }

    if (!summary || summary.length === 0) {
        return;
    }

    const labels = summary.map(s => s.user);
    const prCounts = summary.map(s => s.total_prs);
    const avgLines = summary.map(s => s.avg_lines_per_pr);

    chartInstance = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Total PRs',
                    data: prCounts,
                    backgroundColor: 'rgba(3, 102, 214, 0.7)',
                    borderColor: 'rgba(3, 102, 214, 1)',
                    borderWidth: 1,
                    yAxisID: 'y'
                },
                {
                    label: 'Avg Lines per PR',
                    data: avgLines,
                    backgroundColor: 'rgba(40, 167, 69, 0.7)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 1,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                title: {
                    display: true,
                    text: 'PR Activity Comparison',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    display: true,
                    position: 'top',
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Total PRs'
                    },
                    beginAtZero: true
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Avg Lines per PR'
                    },
                    beginAtZero: true,
                    grid: {
                        drawOnChartArea: false,
                    },
                }
            }
        }
    });
}

function convertToCSV(data) {
    let csv = 'user,total_prs,avg_lines_per_pr,total_lines\n';
    data.summary.forEach(stat => {
        csv += `${stat.user},${stat.total_prs},${stat.avg_lines_per_pr},${stat.total_lines}\n`;
    });
    return csv;
}

function downloadFile(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Set default end date to today
document.getElementById('end_date').valueAsDate = new Date();
