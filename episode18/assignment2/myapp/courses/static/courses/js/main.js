// Episode 18 - Assignment 2: Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initializeFooterYear();
    initializeBootstrapTooltips();
    initializeDeleteConfirmation();
    initializeTableSearch();
    initializeScrollEffects();
});

/**
 * Display current year in footer
 */
function initializeFooterYear() {
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeBootstrapTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Confirm delete actions before proceeding
 */
function initializeDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Search/filter table rows by text input
 */
function initializeTableSearch() {
    const searchInputs = document.querySelectorAll('.table-search');
    
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function(e) {
            const searchValue = this.value.toLowerCase();
            const table = this.closest('.card')?.querySelector('table') || 
                          document.querySelector('table');
            
            if (!table) return;
            
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchValue) ? '' : 'none';
            });
        });
    });
}

/**
 * Add scroll effects to navbar
 */
function initializeScrollEffects() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 10) {
            navbar.style.boxShadow = '0 0.5rem 1rem rgba(0, 0, 0, 0.15)';
        } else {
            navbar.style.boxShadow = '0 0.125rem 0.25rem rgba(0, 0, 0, 0.075)';
        }
    });
}

/**
 * Sort table column when header is clicked
 * Usage: Add data-sortable="true" to th element
 */
function makeTableSortable(tableSelector = 'table') {
    const table = document.querySelector(tableSelector);
    if (!table) return;
    
    const headers = table.querySelectorAll('th[data-sortable="true"]');
    
    headers.forEach((header, index) => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            sortTable(table, index, this.classList.contains('sorted-asc'));
        });
    });
}

/**
 * Sort table by column index
 */
function sortTable(table, columnIndex, isAscending = true) {
    const rows = [].slice.call(table.querySelectorAll('tbody tr'));
    
    rows.sort(function(rowA, rowB) {
        const cellA = rowA.children[columnIndex].textContent.trim();
        const cellB = rowB.children[columnIndex].textContent.trim();
        
        // Try to parse as numbers
        const numA = parseFloat(cellA);
        const numB = parseFloat(cellB);
        
        if (!isNaN(numA) && !isNaN(numB)) {
            return isAscending ? numA - numB : numB - numA;
        }
        
        // String comparison
        return isAscending ? 
            cellA.localeCompare(cellB) : 
            cellB.localeCompare(cellA);
    });
    
    // Re-append sorted rows
    const tbody = table.querySelector('tbody');
    rows.forEach(row => tbody.appendChild(row));
    
    // Update header classes
    table.querySelectorAll('th').forEach((th, idx) => {
        th.classList.remove('sorted-asc', 'sorted-desc');
        if (idx === columnIndex) {
            th.classList.add(isAscending ? 'sorted-desc' : 'sorted-asc');
        }
    });
}

/**
 * Format date to readable string
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Toggle dark mode (if implemented)
 */
function toggleDarkMode() {
    const html = document.documentElement;
    html.dataset.bsTheme = html.dataset.bsTheme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', html.dataset.bsTheme);
}

/**
 * Load saved theme preference
 */
function loadThemePreference() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.dataset.bsTheme = savedTheme;
}

/**
 * Highlight search results
 */
function highlightText(text, search) {
    if (!search) return text;
    
    const regex = new RegExp(`(${search})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

/**
 * Add animation to element
 */
function addFadeIn(element) {
    element.classList.add('fade-in');
}

/**
 * Handle form submission with loading state
 */
function handleFormSubmit(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        }
    });
}

/**
 * Export table to CSV (bonus feature)
 */
function exportTableToCSV(tableSelector, filename = 'export.csv') {
    const table = document.querySelector(tableSelector);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        let csvRow = [];
        row.querySelectorAll('th, td').forEach(cell => {
            csvRow.push('"' + cell.textContent.trim() + '"');
        });
        csv.push(csvRow.join(','));
    });
    
    // Create download link
    const csvContent = 'data:text/csv;charset=utf-8,' + csv.join('\n');
    const link = document.createElement('a');
    link.setAttribute('href', encodeURI(csvContent));
    link.setAttribute('download', filename);
    link.click();
}

/**
 * Print table
 */
function printTable(tableSelector) {
    const table = document.querySelector(tableSelector);
    if (!table) return;
    
    const printWindow = window.open('', '', 'width=1000,height=600');
    printWindow.document.write('<html><head><title>Print</title>');
    printWindow.document.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">');
    printWindow.document.write('</head><body>');
    printWindow.document.write(table.outerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}

// Export functions for global use
window.tableSort = makeTableSortable;
window.exportCSV = exportTableToCSV;
window.printTable = printTable;
window.toggleDarkMode = toggleDarkMode;
