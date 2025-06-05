import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AuthProvider } from './contexts/AuthContext';
import PrivateRoute from './components/PrivateRoute';
import Layout from './components/Layout';
import Login from './pages/Login';
import UserList from './pages/UserList';
import UserForm from './pages/UserForm';
import Menu from './pages/Menu';
import Books from './pages/Books';
import Events from './pages/Events';
import Orders from './pages/Orders';
import BookingForm from './pages/BookingForm';

const theme = createTheme({
  palette: {
    primary: {
      main: '#4A3728', // Coffee brown
    },
    secondary: {
      main: '#8B5E3C', // Warm brown
    },
    background: {
      default: '#FAF3E0', // Cream color
      paper: '#FFFFFF',
    },
  },
  typography: {
    fontFamily: "'Open Sans', 'Helvetica', 'Arial', sans-serif",
    h1: {
      fontFamily: "'Merriweather', serif",
      fontWeight: 700,
    },
    h2: {
      fontFamily: "'Merriweather', serif",
      fontWeight: 700,
    },
    h3: {
      fontFamily: "'Merriweather', serif",
      fontWeight: 700,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          padding: '8px 24px',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={
              <PrivateRoute>
                <Layout />
              </PrivateRoute>
            }>
              <Route index element={<Navigate to="/menu" replace />} />
              <Route path="users" element={<UserList />} />
              <Route path="users/new" element={<UserForm />} />
              <Route path="users/:id" element={<UserForm />} />
              <Route path="menu" element={<Menu />} />
              <Route path="books" element={<Books />} />
              <Route path="events" element={<Events />} />
              <Route path="orders" element={<Orders />} />
              <Route path="booking" element={<BookingForm />} />
            </Route>
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App; 