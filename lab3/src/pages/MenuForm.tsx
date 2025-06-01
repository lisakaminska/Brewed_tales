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
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  SelectChangeEvent,
} from '@mui/material';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

interface MenuItemFormData {
  name: string;
  category: string;
  description: string;
  price: string;
  available: boolean;
}

const categories = [
  'Coffee',
  'Tea',
  'Pastries',
  'Sandwiches',
  'Desserts',
  'Beverages',
];

function MenuForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const { token } = useAuth();
  const [formError, setFormError] = useState('');
  const [formData, setFormData] = useState<MenuItemFormData>({
    name: '',
    category: '',
    description: '',
    price: '',
    available: true,
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSelectChange = (e: SelectChangeEvent) => {
    setFormData((prev) => ({
      ...prev,
      category: e.target.value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const menuData = {
        ...formData,
        price: parseFloat(formData.price),
      };

      if (id) {
        await axios.put(`http://localhost:3000/api/menu/${id}`, menuData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        await axios.post('http://localhost:3000/api/menu', menuData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      navigate('/menu');
    } catch (err) {
      console.error('Error saving menu item:', err);
      setFormError('Error saving menu item data');
    }
  };

  useEffect(() => {
    const fetchMenuItem = async () => {
      if (id) {
        try {
          const response = await axios.get(`http://localhost:3000/api/menu/${id}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          const menuData = response.data;
          setFormData({
            name: menuData.name,
            category: menuData.category,
            description: menuData.description,
            price: menuData.price.toString(),
            available: menuData.available,
          });
        } catch (err) {
          console.error('Error fetching menu item:', err);
          setFormError('Error loading menu item data');
        }
      }
    };

    fetchMenuItem();
  }, [id, token]);

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          {id ? 'Edit Menu Item' : 'Add New Menu Item'}
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
            id="name"
            label="Name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
          />
          <FormControl fullWidth margin="normal">
            <InputLabel id="category-label">Category</InputLabel>
            <Select
              labelId="category-label"
              id="category"
              name="category"
              value={formData.category}
              label="Category"
              onChange={handleSelectChange}
              required
            >
              {categories.map((category) => (
                <MenuItem key={category} value={category}>
                  {category}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            margin="normal"
            required
            fullWidth
            id="description"
            label="Description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            multiline
            rows={3}
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
            onChange={handleInputChange}
            inputProps={{ step: '0.01', min: '0' }}
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={formData.available}
                onChange={handleInputChange}
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
              {id ? 'Update Item' : 'Add Item'}
            </Button>
            <Button
              fullWidth
              variant="outlined"
              onClick={() => navigate('/menu')}
            >
              Cancel
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
}

export default MenuForm;
