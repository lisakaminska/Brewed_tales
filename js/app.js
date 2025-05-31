class App {
    constructor() {
        this.api = 'http://localhost:3000/api';
        this.init();
    }

    init() {
        // Load all content sections
        this.loadFeaturedItems();
        this.loadMenu();
        this.loadBooks();
    }

    async loadFeaturedItems() {
        const featuredContent = document.getElementById('featured-content');
        try {
            const response = await fetch(`${this.api}/featured`);
            if (!response.ok) throw new Error('Network response was not ok');
            const items = await response.json();

            featuredContent.innerHTML = items.map(item => `
                <div class="item">
                    <h3>${item.name}</h3>
                    <p>${item.description}</p>
                    <p class="price">$${item.price}</p>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading featured items:', error);
            featuredContent.innerHTML = '<p>Error loading featured items. Please try again later.</p>';
        }
    }

    async loadMenu() {
        const menuContent = document.getElementById('menu-content');
        try {
            const response = await fetch(`${this.api}/menu`);
            if (!response.ok) throw new Error('Network response was not ok');
            const items = await response.json();

            menuContent.innerHTML = items.map(item => `
                <div class="menu-item">
                    <h3>${item.name}</h3>
                    <p>${item.description}</p>
                    <p class="price">$${item.price}</p>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading menu:', error);
            menuContent.innerHTML = '<p>Error loading menu. Please try again later.</p>';
        }
    }

    async loadBooks() {
        const booksContent = document.getElementById('books-content');
        try {
            const response = await fetch(`${this.api}/books`);
            if (!response.ok) throw new Error('Network response was not ok');
            const books = await response.json();

            booksContent.innerHTML = books.map(book => `
                <div class="book">
                    <h3>${book.title}</h3>
                    <p>Author: ${book.author}</p>
                    <p>${book.description}</p>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading books:', error);
            booksContent.innerHTML = '<p>Error loading books. Please try again later.</p>';
        }
    }
}

// Initialize the application when the DOM is loaded
const app = new App(); 