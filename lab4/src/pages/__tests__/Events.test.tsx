import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../../contexts/AuthContext';
import Events from '../Events';
import mockAxios from '../../__mocks__/axios';

jest.mock('axios');

const mockEvents = [
  {
    id: '1',
    title: 'Test Event 1',
    description: 'Description 1',
    date: '2024-03-20T18:00:00.000Z',
    capacity: 50,
  },
  {
    id: '2',
    title: 'Test Event 2',
    description: 'Description 2',
    date: '2024-03-21T19:00:00.000Z',
    capacity: 30,
  },
];

describe('Events Component', () => {
  beforeEach(() => {
    mockAxios.get.mockResolvedValueOnce({ data: mockEvents });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders events list', async () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Events />
        </AuthProvider>
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Event 1')).toBeInTheDocument();
      expect(screen.getByText('Test Event 2')).toBeInTheDocument();
      expect(screen.getByText('Description 1')).toBeInTheDocument();
      expect(screen.getByText('Description 2')).toBeInTheDocument();
    });
  });

  it('displays event details', async () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Events />
        </AuthProvider>
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Event 1')).toBeInTheDocument();
      expect(screen.getByText('Description 1')).toBeInTheDocument();
      expect(screen.getByText('March 20, 2024 8:00 PM')).toBeInTheDocument();
    });
  });

  it('allows event registration', async () => {
    mockAxios.post.mockResolvedValueOnce({ data: { message: 'Registration successful' } });

    render(
      <BrowserRouter>
        <AuthProvider>
          <Events />
        </AuthProvider>
      </BrowserRouter>
    );

    await waitFor(() => {
      const registerButtons = screen.getAllByRole('button', { name: /register/i });
      fireEvent.click(registerButtons[0]);
    });

    await waitFor(() => {
      expect(mockAxios.post).toHaveBeenCalledWith(
        'http://localhost:3000/api/events/1/register',
        expect.any(Object)
      );
    });
  });
}); 