// Topic 19-20: Gallery JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Topic 19: Initialize gallery interactions
    initializeGallery();
    initializeComments();
});

function initializeGallery() {
    // Topic 20: Click handlers for images
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const img = this.querySelector('img');
            if (img) {
                openLightbox(img.src);
            }
        });
    });
}

function openLightbox(src) {
    // Topic 19-20: Open image in lightbox
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-content');
    
    if (lightbox && lightboxImg) {
        lightboxImg.src = src;
        lightbox.style.display = 'block';
    }
}

function closeLightbox() {
    // Topic 20: Close lightbox
    const lightbox = document.getElementById('lightbox');
    if (lightbox) {
        lightbox.style.display = 'none';
    }
}

function initializeComments() {
    // Topic 61-70: Comment form handling
    const commentForm = document.querySelector('.comment-form form');
    
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            // Topic 62: Validate form before submit
            const textField = this.querySelector('textarea');
            if (textField && textField.value.length < 10) {
                alert('Comment must be at least 10 characters long');
                e.preventDefault();
            }
        });
    }
}

// Topic 20: Keyboard navigation
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeLightbox();
    }
});
