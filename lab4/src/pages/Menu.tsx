import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  TextField,
  Box,
  Snackbar,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

interface MenuItem {
  id: string;
  name: string;
  price: number;
  category: string;
}

const Menu: React.FC = () => {
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [quantities, setQuantities] = useState<Record<string, number>>({});
  const [orderSuccess, setOrderSuccess] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    const fetchMenuItems = async () => {
      try {
        const response = await axios.get('http://localhost:3000/api/menu');
        setMenuItems(response.data);
      } catch (err) {
        setError('Error loading menu items. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchMenuItems();
  }, []);

  const handleQuantityChange = (itemId: string, value: string) => {
    const quantity = parseInt(value) || 0;
    if (quantity >= 0) {
      setQuantities((prev) => ({
        ...prev,
        [itemId]: quantity,
      }));
    }
  };

  const handleOrder = async () => {
    try {
      const items = Object.entries(quantities)
        .filter(([_, quantity]) => quantity > 0)
        .map(([id, quantity]) => ({ id, quantity }));

      if (items.length === 0) {
        setError('Please select at least one item to order.');
        return;
      }

      await axios.post('http://localhost:3000/api/orders', {
        userId: user?.id,
        items,
      });

      setOrderSuccess(true);
      setQuantities({});
    } catch (err) {
      setError('Error placing order. Please try again later.');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  const categories = Array.from(new Set(menuItems.map((item) => item.category)));

  return (
    <Container>
      <Typography variant="h1" component="h1" gutterBottom sx={{ fontSize: '2.5rem' }}>
        Our Menu
      </Typography>

      {categories.map((category) => (
        <Box key={category} mb={4}>
          <Typography variant="h2" sx={{ fontSize: '2rem', mb: 2 }}>
            {category}
          </Typography>
          <Grid container spacing={3}>
            {menuItems
              .filter((item) => item.category === category)
              .map((item) => (
                <Grid item xs={12} sm={6} md={4} key={item.id}>
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
                        {item.name}
                      </Typography>
                      <Typography variant="body1" color="text.secondary" gutterBottom>
                        ${item.price.toFixed(2)}
                      </Typography>
                    </CardContent>
                    <CardActions sx={{ p: 2, pt: 0 }}>
                      <TextField
                        type="number"
                        label="Quantity"
                        value={quantities[item.id] || ''}
                        onChange={(e) => handleQuantityChange(item.id, e.target.value)}
                        InputProps={{ inputProps: { min: 0 } }}
                        size="small"
                        sx={{ width: 100, mr: 1 }}
                      />
                    </CardActions>
                  </Card>
                </Grid>
              ))}
          </Grid>
        </Box>
      ))}

      <Box sx={{ position: 'sticky', bottom: 16, textAlign: 'right', pb: 2 }}>
        <Button
          variant="contained"
          color="primary"
          size="large"
          onClick={handleOrder}
          disabled={Object.values(quantities).every((q) => !q)}
        >
          Place Order
        </Button>
      </Box>

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
        open={orderSuccess}
        autoHideDuration={6000}
        onClose={() => setOrderSuccess(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert onClose={() => setOrderSuccess(false)} severity="success" sx={{ width: '100%' }}>
          Order placed successfully!
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Menu; 