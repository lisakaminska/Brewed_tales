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
import BookList from './pages/BookList';
import BookForm from './pages/BookForm';
import MenuList from './pages/MenuList';
import MenuForm from './pages/MenuForm';
import Dashboard from './pages/Dashboard';

const theme = createTheme({
  palette: {
    primary: {
      main: '#4A3728',
    },
    secondary: {
      main: '#8B5E3C',
    },
    background: {
      default: '#FAF3E0',
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
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="users" element={<UserList />} />
              <Route path="users/new" element={<UserForm />} />
              <Route path="users/:id" element={<UserForm />} />
              <Route path="books" element={<BookList />} />
              <Route path="books/new" element={<BookForm />} />
              <Route path="books/:id" element={<BookForm />} />
              <Route path="menu" element={<MenuList />} />
              <Route path="menu/new" element={<MenuForm />} />
              <Route path="menu/:id" element={<MenuForm />} />
            </Route>
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
