import express from 'express';
import cors from 'cors';
import { v4 as uuidv4 } from 'uuid';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

interface User {
  id: string;
  username: string;
  password: string;
  role: 'admin' | 'user';
}

interface Book {
  id: string;
  title: string;
  author: string;
  available: boolean;
}

interface MenuItem {
  id: string;
  name: string;
  price: number;
  category: string;
}

interface Event {
  id: string;
  title: string;
  date: string;
  description: string;
}

interface Order {
  id: string;
  userId: string;
  items: { id: string; quantity: number }[];
  status: 'pending' | 'completed' | 'cancelled';
  createdAt: string;
}

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

// In-memory storage (replace with a database in production)
const users: User[] = [
  {
    id: '1',
    username: 'admin',
    password: 'admin123',
    role: 'admin',
  },
  {
    id: '2',
    username: 'user',
    password: 'user123',
    role: 'user',
  },
];

const books: Book[] = [
  {
    id: '1',
    title: 'The Great Gatsby',
    author: 'F. Scott Fitzgerald',
    available: true,
  },
  {
    id: '2',
    title: '1984',
    author: 'George Orwell',
    available: true,
  },
];

const menuItems: MenuItem[] = [
  {
    id: '1',
    name: 'Classic Cappuccino',
    price: 4.50,
    category: 'Coffee',
  },
  {
    id: '2',
    name: 'Chocolate Croissant',
    price: 3.75,
    category: 'Pastries',
  },
];

const events: Event[] = [
  {
    id: '1',
    title: 'Book Club Meeting',
    date: '2024-03-15T18:00:00',
    description: 'Discussion of The Great Gatsby',
  },
  {
    id: '2',
    title: 'Poetry Reading',
    date: '2024-03-20T19:00:00',
    description: 'Local poets share their work',
  },
];

const orders: Order[] = [];

// Auth endpoints
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  const user = users.find(
    (u) => u.username === username && u.password === password
  );

  if (user) {
    const { password: _, ...userWithoutPassword } = user;
    res.json(userWithoutPassword);
  } else {
    res.status(401).json({ message: 'Invalid credentials' });
  }
});

// User endpoints
app.get('/api/users', (_req, res) => {
  const usersWithoutPasswords = users.map(({ password: _, ...user }) => user);
  res.json(usersWithoutPasswords);
});

app.post('/api/users', (req, res) => {
  const newUser: User = {
    id: uuidv4(),
    ...req.body,
  };
  users.push(newUser);
  const { password: _, ...userWithoutPassword } = newUser;
  res.status(201).json(userWithoutPassword);
});

// Menu endpoints
app.get('/api/menu', (_req, res) => {
  res.json(menuItems);
});

// Books endpoints
app.get('/api/books', (_req, res) => {
  res.json(books);
});

app.post('/api/books/borrow', (req, res) => {
  const { bookId, userId } = req.body;
  const book = books.find((b) => b.id === bookId);
  
  if (!book) {
    return res.status(404).json({ message: 'Book not found' });
  }
  
  if (!book.available) {
    return res.status(400).json({ message: 'Book is not available' });
  }
  
  book.available = false;
  res.json({ message: 'Book borrowed successfully' });
});

// Events endpoints
app.get('/api/events', (_req, res) => {
  res.json(events);
});

app.post('/api/events', (req, res) => {
  const newEvent: Event = {
    id: uuidv4(),
    ...req.body,
  };
  events.push(newEvent);
  res.status(201).json(newEvent);
});

// Orders endpoints
app.get('/api/orders', (_req, res) => {
  res.json(orders);
});

app.post('/api/orders', (req, res) => {
  const newOrder: Order = {
    id: uuidv4(),
    status: 'pending',
    ...req.body,
    createdAt: new Date().toISOString(),
  };
  orders.push(newOrder);
  res.status(201).json(newOrder);
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
}); 