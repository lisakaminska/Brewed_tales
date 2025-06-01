import React from 'react';
import { Container, Grid, Paper, Typography } from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

// Temporary mock data - will be replaced with real API data
const topCustomersData = [
  { name: 'John Doe', orders: 25 },
  { name: 'Jane Smith', orders: 18 },
  { name: 'Bob Johnson', orders: 15 },
  { name: 'Alice Brown', orders: 12 },
];

const popularBooksData = [
  { name: 'The Great Gatsby', value: 30 },
  { name: '1984', value: 25 },
  { name: 'Pride and Prejudice', value: 20 },
  { name: 'To Kill a Mockingbird', value: 15 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

function Dashboard() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Top Customers Chart */}
        <Grid item xs={12} md={6}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 400,
            }}
          >
            <Typography variant="h6" gutterBottom>
              Top Customers
            </Typography>
            <ResponsiveContainer>
              <BarChart
                data={topCustomersData}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="orders" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Popular Books Chart */}
        <Grid item xs={12} md={6}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 400,
            }}
          >
            <Typography variant="h6" gutterBottom>
              Popular Books
            </Typography>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={popularBooksData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                  outerRadius={120}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {popularBooksData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Dashboard; 