import React from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Container,
  Box,
  Paper,
  Grid,
  IconButton,
  useTheme,
} from '@mui/material';
import {
  Menu as MenuIcon,
  ExitToApp as LogoutIcon,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

const Layout: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  const navItems = [
    { label: 'Menu', path: '/menu' },
    { label: 'Books', path: '/books' },
    { label: 'Events', path: '/events' },
    { label: 'Orders', path: '/orders' },
    ...(user?.role === 'admin' ? [{ label: 'Users', path: '/users' }] : []),
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static" color="primary">
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h1"
            component="div"
            sx={{
              flexGrow: 1,
              fontSize: '1.5rem',
              fontFamily: "'Merriweather', serif",
            }}
          >
            Brewed Tales
          </Typography>
          <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
            {navItems.map((item) => (
              <Button
                key={item.path}
                color="inherit"
                onClick={() => navigate(item.path)}
                sx={{
                  mx: 1,
                  fontWeight: location.pathname === item.path ? 'bold' : 'normal',
                  borderBottom:
                    location.pathname === item.path
                      ? `2px solid ${theme.palette.secondary.main}`
                      : 'none',
                }}
              >
                {item.label}
              </Button>
            ))}
          </Box>
          <IconButton color="inherit" onClick={handleLogout} sx={{ ml: 2 }}>
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container component="main" sx={{ flex: 1, py: 4 }}>
        <Outlet />
      </Container>

      <Paper component="footer" sx={{ mt: 'auto', py: 4, bgcolor: 'primary.main', color: 'white' }}>
        <Container>
          <Grid container spacing={4}>
            <Grid item xs={12} sm={4}>
              <Typography variant="h6" gutterBottom>
                Hours
              </Typography>
              <Typography variant="body2">
                Monday - Friday: 7am - 10pm
                <br />
                Saturday - Sunday: 8am - 11pm
              </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Typography variant="h6" gutterBottom>
                Contact
              </Typography>
              <Typography variant="body2" component="address">
                123 Book Street
                <br />
                Phone: (555) 123-4567
                <br />
                Email: info@brewedtales.com
              </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Typography variant="h6" gutterBottom>
                Follow Us
              </Typography>
              <Box>
                <Button color="inherit" size="small">
                  Facebook
                </Button>
                <Button color="inherit" size="small">
                  Instagram
                </Button>
                <Button color="inherit" size="small">
                  Twitter
                </Button>
              </Box>
            </Grid>
          </Grid>
          <Typography
            variant="body2"
            align="center"
            sx={{ mt: 4, borderTop: '1px solid rgba(255,255,255,0.1)', pt: 2 }}
          >
            © {new Date().getFullYear()} Brewed Tales. All rights reserved.
          </Typography>
        </Container>
      </Paper>
    </Box>
  );
};

export default Layout; 