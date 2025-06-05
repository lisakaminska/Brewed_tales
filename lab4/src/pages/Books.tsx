import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  Snackbar,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

interface Book {
  id: string;
  title: string;
  author: string;
  available: boolean;
}

const Books: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [borrowSuccess, setBorrowSuccess] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axios.get('http://localhost:3000/api/books');
        setBooks(response.data);
      } catch (err) {
        setError('Error loading books. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchBooks();
  }, []);

  const handleBorrow = async (bookId: string) => {
    try {
      await axios.post('http://localhost:3000/api/books/borrow', {
        bookId,
        userId: user?.id,
      });

      setBooks((prevBooks) =>
        prevBooks.map((book) =>
          book.id === bookId ? { ...book, available: false } : book
        )
      );
      setBorrowSuccess(true);
    } catch (err) {
      setError('Error borrowing book. Please try again later.');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container>
      <Typography variant="h1" component="h1" gutterBottom sx={{ fontSize: '2.5rem' }}>
        Library
      </Typography>

      <Grid container spacing={3}>
        {books.map((book) => (
          <Grid item xs={12} sm={6} md={4} key={book.id}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  transition: 'transform 0.2s ease-in-out',
                },
              }}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h3" component="div" sx={{ fontSize: '1.5rem', mb: 1 }}>
                  {book.title}
                </Typography>
                <Typography variant="body1" color="text.secondary" gutterBottom>
                  by {book.author}
                </Typography>
                <Typography
                  variant="body2"
                  color={book.available ? 'success.main' : 'error.main'}
                  sx={{ mt: 2 }}
                >
                  {book.available ? 'Available' : 'Currently Borrowed'}
                </Typography>
              </CardContent>
              <CardActions sx={{ p: 2, pt: 0 }}>
                <Button
                  variant="contained"
                  color="primary"
                  disabled={!book.available}
                  onClick={() => handleBorrow(book.id)}
                  fullWidth
                >
                  {book.available ? 'Borrow' : 'Not Available'}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError('')}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert onClose={() => setError('')} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>

      <Snackbar
        open={borrowSuccess}
        autoHideDuration={6000}
        onClose={() => setBorrowSuccess(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert onClose={() => setBorrowSuccess(false)} severity="success" sx={{ width: '100%' }}>
          Book borrowed successfully!
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Books; 