import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Alert,
  Snackbar,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import { format } from 'date-fns';

interface OrderItem {
  id: string;
  quantity: number;
  name?: string;
  price?: number;
}

interface Order {
  id: string;
  userId: string;
  items: OrderItem[];
  status: 'pending' | 'completed' | 'cancelled';
  createdAt: string;
  total?: number;
}

const Orders: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const [ordersResponse, menuResponse] = await Promise.all([
          axios.get('http://localhost:3000/api/orders'),
          axios.get('http://localhost:3000/api/menu'),
        ]);

        const menuItems = menuResponse.data;
        const ordersWithDetails = ordersResponse.data.map((order: Order) => ({
          ...order,
          items: order.items.map((item) => {
            const menuItem = menuItems.find((m: any) => m.id === item.id);
            return {
              ...item,
              name: menuItem?.name || 'Unknown Item',
              price: menuItem?.price || 0,
            };
          }),
          total: order.items.reduce((sum, item) => {
            const menuItem = menuItems.find((m: any) => m.id === item.id);
            return sum + (menuItem?.price || 0) * item.quantity;
          }, 0),
        }));

        setOrders(
          user?.role === 'admin'
            ? ordersWithDetails
            : ordersWithDetails.filter((order: Order) => order.userId === user?.id)
        );
      } catch (err) {
        setError('Error loading orders. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [user]);

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
        {user?.role === 'admin' ? 'All Orders' : 'My Orders'}
      </Typography>

      {orders.length === 0 ? (
        <Alert severity="info">No orders found.</Alert>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Order ID</TableCell>
                <TableCell>Date</TableCell>
                <TableCell>Items</TableCell>
                <TableCell align="right">Total</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {orders.map((order) => (
                <TableRow key={order.id}>
                  <TableCell component="th" scope="row">
                    {order.id.slice(0, 8)}
                  </TableCell>
                  <TableCell>
                    {format(new Date(order.createdAt), 'MMM d, yyyy h:mm a')}
                  </TableCell>
                  <TableCell>
                    <Box>
                      {order.items.map((item, index) => (
                        <Typography key={index} variant="body2" gutterBottom>
                          {item.quantity}x {item.name} (${item.price?.toFixed(2)})
                        </Typography>
                      ))}
                    </Box>
                  </TableCell>
                  <TableCell align="right">${order.total?.toFixed(2)}</TableCell>
                  <TableCell>
                    <Chip
                      label={order.status}
                      color={
                        order.status === 'completed'
                          ? 'success'
                          : order.status === 'cancelled'
                          ? 'error'
                          : 'warning'
                      }
                      size="small"
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

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
    </Container>
  );
};

export default Orders; 