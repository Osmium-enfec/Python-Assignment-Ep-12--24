// Topic 19-20: Custom JavaScript for product management

document.addEventListener('DOMContentLoaded', function() {
    // Topic 19: Page initialization
    console.log('Products page loaded');
    
    // Topic 20: Event listeners
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.borderColor = '#007bff';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.borderColor = '';
        });
    });
});

// Topic 19: Image preview for upload form
function previewImage(event) {
    const file = event.target.files[0];
    const preview = document.getElementById('imagePreview');
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}
