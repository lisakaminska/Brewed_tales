import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  FormControlLabel,
  Checkbox,
} from '@mui/material';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

interface BookFormData {
  title: string;
  author: string;
  genre: string;
  price: string;
  available: boolean;
}

function BookForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const { token } = useAuth();
  const [formError, setFormError] = useState('');
  const [formData, setFormData] = useState<BookFormData>({
    title: '',
    author: '',
    genre: '',
    price: '',
    available: true,
  });

  useEffect(() => {
    const fetchBook = async () => {
      if (id) {
        try {
          const response = await axios.get(`http://localhost:3000/api/books/${id}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          const bookData = response.data;
          setFormData({
            title: bookData.title,
            author: bookData.author,
            genre: bookData.genre,
            price: bookData.price.toString(),
            available: bookData.available,
          });
        } catch (err) {
          console.error('Error fetching book:', err);
          setFormError('Error loading book data');
        }
      }
    };

    fetchBook();
  }, [id, token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const bookData = {
        ...formData,
        price: parseFloat(formData.price),
      };

      if (id) {
        await axios.put(`http://localhost:3000/api/books/${id}`, bookData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        await axios.post('http://localhost:3000/api/books', bookData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      navigate('/books');
    } catch (err) {
      console.error('Error saving book:', err);
      setFormError('Error saving book data');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, checked, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          {id ? 'Edit Book' : 'Add New Book'}
        </Typography>

        {formError && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {formError}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="title"
            label="Title"
            name="title"
            value={formData.title}
            onChange={handleChange}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="author"
            label="Author"
            name="author"
            value={formData.author}
            onChange={handleChange}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="genre"
            label="Genre"
            name="genre"
            value={formData.genre}
            onChange={handleChange}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="price"
            label="Price"
            name="price"
            type="number"
            value={formData.price}
            onChange={handleChange}
            inputProps={{ step: '0.01', min: '0' }}
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={formData.available}
                onChange={handleChange}
                name="available"
              />
            }
            label="Available"
          />
          <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
            >
              {id ? 'Update Book' : 'Add Book'}
            </Button>
            <Button
              fullWidth
              variant="outlined"
              onClick={() => navigate('/books')}
            >
              Cancel
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
}

export default BookForm; 