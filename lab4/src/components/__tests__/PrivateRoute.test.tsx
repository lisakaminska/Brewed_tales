import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from '../../contexts/AuthContext';
import PrivateRoute from '../PrivateRoute';

const TestComponent = () => <div>Protected Content</div>;

describe('PrivateRoute', () => {
  it('redirects to login when not authenticated', () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/" element={
              <PrivateRoute>
                <TestComponent />
              </PrivateRoute>
            } />
            <Route path="/login" element={<div>Login Page</div>} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    );

    expect(screen.getByText('Login Page')).toBeInTheDocument();
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
  });

  it('renders protected content when authenticated', async () => {
    // Mock the auth context to simulate an authenticated user
    const mockAuthContext = {
      user: { id: '1', username: 'admin', role: 'admin' },
      login: jest.fn(),
      logout: jest.fn(),
    };

    jest.spyOn(React, 'useContext').mockImplementation(() => mockAuthContext);

    render(
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/" element={
              <PrivateRoute>
                <TestComponent />
              </PrivateRoute>
            } />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    );

    expect(screen.getByText('Protected Content')).toBeInTheDocument();
  });
}); 