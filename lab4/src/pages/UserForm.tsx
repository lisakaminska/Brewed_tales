import React, { useState, useEffect } from 'react';
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
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

interface UserFormData {
  username: string;
  password: string;
  role: 'admin' | 'user';
}

const UserForm: React.FC = () => {
  const [formData, setFormData] = useState<UserFormData>({
    username: '',
    password: '',
    role: 'user',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { user: currentUser } = useAuth();
  const isEdit = !!id;

  useEffect(() => {
    if (currentUser?.role !== 'admin') {
      navigate('/');
      return;
    }

    if (isEdit) {
      const fetchUser = async () => {
        try {
          const response = await axios.get(`http://localhost:3000/api/users/${id}`);
          const { password: _, ...userData } = response.data;
          setFormData((prev) => ({ ...prev, ...userData }));
        } catch (err) {
          setError('Error loading user data. Please try again later.');
          navigate('/users');
        }
      };

      fetchUser();
    }
  }, [currentUser, id, isEdit, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isEdit) {
        await axios.put(`http://localhost:3000/api/users/${id}`, formData);
      } else {
        await axios.post('http://localhost:3000/api/users', formData);
      }

      setSuccess('User saved successfully!');
      setTimeout(() => navigate('/users'), 1500);
    } catch (err) {
      setError('Error saving user. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h1" component="h1" gutterBottom sx={{ fontSize: '2.5rem' }}>
        {isEdit ? 'Edit User' : 'Add User'}
      </Typography>

      <Paper sx={{ p: 4 }}>
        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Username"
            value={formData.username}
            onChange={(e) => setFormData((prev) => ({ ...prev, username: e.target.value }))}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Password"
            type="password"
            value={formData.password}
            onChange={(e) => setFormData((prev) => ({ ...prev, password: e.target.value }))}
            margin="normal"
            required={!isEdit}
            helperText={isEdit ? 'Leave blank to keep current password' : ''}
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Role</InputLabel>
            <Select
              value={formData.role}
              onChange={(e) =>
                setFormData((prev) => ({ ...prev, role: e.target.value as 'admin' | 'user' }))
              }
              label="Role"
              required
            >
              <MenuItem value="user">User</MenuItem>
              <MenuItem value="admin">Admin</MenuItem>
            </Select>
          </FormControl>

          <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
            <Button
              type="button"
              variant="outlined"
              onClick={() => navigate('/users')}
              disabled={loading}
            >
              Cancel
            </Button>
            <Button type="submit" variant="contained" disabled={loading}>
              {loading ? <CircularProgress size={24} /> : isEdit ? 'Save Changes' : 'Add User'}
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

export default UserForm; 