class MenuPage {
    constructor() {
        this.api = 'http://localhost:3000/api';
        this.currentCategory = 'all';
        this.init();
    }

    init() {
        this.setupFilterButtons();
        this.loadMenuItems();
    }

    setupFilterButtons() {
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Update active button
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');

                // Update category and reload items
                this.currentCategory = button.dataset.category;
                this.loadMenuItems();
            });
        });
    }

    async loadMenuItems() {
        const menuContent = document.getElementById('menu-content');
        try {
            const url = this.currentCategory === 'all' 
                ? `${this.api}/menu`
                : `${this.api}/menu?category=${this.currentCategory}`;

            const response = await fetch(url);
            if (!response.ok) throw new Error('Network response was not ok');
            const items = await response.json();

            menuContent.innerHTML = items.map(item => `
                <div class="menu-item">
                    <div class="item-image">
                        <img src="${item.image}" alt="${item.name}">
                    </div>
                    <div class="item-content">
                        <h3>${item.name}</h3>
                        <p>${item.description}</p>
                        <p class="price">$${item.price.toFixed(2)}</p>
                        <p class="category">${item.category}</p>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading menu items:', error);
            menuContent.innerHTML = '<p>Error loading menu items. Please try again later.</p>';
        }
    }
}

// Initialize the menu page when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MenuPage();
}); 