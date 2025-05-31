class BooksPage {
    constructor() {
        this.api = 'http://localhost:3000/api';
        this.currentGenre = 'all';
        this.init();
    }

    init() {
        this.setupFilterButtons();
        this.loadBooks();
    }

    setupFilterButtons() {
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Update active button
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');

                // Update genre and reload books
                this.currentGenre = button.dataset.genre;
                this.loadBooks();
            });
        });
    }

    async loadBooks() {
        const booksContent = document.getElementById('books-content');
        try {
            const url = this.currentGenre === 'all'
                ? `${this.api}/books`
                : `${this.api}/books?genre=${encodeURIComponent(this.currentGenre)}`;

            const response = await fetch(url);
            if (!response.ok) throw new Error('Network response was not ok');
            const books = await response.json();

            booksContent.innerHTML = books.map(book => `
                <div class="book">
                    <div class="book-image">
                        <img src="${book.image}" alt="${book.title}">
                    </div>
                    <div class="book-content">
                        <h3>${book.title}</h3>
                        <p class="author">By ${book.author}</p>
                        <p>${book.description}</p>
                        <p class="genre">${book.genre}</p>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading books:', error);
            booksContent.innerHTML = '<p>Error loading books. Please try again later.</p>';
        }
    }
}

// Initialize the books page when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BooksPage();
}); 