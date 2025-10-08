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
    
    // Skip if form action includes any of these routes
    if (form && (
        form.action.includes('delete') || 
        form.action.includes('edit') ||
        form.action.includes('edit_user') ||
        form.action.includes('add_to_cart') ||
        form.action.includes('checkout') ||
        form.action.includes('profile') ||
        form.action.includes('/login') ||
        form.action.includes('/register') ||
        form.action.includes('add_category') ||
        form.action.includes('add_product') ||
        form.action.includes('update_order_status')
    )) {
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
        window.location.pathname.includes('profile')) {
      return;
    }
    
    // Apply processing state to other buttons
    button.addEventListener('click', function() {
      const originalText = this.innerHTML;
      this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
      this.disabled = true;
      setTimeout(() => {
        this.innerHTML = originalText;
        this.disabled = false;
      }, 3000);
    });
  });
});
