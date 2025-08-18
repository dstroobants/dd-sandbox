import tracer from 'dd-trace';

tracer.init({
  service: "api-testing-prisma",
});

import express from 'express';
import { PrismaClient } from '@prisma/client';

const app = express();
const prisma = new PrismaClient();

// Middleware
app.use(express.json());

// Health check endpoint
app.get('/', async (req, res) => {
  try {
    console.log('Processing request to /');
    
    // Perform a database query to trigger Prisma tracing
    const posts = await prisma.post.findMany({
      take: 5
    });
    
    // Also query users to generate more trace data
    const users = await prisma.user.findMany({
      take: 5
    });
    
    console.log(`Found ${posts.length} posts and ${users.length} users`);
    
    res.json({
      message: 'API is working!',
      timestamp: new Date().toISOString(),
      data: {
        posts: posts.length,
        users: users.length
      }
    });
  } catch (error) {
    console.error('Error in / endpoint:', error);
    res.status(500).json({ 
      error: 'Internal server error',
      message: error.message 
    });
  }
});

// Create a new post
app.post('/posts', async (req, res) => {
  try {
    const { title, content, published = false } = req.body;
    
    const post = await prisma.post.create({
      data: {
        title,
        content,
        published
      }
    });
    
    res.json(post);
  } catch (error) {
    console.error('Error creating post:', error);
    res.status(500).json({ 
      error: 'Failed to create post',
      message: error.message 
    });
  }
});

// Get all posts
app.get('/posts', async (req, res) => {
  try {
    const posts = await prisma.post.findMany({
      orderBy: {
        createdAt: 'desc'
      }
    });
    
    res.json(posts);
  } catch (error) {
    console.error('Error fetching posts:', error);
    res.status(500).json({ 
      error: 'Failed to fetch posts',
      message: error.message 
    });
  }
});

// Create a new user
app.post('/users', async (req, res) => {
  try {
    const { email, name } = req.body;
    
    const user = await prisma.user.create({
      data: {
        email,
        name
      }
    });
    
    res.json(user);
  } catch (error) {
    console.error('Error creating user:', error);
    res.status(500).json({ 
      error: 'Failed to create user',
      message: error.message 
    });
  }
});

// Get all users
app.get('/users', async (req, res) => {
  try {
    const users = await prisma.user.findMany();
    
    res.json(users);
  } catch (error) {
    console.error('Error fetching users:', error);
    res.status(500).json({ 
      error: 'Failed to fetch users',
      message: error.message 
    });
  }
});

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('Shutting down gracefully...');
  await prisma.$disconnect();
  process.exit(0);
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});
