// DD-Trace is initialized via --require ./tracer.cjs
// This ensures it loads before any other modules

console.log('Application starting - Prisma + Datadog tracing loaded')

// Import other dependencies AFTER tracer initialization
import express from 'express'

// Import the extended Prisma client with tracing
import { prisma } from './client.js'

console.log('Using official Prisma client with Datadog extensions')

// Create Express app
const app = express()
const PORT = 3000

// Middleware for parsing JSON
app.use(express.json())

// Prisma client is imported from client.js with tracing extensions
console.log('Prisma client with Datadog tracing ready')

// Basic logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`)
  next()
})

// Root route
app.get('/', async (req, res) => {
  res.json({ hello: 'world', status: 'API is running' })
})

// Get all users
app.get('/users', async (req, res) => {
  try {
    const users = await prisma.user.findMany({
      orderBy: {
        createdAt: 'desc'
      }
    })
    res.json({ users, count: users.length })
  } catch (error) {
    console.error('Error fetching users:', error)
    res.status(500).json({ error: 'Failed to fetch users' })
  }
})

// Get user by ID
app.get('/users/:id', async (req, res) => {
  try {
    const { id } = req.params
    const user = await prisma.user.findUnique({
      where: {
        id: parseInt(id)
      }
    })
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' })
    }
    
    res.json({ user })
  } catch (error) {
    console.error('Error fetching user:', error)
    res.status(500).json({ error: 'Failed to fetch user' })
  }
})

// Create a new user
app.post('/users', async (req, res) => {
  try {
    const { email, name } = req.body
    
    if (!email) {
      return res.status(400).json({ error: 'Email is required' })
    }
    
    const user = await prisma.user.create({
      data: {
        email,
        name: name || null
      }
    })
    
    res.status(201).json({ user })
  } catch (error) {
    console.error('Error creating user:', error)
    if (error.code === 'P2002') {
      res.status(400).json({ error: 'Email already exists' })
    } else {
      res.status(500).json({ error: 'Failed to create user' })
    }
  }
})

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err)
  res.status(500).json({ error: 'Internal server error' })
})

// Graceful shutdown
const gracefulShutdown = async (signal) => {
  console.log(`Received ${signal}. Starting graceful shutdown...`)
  
  try {
    await prisma.$disconnect()
    console.log('Prisma disconnected successfully')
    process.exit(0)
  } catch (error) {
    console.error('Error during shutdown:', error)
    process.exit(1)
  }
}

process.on('SIGINT', () => gracefulShutdown('SIGINT'))
process.on('SIGTERM', () => gracefulShutdown('SIGTERM'))

// Start the server
app.listen(PORT, '0.0.0.0', (err) => {
  if (err) {
    console.error('Failed to start server:', err)
    process.exit(1)
  }
  console.log(`Server started successfully on port ${PORT}`)
})
