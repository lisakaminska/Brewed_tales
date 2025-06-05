import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  Snackbar,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

interface BookingFormData {
  eventId: string;
  numberOfPeople: number;
  specialRequests: string;
}

const BookingForm: React.FC = () => {
  const [formData, setFormData] = useState<BookingFormData>({
    eventId: '',
    numberOfPeople: 1,
    specialRequests: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();
  const { user } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await axios.post('http://localhost:3000/api/bookings', {
        ...formData,
        userId: user?.id,
      });

      setSuccess('Booking submitted successfully!');
      setTimeout(() => navigate('/events'), 1500);
    } catch (err) {
      setError('Error submitting booking. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h1" component="h1" gutterBottom sx={{ fontSize: '2.5rem' }}>
        Book Event
      </Typography>

      <Paper sx={{ p: 4 }}>
        <Box component="form" onSubmit={handleSubmit}>
          <FormControl fullWidth margin="normal">
            <InputLabel>Event</InputLabel>
            <Select
              value={formData.eventId}
              onChange={(e) =>
                setFormData((prev) => ({ ...prev, eventId: e.target.value as string }))
              }
              label="Event"
              required
            >
              <MenuItem value="1">Book Club Meeting - March 15, 2024</MenuItem>
              <MenuItem value="2">Poetry Reading - March 20, 2024</MenuItem>
            </Select>
          </FormControl>

          <TextField
            fullWidth
            label="Number of People"
            type="number"
            value={formData.numberOfPeople}
            onChange={(e) =>
              setFormData((prev) => ({
                ...prev,
                numberOfPeople: Math.max(1, parseInt(e.target.value) || 1),
              }))
            }
            margin="normal"
            required
            InputProps={{ inputProps: { min: 1 } }}
          />

          <TextField
            fullWidth
            label="Special Requests"
            value={formData.specialRequests}
            onChange={(e) =>
              setFormData((prev) => ({ ...prev, specialRequests: e.target.value }))
            }
            margin="normal"
            multiline
            rows={4}
          />

          <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
            <Button
              type="button"
              variant="outlined"
              onClick={() => navigate('/events')}
              disabled={loading}
            >
              Cancel
            </Button>
            <Button type="submit" variant="contained" disabled={loading}>
              {loading ? <CircularProgress size={24} /> : 'Submit Booking'}
            </Button>
          </Box>
        </Box>
      </Paper>

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
        open={!!success}
        autoHideDuration={6000}
        onClose={() => setSuccess('')}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert onClose={() => setSuccess('')} severity="success" sx={{ width: '100%' }}>
          {success}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default BookingForm; 