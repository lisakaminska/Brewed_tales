const express = require('express');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

interface User {
  id: string;
  username: string;
  email: string;
  role: 'admin' | 'user';
  password: string;
}

// Mock database
let users: User[] = [
  {
    id: '1',
    username: 'admin',
    email: 'admin@brewedtales.com',
    role: 'admin',
    password: 'admin123',
  },
  {
    id: '2',
    username: 'user',
    email: 'user@brewedtales.com',
    role: 'user',
    password: 'user123',
  },
];

// Authentication middleware
const authenticateToken = (req: any, res: any, next: any) => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }

  // In a real application, you would verify the JWT token here
  // For this demo, we'll just check if the token exists
  next();
};

// Login endpoint
app.post('/api/login', (req: any, res: any) => {
  const { username, password } = req.body;
  console.log('Login attempt:', { username, password }); // Add logging
  const user = users.find(u => u.username === username && u.password === password);

  if (!user) {
    console.log('Invalid credentials for username:', username); // Add logging
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // In a real application, you would generate a JWT token here
  const token = 'mock-jwt-token';
  console.log('Login successful for user:', username); // Add logging

  res.json({
    token,
    user: {
      id: user.id,
      username: user.username,
      email: user.email,
      role: user.role,
    },
  });
});

// Get all users (requires authentication)
app.get('/api/users', authenticateToken, (req: any, res: any) => {
  // Don't send passwords to the client
  const safeUsers = users.map(({ password, ...user }) => user);
  res.json(safeUsers);
});

// Get user by ID (requires authentication)
app.get('/api/users/:id', authenticateToken, (req: any, res: any) => {
  const user = users.find(u => u.id === req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  const { password, ...safeUser } = user;
  res.json(safeUser);
});

// Create new user (requires authentication)
app.post('/api/users', authenticateToken, (req: any, res: any) => {
  const { username, email, role, password } = req.body;

  if (users.some(u => u.username === username)) {
    return res.status(400).json({ error: 'Username already exists' });
  }

  const newUser: User = {
    id: uuidv4(),
    username,
    email,
    role,
    password,
  };

  users.push(newUser);
  const { password: removedPassword, ...safeUser } = newUser;
  res.status(201).json(safeUser);
});

// Update user (requires authentication)
app.put('/api/users/:id', authenticateToken, (req: any, res: any) => {
  const { username, email, role, password } = req.body;
  const userIndex = users.findIndex(u => u.id === req.params.id);

  if (userIndex === -1) {
    return res.status(404).json({ error: 'User not found' });
  }

  users[userIndex] = {
    ...users[userIndex],
    username: username || users[userIndex].username,
    email: email || users[userIndex].email,
    role: role || users[userIndex].role,
    password: password || users[userIndex].password,
  };

  const { password: removedPassword, ...safeUser } = users[userIndex];
  res.json(safeUser);
});

// Delete user (requires authentication)
app.delete('/api/users/:id', authenticateToken, (req: any, res: any) => {
  const userIndex = users.findIndex(u => u.id === req.params.id);

  if (userIndex === -1) {
    return res.status(404).json({ error: 'User not found' });
  }

  users = users.filter(u => u.id !== req.params.id);
  res.status(204).send();
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
  console.log('Mock users:', users); // Add logging of initial users
});
