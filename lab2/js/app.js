class App {
    constructor() {
        this.api = 'http://localhost:3000/api';
        this.init();
    }

    init() {
        this.loadFeaturedItems();
    }

    async loadFeaturedItems() {
        const featuredContent = document.getElementById('featured-content');
        try {
            const response = await fetch(`${this.api}/featured`);
            if (!response.ok) throw new Error('Network response was not ok');
            const items = await response.json();

            featuredContent.innerHTML = items.map(item => `
                <div class="item">
                    <div class="item-image">
                        <img src="${item.image}" alt="${item.name}">
                    </div>
                    <div class="item-content">
                        <h3>${item.name}</h3>
                        <p>${item.description}</p>
                        <p class="price">$${item.price.toFixed(2)}</p>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading featured items:', error);
            featuredContent.innerHTML = '<p>Error loading featured items. Please try again later.</p>';
        }
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new App();
}); 