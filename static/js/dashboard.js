// Dashboard specific JavaScript

class DashboardManager {
    constructor() {
        this.charts = new Map();
        this.initializeCharts();
        this.initializeRealTimeUpdates();
    }

    initializeCharts() {
        // Initialize attendance chart if exists
        const attendanceChart = document.getElementById('attendance-chart');
        if (attendanceChart) {
            this.createAttendanceChart();
        }

        // Initialize grade distribution chart if exists
        const gradeChart = document.getElementById('grade-chart');
        if (gradeChart) {
            this.createGradeDistributionChart();
        }

        // Initialize fee status chart if exists
        const feeChart = document.getElementById('fee-chart');
        if (feeChart) {
            this.createFeeStatusChart();
        }
    }

    createAttendanceChart() {
        const ctx = document.getElementById('attendance-chart').getContext('2d');
        this.charts.set('attendance', new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Attendance Rate',
                    data: [85, 92, 78, 88, 95, 60, 70],
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Weekly Attendance Trend'
                    }
                }
            }
        }));
    }

    createGradeDistributionChart() {
        const ctx = document.getElementById('grade-chart').getContext('2d');
        this.charts.set('grades', new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['A (90-100%)', 'B (80-89%)', 'C (70-79%)', 'D (60-69%)', 'F (Below 60%)'],
                datasets: [{
                    data: [25, 35, 20, 15, 5],
                    backgroundColor: [
                        '#27ae60',
                        '#3498db',
                        '#f39c12',
                        '#e67e22',
                        '#e74c3c'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Grade Distribution'
                    }
                }
            }
        }));
    }

    createFeeStatusChart() {
        const ctx = document.getElementById('fee-chart').getContext('2d');
        this.charts.set('fees', new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Collected',
                    data: [12000, 19000, 15000, 18000, 22000, 25000],
                    backgroundColor: '#27ae60'
                }, {
                    label: 'Pending',
                    data: [5000, 3000, 4000, 2000, 1000, 1500],
                    backgroundColor: '#f39c12'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Fee Collection Status'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Amount ($)'
                        }
                    }
                }
            }
        }));
    }

    initializeRealTimeUpdates() {
        // Update dashboard stats every 30 seconds
        setInterval(() => {
            this.updateDashboardStats();
        }, 30000);

        // Initialize real-time notifications
        this.initializeWebSocket();
    }

    async updateDashboardStats() {
        try {
            const response = await fetch('/api/dashboard/stats');
            const data = await response.json();
            
            // Update quick stats
            this.updateQuickStats(data);
            
            // Update charts if needed
            this.updateCharts(data);
            
        } catch (error) {
            console.error('Failed to update dashboard stats:', error);
        }
    }

    updateQuickStats(data) {
        const stats = [
            { id: 'total-students', value: data.total_students },
            { id: 'total-teachers', value: data.total_teachers },
            { id: 'total-courses', value: data.total_courses },
            { id: 'attendance-rate', value: data.attendance_rate + '%' },
            { id: 'total-revenue', value: '$' + data.total_revenue },
            { id: 'pending-fees', value: '$' + data.pending_fees }
        ];

        stats.forEach(stat => {
            const element = document.getElementById(stat.id);
            if (element) {
                // Animate counter
                this.animateCounter(element, stat.value);
            }
        });
    }

    animateCounter(element, targetValue) {
        const currentValue = parseInt(element.textContent.replace(/[^0-9]/g, '')) || 0;
        const target = parseInt(targetValue.toString().replace(/[^0-9]/g, '')) || 0;
        
        if (currentValue === target) return;

        const duration = 1000; // 1 second
        const step = (target - currentValue) / (duration / 16);
        let current = currentValue;

        const timer = setInterval(() => {
            current += step;
            if ((step > 0 && current >= target) || (step < 0 && current <= target)) {
                current = target;
                clearInterval(timer);
            }
            
            if (targetValue.toString().includes('$')) {
                element.textContent = '$' + Math.round(current).toLocaleString();
            } else if (targetValue.toString().includes('%')) {
                element.textContent = Math.round(current) + '%';
            } else {
                element.textContent = Math.round(current).toLocaleString();
            }
        }, 16);
    }

    updateCharts(data) {
        // Update charts with new data
        // This would be implemented based on specific chart data structure
    }

    initializeWebSocket() {
        // WebSocket for real-time updates
        if (typeof window.chatManager !== 'undefined') {
            // Reuse existing WebSocket connection if available
            return;
        }

        // Alternatively, set up a separate WebSocket for dashboard updates
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/dashboard`;
        
        try {
            const socket = new WebSocket(wsUrl);
            
            socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleRealTimeUpdate(data);
            };
            
            socket.onclose = () => {
                console.log('Dashboard WebSocket disconnected');
            };
            
        } catch (error) {
            console.error('Failed to connect to dashboard WebSocket:', error);
        }
    }

    handleRealTimeUpdate(data) {
        switch (data.type) {
            case 'new_notice':
                this.showNewNotice(data.notice);
                break;
            case 'attendance_update':
                this.updateAttendance(data.attendance);
                break;
            case 'grade_update':
                this.updateGrades(data.grades);
                break;
            case 'fee_update':
                this.updateFees(data.fees);
                break;
        }
    }

    showNewNotice(notice) {
        showToast(`New notice: ${notice.title}`, 'info');
        
        // Update notices list
        const noticesList = document.getElementById('notices-list');
        if (noticesList) {
            const noticeElement = this.createNoticeElement(notice);
            noticesList.insertBefore(noticeElement, noticesList.firstChild);
            
            // Limit to 5 notices
            if (noticesList.children.length > 5) {
                noticesList.removeChild(noticesList.lastChild);
            }
        }
    }

    createNoticeElement(notice) {
        const div = document.createElement('div');
        div.className = 'list-group-item';
        div.innerHTML = `
            <div class="d-flex w-100 justify-content-between">
                <h6 class="mb-1">${notice.title}</h6>
                <small>Just now</small>
            </div>
            <p class="mb-1">${notice.content}</p>
            <small class="text-muted">By ${notice.author}</small>
        `;
        return div;
    }

    updateAttendance(attendance) {
        // Update attendance chart and stats
        console.log('Attendance updated:', attendance);
    }

    updateGrades(grades) {
        // Update grade chart and stats
        console.log('Grades updated:', grades);
    }

    updateFees(fees) {
        // Update fee chart and stats
        console.log('Fees updated:', fees);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.dashboardManager = new DashboardManager();
    
    // Initialize any dashboard-specific components
    initializeDashboardComponents();
});

function initializeDashboardComponents() {
    // Initialize any plugins or components specific to dashboard
    initializeDateRangePickers();
    initializeDataTables();
    initializeExportButtons();
}

function initializeDateRangePickers() {
    // Initialize date range pickers if any
    const datePickers = document.querySelectorAll('.date-picker');
    datePickers.forEach(picker => {
        // You would integrate with a date picker library here
        picker.addEventListener('change', function() {
            updateDashboardWithDateRange(this.value);
        });
    });
}

function initializeDataTables() {
    // Initialize data tables if any
    const tables = document.querySelectorAll('.data-table');
    tables.forEach(table => {
        // You would integrate with a data table library here
        console.log('Initializing data table:', table);
    });
}

function initializeExportButtons() {
    // Initialize export functionality
    const exportButtons = document.querySelectorAll('.export-btn');
    exportButtons.forEach(button => {
        button.addEventListener('click', function() {
            const format = this.dataset.format || 'csv';
            const dataType = this.dataset.type || 'general';
            exportData(dataType, format);
        });
    });
}

async function exportData(dataType, format) {
    try {
        showToast(`Exporting ${dataType} data as ${format}...`, 'info');
        
        const response = await fetch(`/api/export/${dataType}?format=${format}`);
        const blob = await response.blob();
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${dataType}_export.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showToast('Export completed successfully', 'success');
    } catch (error) {
        console.error('Export failed:', error);
        showToast('Export failed. Please try again.', 'danger');
    }
}

function updateDashboardWithDateRange(dateRange) {
    // Update dashboard based on selected date range
    console.log('Updating dashboard with date range:', dateRange);
    
    // You would make an API call here to get updated data
    // and then update the charts and statistics
}