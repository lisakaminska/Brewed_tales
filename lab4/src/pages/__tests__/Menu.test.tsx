import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../../contexts/AuthContext';
import Menu from '../Menu';
import mockAxios from '../../__mocks__/axios';

jest.mock('axios');

const mockMenuItems = [
  {
    id: '1',
    name: 'Test Item 1',
    description: 'Description 1',
    price: 9.99,
    category: 'Beverages',
  },
  {
    id: '2',
    name: 'Test Item 2',
    description: 'Description 2',
    price: 14.99,
    category: 'Food',
  },
];

describe('Menu Component', () => {
  beforeEach(() => {
    mockAxios.get.mockResolvedValueOnce({ data: mockMenuItems });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders menu items list', async () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Menu />
        </AuthProvider>
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Item 1')).toBeInTheDocument();
      expect(screen.getByText('Test Item 2')).toBeInTheDocument();
      expect(screen.getByText('$9.99')).toBeInTheDocument();
      expect(screen.getByText('$14.99')).toBeInTheDocument();
    });
  });

  it('allows adding items to order', async () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Menu />
        </AuthProvider>
      </BrowserRouter>
    );

    await waitFor(() => {
      const quantityInputs = screen.getAllByLabelText(/quantity/i);
      fireEvent.change(quantityInputs[0], { target: { value: '2' } });
    });

    const placeOrderButton = screen.getByRole('button', { name: /place order/i });
    expect(placeOrderButton).toBeInTheDocument();
  });

  it('displays items by category', async () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Menu />
        </AuthProvider>
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Beverages')).toBeInTheDocument();
      expect(screen.getByText('Food')).toBeInTheDocument();
      expect(screen.getByText('Test Item 1')).toBeInTheDocument();
      expect(screen.getByText('Test Item 2')).toBeInTheDocument();
    });
  });
}); 