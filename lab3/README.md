# Brewed Tales - Lab 3

A single-page application for managing users in the Brewed Tales coffee shop system. Built with React, TypeScript, and Material-UI.

## Features

- User authentication (login/logout)
- User roles (admin/user)
- User management (CRUD operations)
- Responsive design
- Modern UI with Material-UI components
- TypeScript for type safety
- ESLint with Airbnb configuration

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd lab3
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
- Admin user:
  - Username: admin
  - Password: admin123
- Regular user:
  - Username: user
  - Password: user123

## Project Structure

```
lab3/
├── src/
│   ├── components/     # Reusable UI components
│   ├── contexts/       # React contexts
│   ├── pages/         # Page components
│   └── App.tsx        # Main application component
├── server/
│   └── server.ts      # Express backend server
└── package.json       # Project dependencies and scripts
```

## Browser Support

The application is tested and supported in:
- Google Chrome (latest)
- Mozilla Firefox (latest)
- Microsoft Edge (latest)

## Development

- Run `npm run lint` to check for linting errors
- The application uses ESLint with Airbnb TypeScript configuration
- All components follow the single responsibility principle
- Code is organized into small, focused functions and components
