import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../../contexts/AuthContext';
import Books from '../Books';
import mockAxios from '../../__mocks__/axios';

jest.mock('axios');

const mockBooks = [
  {
    id: '1',
    title: 'Test Book 1',
    author: 'Author 1',
    description: 'Description 1',
    price: 19.99,
  },
  {
    id: '2',
    title: 'Test Book 2',
    author: 'Author 2',
    description: 'Description 2',
    price: 29.99,
  },
];

describe('Books Component', () => {
  beforeEach(() => {
    mockAxios.get.mockResolvedValueOnce({ data: mockBooks });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders books list', async () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Books />
        </AuthProvider>
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Book 1')).toBeInTheDocument();
      expect(screen.getByText('Test Book 2')).toBeInTheDocument();
    });
  });

  it('handles book deletion', async () => {
    mockAxios.delete.mockResolvedValueOnce({ data: {} });

    render(
      <BrowserRouter>
        <AuthProvider>
          <Books />
        </AuthProvider>
      </BrowserRouter>
    );

    await waitFor(() => {
      const deleteButtons = screen.getAllByRole('button', { name: /delete/i });
      fireEvent.click(deleteButtons[0]);
    });

    await waitFor(() => {
      expect(mockAxios.delete).toHaveBeenCalledWith(expect.stringContaining('/books/1'));
    });
  });

  it('handles book creation', async () => {
    const newBook = {
      title: 'New Book',
      author: 'New Author',
      description: 'New Description',
      price: 39.99,
    };

    mockAxios.post.mockResolvedValueOnce({ data: { id: '3', ...newBook } });

    render(
      <BrowserRouter>
        <AuthProvider>
          <Books />
        </AuthProvider>
      </BrowserRouter>
    );

    const addButton = screen.getByRole('button', { name: /add book/i });
    fireEvent.click(addButton);

    const titleInput = screen.getByLabelText(/title/i);
    const authorInput = screen.getByLabelText(/author/i);
    const descriptionInput = screen.getByLabelText(/description/i);
    const priceInput = screen.getByLabelText(/price/i);

    fireEvent.change(titleInput, { target: { value: newBook.title } });
    fireEvent.change(authorInput, { target: { value: newBook.author } });
    fireEvent.change(descriptionInput, { target: { value: newBook.description } });
    fireEvent.change(priceInput, { target: { value: newBook.price } });

    const submitButton = screen.getByRole('button', { name: /submit/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockAxios.post).toHaveBeenCalledWith(
        expect.stringContaining('/books'),
        expect.objectContaining(newBook)
      );
    });
  });
}); 