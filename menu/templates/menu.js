document.addEventListener('DOMContentLoaded', function() {
   // Category filter buttons
   const filterButtons = document.querySelectorAll('.filter-btn');
   filterButtons.forEach(button => {
       button.addEventListener('click', function() {
           // Remove active class from all buttons
           filterButtons.forEach(btn => btn.classList.remove('active'));
           // Add active class to clicked button
           this.classList.add('active');

           const category = this.dataset.category;
           if (category === 'all') {
               window.location.href = '{% url "menu:list" %}';
           } else {
               window.location.href = `{% url "menu:list" %}?category=${category}`;
           }
       });
   });

   // Set active class based on current URL
   const urlParams = new URLSearchParams(window.location.search);
   const currentCategory = urlParams.get('category');
   if (currentCategory) {
       const activeButton = document.querySelector(`[data-category="${currentCategory}"]`);
       if (activeButton) {
           activeButton.classList.add('active');
       }
   } else {
       const allButton = document.querySelector('[data-category="all"]');
       if (allButton) {
           allButton.classList.add('active');
       }
   }
});