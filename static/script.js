// Geolocation function
function initGeolocation() {
    const latInput = document.getElementById('lat');
    const lonInput = document.getElementById('lon');
    
    if (latInput && lonInput && navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(pos) {
            latInput.value = pos.coords.latitude;
            lonInput.value = pos.coords.longitude;
        });
    }
}

// Form validation
function validateImageForm() {
    const fileInput = document.querySelector('input[name="file"]');
    if (fileInput && fileInput.files.length === 0) {
        alert('Please select a file to upload');
        return false;
    }
    
    const file = fileInput.files[0];
    if (file && !file.type.startsWith('image/')) {
        alert('Please upload a valid image file');
        return false;
    }
    
    return true;
}

function validateVideoForm() {
    const fileInput = document.querySelector('input[name="file"]');
    if (fileInput && fileInput.files.length === 0) {
        alert('Please select a video to upload');
        return false;
    }
    
    const file = fileInput.files[0];
    if (file && !file.type.startsWith('video/')) {
        alert('Please upload a valid video file');
        return false;
    }
    
    return true;
}

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
});

// Add loading effect on form submit
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', function(e) {
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            
            // Re-enable after 30 seconds (in case of error)
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = submitBtn.getAttribute('data-original-text') || submitBtn.innerHTML;
            }, 30000);
            
            // Store original text
            if (!submitBtn.getAttribute('data-original-text')) {
                submitBtn.setAttribute('data-original-text', submitBtn.innerHTML);
            }
        }
    });
});

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add scroll to top button
window.addEventListener('load', function() {
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollBtn.style.position = 'fixed';
    scrollBtn.style.bottom = '20px';
    scrollBtn.style.right = '20px';
    scrollBtn.style.width = '50px';
    scrollBtn.style.height = '50px';
    scrollBtn.style.borderRadius = '50%';
    scrollBtn.style.display = 'none';
    scrollBtn.style.zIndex = '1000';
    scrollBtn.onclick = scrollToTop;
    document.body.appendChild(scrollBtn);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    });
});

// Confirm before dangerous actions
const deleteButtons = document.querySelectorAll('.btn-danger, .btn-danger-small');
deleteButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
        if (!confirm('Are you sure you want to perform this action?')) {
            e.preventDefault();
        }
    });
});

// Live camera reload prevention
const liveForm = document.querySelector('.live-controls');
if (liveForm) {
    liveForm.addEventListener('submit', function(e) {
        const captureBtn = this.querySelector('button[name="capture"]');
        const exitBtn = this.querySelector('button[name="exit"]');
        
        if (exitBtn && e.submitter === exitBtn) {
            if (!confirm('Are you sure you want to exit live camera?')) {
                e.preventDefault();
            }
        }
    });
}

// Gallery image lightbox
const galleryImages = document.querySelectorAll('.gallery-item img');
galleryImages.forEach(img => {
    img.addEventListener('click', function() {
        const modal = document.createElement('div');
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        modal.style.backgroundColor = 'rgba(0,0,0,0.9)';
        modal.style.zIndex = '2000';
        modal.style.display = 'flex';
        modal.style.alignItems = 'center';
        modal.style.justifyContent = 'center';
        modal.style.cursor = 'pointer';
        
        const imgElement = document.createElement('img');
        imgElement.src = this.src;
        imgElement.style.maxWidth = '90%';
        imgElement.style.maxHeight = '90%';
        imgElement.style.borderRadius = '1rem';
        
        modal.appendChild(imgElement);
        modal.onclick = () => modal.remove();
        document.body.appendChild(modal);
    });
});

// Copy result to clipboard
const resultText = document.querySelector('.result-text');
if (resultText) {
    const copyBtn = document.createElement('button');
    copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy Result';
    copyBtn.style.marginTop = '0.5rem';
    copyBtn.style.padding = '0.5rem 1rem';
    copyBtn.style.fontSize = '0.875rem';
    copyBtn.onclick = () => {
        navigator.clipboard.writeText(resultText.innerText);
        alert('Result copied to clipboard!');
    };
    resultText.parentNode.insertBefore(copyBtn, resultText.nextSibling);
}