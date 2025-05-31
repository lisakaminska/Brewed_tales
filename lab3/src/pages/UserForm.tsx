import React, { useState, useEffect, ChangeEvent } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Alert,
  SelectChangeEvent,
} from '@mui/material';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

interface UserFormData {
  username: string;
  email: string;
  role: 'admin' | 'user';
  password: string;
}

function UserForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const { token } = useAuth();
  const [formError, setFormError] = useState('');
  const [formData, setFormData] = useState<UserFormData>({
    username: '',
    email: '',
    role: 'user',
    password: '',
  });

  useEffect(() => {
    const fetchUser = async () => {
      if (id) {
        try {
          const response = await axios.get(`http://localhost:3000/api/users/${id}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          const { password, ...userData } = response.data;
          setFormData({ ...userData, password: '' });
        } catch (err) {
          console.error('Error fetching user:', err);
          setFormError('Error loading user data');
        }
      }
    };

    fetchUser();
  }, [id, token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (id) {
        await axios.put(`http://localhost:3000/api/users/${id}`, formData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        await axios.post('http://localhost:3000/api/users', formData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      navigate('/users');
    } catch (err) {
      console.error('Error saving user:', err);
      setFormError('Error saving user data');
    }
  };

  const handleTextChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleRoleChange = (e: SelectChangeEvent) => {
    setFormData(prev => ({
      ...prev,
      role: e.target.value as 'admin' | 'user',
    }));
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          {id ? 'Edit User' : 'Create User'}
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
            id="username"
            label="Username"
            name="username"
            value={formData.username}
            onChange={handleTextChange}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleTextChange}
          />
          <FormControl fullWidth margin="normal">
            <InputLabel id="role-label">Role</InputLabel>
            <Select
              labelId="role-label"
              id="role"
              name="role"
              value={formData.role}
              label="Role"
              onChange={handleRoleChange}
            >
              <MenuItem value="user">User</MenuItem>
              <MenuItem value="admin">Admin</MenuItem>
            </Select>
          </FormControl>
          <TextField
            margin="normal"
            fullWidth
            id="password"
            label={id ? 'New Password (leave blank to keep current)' : 'Password'}
            name="password"
            type="password"
            value={formData.password}
            onChange={handleTextChange}
            required={!id}
          />
          <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
            >
              {id ? 'Update' : 'Create'}
            </Button>
            <Button
              fullWidth
              variant="outlined"
              onClick={() => navigate('/users')}
            >
              Cancel
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
}

export default UserForm; 