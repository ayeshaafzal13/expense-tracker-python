
    // ============================================================
    // DATA MANAGEMENT
    // ============================================================
    
    let expenses = [];
    let monthlyChart = null;
    let categoryChart = null;

    // Category colors
    const categoryColors = {
        'Food': '#FF6B6B',
        'Transport': '#4ECDC4',
        'Shopping': '#45B7D1',
        'Entertainment': '#96CEB4',
        'Bills': '#FFEAA7',
        'Healthcare': '#DDA0DD',
        'Education': '#FF8C94',
        'Other': '#C3B1E1'
    };

    // Load data from JSON
    async function loadData() {
        try {
            const response = await fetch('expenses.json');
            if (response.ok) {
                expenses = await response.json();
            } else {
                expenses = [];
            }
        } catch (error) {
            console.log('No expenses.json found, starting with empty list');
            expenses = [];
        }
        updateUI();
    }

    // Save data to JSON
    async function saveData() {
        try {
            const response = await fetch('/save-expenses', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(expenses)
            });
            if (!response.ok) {
                // If server save fails, download as file
                downloadJSON(expenses);
            }
        } catch (error) {
            // If server not available, download as file
            downloadJSON(expenses);
        }
    }

    // Fallback: Download JSON file
    function downloadJSON(data) {
        const blob = new Blob([JSON.stringify(data, null, 4)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'expenses.json';
        a.click();
        URL.revokeObjectURL(url);
        showToast('📥 Data downloaded! Place expenses.json in the same folder.', 'success');
    }

    // ============================================================
    // UI UPDATE FUNCTIONS
    // ============================================================
    
    function updateUI() {
        updateStats();
        updateExpenseList();
        updateCharts();
    }

    function updateStats() {
        const total = expenses.reduce((sum, e) => sum + e.amount, 0);
        const avg = expenses.length > 0 ? total / expenses.length : 0;
        const highest = expenses.length > 0 ? Math.max(...expenses.map(e => e.amount)) : 0;
        
        document.getElementById('totalSpent').textContent = `PKR ${total.toLocaleString()}`;
        document.getElementById('totalTransactions').textContent = expenses.length;
        document.getElementById('averageAmount').textContent = `PKR ${avg.toFixed(0).toLocaleString()}`;
        document.getElementById('highestAmount').textContent = `PKR ${highest.toLocaleString()}`;
    }

    function updateExpenseList() {
        const list = document.getElementById('expenseList');
        
        if (expenses.length === 0) {
            list.innerHTML = `
                <div class="no-data">
                    <span class="big-emoji">📭</span>
                    No expenses recorded yet!<br>
                    <small>Click "Add Expense" to get started</small>
                </div>
            `;
            return;
        }
        
        const sorted = [...expenses].reverse();
        
        list.innerHTML = sorted.map(exp => {
            const amountClass = exp.amount > 1000 ? 'high' : exp.amount > 500 ? 'medium' : 'low';
            const color = categoryColors[exp.category] || '#999';
            
            return `
                <div class="expense-item">
                    <div class="left">
                        <span class="category-badge" style="background: ${color}">${exp.category}</span>
                        <span class="description">${exp.description || 'No description'}</span>
                        <span class="date">📅 ${exp.date}</span>
                    </div>
                    <div class="actions">
                        <span class="amount ${amountClass}">PKR ${exp.amount.toLocaleString()}</span>
                        <button class="btn btn-primary btn-sm" onclick="openEditModal(${exp.id})">✏️</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteExpense(${exp.id})">🗑️</button>
                    </div>
                </div>
            `;
        }).join('');
    }

    // ============================================================
    // CHART FUNCTIONS
    // ============================================================
    
    function updateCharts() {
        updateMonthlyChart();
        updateCategoryChart();
    }

    function updateMonthlyChart() {
        const monthly = {};
        expenses.forEach(exp => {
            const parts = exp.date.split('-');
            if (parts.length >= 2) {
                const month = parts[1];
                monthly[month] = (monthly[month] || 0) + exp.amount;
            }
        });
        
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const labels = Object.keys(monthly).sort().map(m => months[parseInt(m) - 1]);
        const data = Object.keys(monthly).sort().map(m => monthly[m]);
        
        const ctx = document.getElementById('monthlyChart').getContext('2d');
        
        if (monthlyChart) {
            monthlyChart.destroy();
        }
        
        monthlyChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels.length > 0 ? labels : ['No Data'],
                datasets: [{
                    label: 'Monthly Spending',
                    data: data.length > 0 ? data : [0],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#667eea',
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return 'PKR ' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    function updateCategoryChart() {
        const categories = {};
        expenses.forEach(exp => {
            categories[exp.category] = (categories[exp.category] || 0) + exp.amount;
        });
        
        const labels = Object.keys(categories);
        const data = Object.values(categories);
        const colors = labels.map(cat => categoryColors[cat] || '#999');
        
        const ctx = document.getElementById('categoryChart').getContext('2d');
        
        if (categoryChart) {
            categoryChart.destroy();
        }
        
        if (labels.length === 0) {
            categoryChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['No Data'],
                    datasets: [{
                        data: [1],
                        backgroundColor: ['#ddd']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
            return;
        }
        
        categoryChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors,
                    borderWidth: 2,
                    borderColor: 'white'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // ============================================================
    // CRUD OPERATIONS
    // ============================================================
    
    // ADD
    function openAddModal() {
        document.getElementById('addModal').classList.add('show');
        document.getElementById('addForm').reset();
        // Set default date to today
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('addDate').value = today;
    }

    document.getElementById('addForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const amount = parseFloat(document.getElementById('addAmount').value);
        const category = document.getElementById('addCategory').value;
        const description = document.getElementById('addDescription').value || 'No description';
        const date = document.getElementById('addDate').value;
        
        if (!category) {
            showToast('❌ Please select a category!', 'error');
            return;
        }
        
        // Format date as DD-MM-YYYY
        const dateObj = new Date(date);
        const formattedDate = `${String(dateObj.getDate()).padStart(2, '0')}-${String(dateObj.getMonth() + 1).padStart(2, '0')}-${dateObj.getFullYear()}`;
        
        const newExpense = {
            id: expenses.length > 0 ? Math.max(...expenses.map(e => e.id)) + 1 : 1,
            amount: amount,
            category: category,
            description: description,
            date: formattedDate,
            timestamp: new Date().toISOString()
        };
        
        expenses.push(newExpense);
        await saveData();
        updateUI();
        closeModal('addModal');
        showToast('✅ Expense added successfully!', 'success');
    });

    // EDIT
    function openEditModal(id) {
        const expense = expenses.find(e => e.id === id);
        if (!expense) return;
        
        document.getElementById('editId').value = id;
        document.getElementById('editAmount').value = expense.amount;
        document.getElementById('editCategory').value = expense.category;
        document.getElementById('editDescription').value = expense.description || '';
        
        // Convert DD-MM-YYYY to YYYY-MM-DD for date input
        const parts = expense.date.split('-');
        if (parts.length === 3) {
            const dateStr = `${parts[2]}-${parts[1]}-${parts[0]}`;
            document.getElementById('editDate').value = dateStr;
        }
        
        document.getElementById('editModal').classList.add('show');
    }

    document.getElementById('editForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const id = parseInt(document.getElementById('editId').value);
        const amount = parseFloat(document.getElementById('editAmount').value);
        const category = document.getElementById('editCategory').value;
        const description = document.getElementById('editDescription').value || 'No description';
        const date = document.getElementById('editDate').value;
        
        // Format date as DD-MM-YYYY
        const dateObj = new Date(date);
        const formattedDate = `${String(dateObj.getDate()).padStart(2, '0')}-${String(dateObj.getMonth() + 1).padStart(2, '0')}-${dateObj.getFullYear()}`;
        
        const index = expenses.findIndex(e => e.id === id);
        if (index !== -1) {
            expenses[index] = {
                ...expenses[index],
                amount: amount,
                category: category,
                description: description,
                date: formattedDate
            };
            await saveData();
            updateUI();
            closeModal('editModal');
            showToast('✅ Expense updated successfully!', 'success');
        }
    });

    // DELETE
    async function deleteExpense(id) {
        if (!confirm('Are you sure you want to delete this expense?')) return;
        
        expenses = expenses.filter(e => e.id !== id);
        await saveData();
        updateUI();
        showToast('🗑️ Expense deleted!', 'success');
    }

    // ============================================================
    // UTILITY FUNCTIONS
    // ============================================================
    
    function closeModal(id) {
        document.getElementById(id).classList.remove('show');
    }

    function showToast(message, type = 'success') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = 'toast ' + type + ' show';
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    async function refreshData() {
        await loadData();
        showToast('🔄 Data refreshed!', 'success');
    }

    // Close modal when clicking outside
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('show');
            }
        });
    });

    // ============================================================
    // INIT
    // ============================================================
    
    loadData();
    console.log('🚀 Expense Tracker Pro loaded!');
    console.log('💡 Add, edit, and delete expenses with ease!');