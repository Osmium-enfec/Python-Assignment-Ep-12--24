document.addEventListener('DOMContentLoaded', function() {
    // Set current year in footer
    const yearElement = document.getElementById('year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize table search functionality
    const searchInput = document.querySelector('.table-search');
    if (searchInput) {
        searchInput.addEventListener('keyup', filterTable);
    }

    // Add delete confirmation
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this record?')) {
                e.preventDefault();
            }
        });
    });

    // Table sort functionality
    const tableHeaders = document.querySelectorAll('.sortable-header');
    tableHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', sortTable);
    });
});

function filterTable(e) {
    const searchTerm = e.target.value.toLowerCase();
    const tableRows = document.querySelectorAll('table tbody tr');
    
    tableRows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

function sortTable(e) {
    const table = e.target.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = e.target.cellIndex;
    
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        if (!isNaN(aValue) && !isNaN(bValue)) {
            return aValue - bValue;
        }
        return aValue.localeCompare(bValue);
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

// Print table functionality
function printTable() {
    const table = document.querySelector('.table-responsive');
    const printWindow = window.open('', '', 'height=400,width=800');
    printWindow.document.write(table.innerHTML);
    printWindow.document.close();
    printWindow.print();
}
