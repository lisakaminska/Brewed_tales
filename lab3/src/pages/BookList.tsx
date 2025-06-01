import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Typography,
  IconButton,
  Box,
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

interface Book {
  id: string;
  title: string;
  author: string;
  genre: string;
  price: number;
  available: boolean;
}

function BookList() {
  const [books, setBooks] = useState<Book[]>([]);
  const navigate = useNavigate();
  const { token } = useAuth();

  const fetchBooks = async () => {
    try {
      const response = await axios.get('http://localhost:3000/api/books', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setBooks(response.data);
    } catch (error) {
      console.error('Error fetching books:', error);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, [token]);

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this book?')) {
      try {
        await axios.delete(`http://localhost:3000/api/books/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        fetchBooks();
      } catch (error) {
        console.error('Error deleting book:', error);
      }
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1" gutterBottom>
          Books
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/books/new')}
        >
          Add New Book
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Author</TableCell>
              <TableCell>Genre</TableCell>
              <TableCell>Price</TableCell>
              <TableCell>Available</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {books.map((book) => (
              <TableRow key={book.id}>
                <TableCell>{book.title}</TableCell>
                <TableCell>{book.author}</TableCell>
                <TableCell>{book.genre}</TableCell>
                <TableCell>${book.price.toFixed(2)}</TableCell>
                <TableCell>{book.available ? 'Yes' : 'No'}</TableCell>
                <TableCell>
                  <IconButton
                    color="primary"
                    onClick={() => navigate(`/books/${book.id}`)}
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    color="error"
                    onClick={() => handleDelete(book.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
}

export default BookList; 