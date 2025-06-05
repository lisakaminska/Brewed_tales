import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '../AuthContext';
import mockAxios from '../../__mocks__/axios';

jest.mock('axios');

const TestComponent = () => {
  const { user, login, logout } = useAuth();
  return (
    <div>
      {user ? (
        <>
          <div data-testid="user-info">
            Logged in as: {user.username} (Role: {user.role})
          </div>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <button onClick={() => login('admin', 'admin123')}>Login</button>
      )}
    </div>
  );
};

describe('AuthContext', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('provides authentication state and methods', async () => {
    const mockUser = { id: '1', username: 'admin', role: 'admin' };
    mockAxios.post.mockResolvedValueOnce({ data: mockUser });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    // Initially not logged in
    expect(screen.queryByTestId('user-info')).not.toBeInTheDocument();

    // Perform login
    const loginButton = screen.getByText('Login');
    fireEvent.click(loginButton);

    await waitFor(() => {
      expect(screen.getByTestId('user-info')).toHaveTextContent('Logged in as: admin');
      expect(screen.getByTestId('user-info')).toHaveTextContent('Role: admin');
    });

    // Verify localStorage
    expect(JSON.parse(localStorage.getItem('user') || '')).toEqual(mockUser);

    // Perform logout
    const logoutButton = screen.getByText('Logout');
    fireEvent.click(logoutButton);

    // Verify logged out state
    expect(screen.queryByTestId('user-info')).not.toBeInTheDocument();
    expect(localStorage.getItem('user')).toBeNull();
  });

  it('handles login failure', async () => {
    mockAxios.post.mockRejectedValueOnce(new Error('Invalid credentials'));

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    const loginButton = screen.getByText('Login');
    fireEvent.click(loginButton);

    await waitFor(() => {
      expect(screen.queryByTestId('user-info')).not.toBeInTheDocument();
    });
  });

  it('restores user from localStorage on mount', () => {
    const mockUser = { id: '1', username: 'admin', role: 'admin' };
    localStorage.setItem('user', JSON.stringify(mockUser));

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByTestId('user-info')).toHaveTextContent('Logged in as: admin');
    expect(screen.getByTestId('user-info')).toHaveTextContent('Role: admin');
  });
}); 