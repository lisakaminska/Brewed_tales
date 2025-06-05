# Brewed Tales - Coffee Shop & Library SPA

A Single Page Application (SPA) for a book-themed coffee shop, built with React, TypeScript, and Material-UI.

## Features

- User Authentication (Login/Logout)
- User Management (Admin only)
- Menu Ordering System
- Library Book Management
- Event Booking System
- Order History

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd lab4
```

2. Install dependencies:
```bash
npm install
```

3. Start the development servers:
```bash
npm start
```

This will start both the frontend and backend servers:
- Frontend: http://localhost:8000
- Backend: http://localhost:3000

## Default Users

The application comes with two default users:

1. Admin User
   - Username: admin
   - Password: admin123

2. Regular User
   - Username: user
   - Password: user123

## Project Structure

```
lab4/
├── src/
│   ├── components/      # Reusable components
│   ├── contexts/        # React contexts
│   ├── pages/          # Page components
│   └── App.tsx         # Main application component
├── server/
│   └── server.ts       # Backend server
└── public/             # Static assets
```

## Technologies Used

- React 18
- TypeScript
- Material-UI
- Express.js
- Node.js
- Axios

## Features

### User Management
- User roles (admin/user)
- CRUD operations for users (admin only)
- Protected routes based on user roles

### Menu
- Display menu items by category
- Add items to order
- Place orders

### Library
- Browse available books
- Borrow books
- Track book availability

### Events
- View upcoming events
- Book event attendance
- Add new events (admin only)

### Orders
- View order history
- Track order status
- Calculate order totals

## Browser Support

The application has been tested and works on:
- Google Chrome (latest)
- Mozilla Firefox (latest)
- Microsoft Edge (latest)

## Development

### Code Style

This project follows the Airbnb JavaScript Style Guide with TypeScript extensions. The code style is enforced using ESLint and Prettier.

To run the linter:
```bash
npm run lint
```

### API Endpoints

The backend provides the following REST API endpoints:

- Authentication
  - POST /api/auth/login

- Users
  - GET /api/users
  - POST /api/users
  - PUT /api/users/:id
  - DELETE /api/users/:id

- Menu
  - GET /api/menu

- Books
  - GET /api/books
  - POST /api/books/borrow

- Events
  - GET /api/events
  - POST /api/events

- Orders
  - GET /api/orders
  - POST /api/orders

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

This project is licensed under the MIT License. 