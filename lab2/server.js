const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());
app.use('/static', express.static('lab2/static'));

// Mock data
const mockData = {
    featured: [
        {
            id: 1,
            name: 'Cappuccino',
            description: 'Rich espresso with steamed milk and foam',
            price: 4.99,
            image: '/static/images/cappuccino.jpg',
            category: 'drinks'
        },
        {
            id: 2,
            name: 'Classic Novel Collection',
            description: 'Set of 3 classic novels in hardcover',
            price: 29.99,
            image: '/static/images/classic-books.jpg',
            category: 'books'
        },
        {
            id: 3,
            name: 'Book Club Special',
            description: 'Coffee and pastry with book rental',
            price: 12.99,
            image: '/static/images/book-club.jpg',
            category: 'special'
        }
    ],
    menu: [
        {
            id: 1,
            name: 'Espresso',
            description: 'Single shot of pure espresso',
            price: 2.99,
            image: '/static/images/espresso.jpg',
            category: 'drinks'
        },
        {
            id: 2,
            name: 'Latte',
            description: 'Espresso with steamed milk and light foam',
            price: 4.49,
            image: '/static/images/latte.jpg',
            category: 'drinks'
        },
        {
            id: 3,
            name: 'Croissant',
            description: 'Freshly baked butter croissant',
            price: 3.49,
            image: '/static/images/croissant.jpg',
            category: 'food'
        },
        {
            id: 4,
            name: 'Chocolate Muffin',
            description: 'Rich chocolate muffin with chocolate chips',
            price: 3.99,
            image: '/static/images/muffin.jpg',
            category: 'food'
        }
    ],
    books: [
        {
            id: 1,
            title: 'Pride and Prejudice',
            author: 'Jane Austen',
            description: 'A classic romance novel about love and social class',
            image: '/static/images/pride-prejudice.jpg',
            genre: 'Classic Romance'
        },
        {
            id: 2,
            title: '1984',
            author: 'George Orwell',
            description: 'A dystopian masterpiece about surveillance and control',
            image: '/static/images/1984.jpg',
            genre: 'Dystopian Fiction'
        },
        {
            id: 3,
            title: 'The Great Gatsby',
            author: 'F. Scott Fitzgerald',
            description: 'American classic about wealth and the American Dream',
            image: '/static/images/gatsby.jpg',
            genre: 'Classic Fiction'
        }
    ]
};

// API endpoints
app.get('/api/featured', (req, res) => {
    res.json(mockData.featured);
});

app.get('/api/menu', (req, res) => {
    const { category } = req.query;
    let items = mockData.menu;
    if (category) {
        items = items.filter(item => item.category === category);
    }
    res.json(items);
});

app.get('/api/books', (req, res) => {
    const { genre } = req.query;
    let books = mockData.books;
    if (genre) {
        books = books.filter(book => book.genre === genre);
    }
    res.json(books);
});

app.get('/api/menu/:id', (req, res) => {
    const item = mockData.menu.find(i => i.id === parseInt(req.params.id));
    if (item) {
        res.json(item);
    } else {
        res.status(404).json({ error: 'Item not found' });
    }
});

app.get('/api/books/:id', (req, res) => {
    const book = mockData.books.find(b => b.id === parseInt(req.params.id));
    if (book) {
        res.json(book);
    } else {
        res.status(404).json({ error: 'Book not found' });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
}); 