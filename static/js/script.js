// Custom JavaScript for Grocery Store

document.addEventListener('DOMContentLoaded', function() {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Initialize popovers
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

  // Auto-hide alerts after 5 seconds
  setTimeout(function() {
    var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
      var bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    });
  }, 5000);

  // Submit button handling - EXCLUDE forms that should submit immediately
  const submitButtons = document.querySelectorAll('button[type="submit"]');
  submitButtons.forEach(button => {
    const form = button.closest('form');
    
    // Skip if no form (shouldn't happen, but safety check)
    if (!form) return;
    
    // Skip if form action includes any of these routes
    if (form.action.includes('delete') || 
        form.action.includes('edit') ||
        form.action.includes('edit_user') ||
        form.action.includes('add_to_cart') ||
        form.action.includes('remove_from_cart') ||
        form.action.includes('update_cart_quantity') ||
        form.action.includes('cancel_order') ||
        form.action.includes('toggle_category') ||
        form.action.includes('toggle_product') ||
        form.action.includes('update_order_status') ||
        form.action.includes('checkout') ||
        form.action.includes('profile') ||
        form.action.includes('/login') ||
        form.action.includes('/register') ||
        form.action.includes('add_category') ||
        form.action.includes('add_product')) {
      return; // Don't apply processing state to these forms
    }
    
    // Skip based on current page path
    if (window.location.pathname.includes('/login') ||
        window.location.pathname.includes('/register') ||
        window.location.pathname.includes('add_category') ||
        window.location.pathname.includes('add_product') ||
        window.location.pathname.includes('edit_category') ||
        window.location.pathname.includes('edit_product') ||
        window.location.pathname.includes('edit_user') ||
        window.location.pathname.includes('checkout') ||
        window.location.pathname.includes('my_orders') ||
        window.location.pathname.includes('cart') ||
        window.location.pathname.includes('profile') ||
        window.location.pathname.includes('/admin/')) {
      return;
    }
    
    // Apply processing state to other buttons
    button.addEventListener('click', function() {
      const originalText = this.innerHTML;
      this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
      this.disabled = true;
      
      // Reset after 3 seconds as safety fallback
      setTimeout(() => {
        this.innerHTML = originalText;
        this.disabled = false;
      }, 3000);
    });
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Image lazy loading fallback for older browsers
  if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
      img.src = img.dataset.src || img.src;
    });
  }

  // Add active class to current nav item
  const currentLocation = window.location.pathname;
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentLocation) {
      link.classList.add('active');
    }
  });

  // Form validation enhancement
  const forms = document.querySelectorAll('.needs-validation');
  forms.forEach(form => {
    form.addEventListener('submit', function(event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    });
  });

  // Console log for debugging
  console.log('GroceryStore app loaded successfully');
  console.log('Current path:', window.location.pathname);
});

// Product quantity controls (for product detail page)
function updateQuantity(action) {
  const quantityInput = document.getElementById('quantity');
  if (!quantityInput) return;
  
  let currentValue = parseInt(quantityInput.value) || 1;
  const max = parseInt(quantityInput.max) || 999;
  const min = parseInt(quantityInput.min) || 1;
  
  if (action === 'increase' && currentValue < max) {
    quantityInput.value = currentValue + 1;
  } else if (action === 'decrease' && currentValue > min) {
    quantityInput.value = currentValue - 1;
  }
}

// Cart quantity update function (if needed)
function updateCartQuantity(productId, action) {
  const form = document.querySelector(`form[data-product-id="${productId}"]`);
  if (form) {
    const actionInput = form.querySelector('input[name="action"]');
    if (actionInput) {
      actionInput.value = action;
      form.submit();
    }
  }
}

// Price formatter
function formatPrice(price) {
  return '₹' + parseFloat(price).toFixed(2);
}

// Show notification (can be used for custom notifications)
function showNotification(message, type = 'info') {
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
  alertDiv.style.zIndex = '9999';
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;
  
  document.body.appendChild(alertDiv);
  
  // Auto remove after 3 seconds
  setTimeout(() => {
    alertDiv.remove();
  }, 3000);
}
