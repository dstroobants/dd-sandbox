// DD-Trace is initialized via --require ./tracer.cjs
console.log('Seed script starting - official Prisma + Datadog tracing loaded')

// Import the extended Prisma client with tracing
import { prisma } from './client.js'

async function main() {
  console.log('🌱 Seeding database with sample users...')

  // Check if users already exist
  const existingUsers = await prisma.user.count()
  if (existingUsers > 0) {
    console.log(`📊 Database already has ${existingUsers} users, skipping seed.`)
    return
  }

  // Create sample users
  const sampleUsers = [
    {
      email: 'alice@example.com',
      name: 'Alice Johnson'
    },
    {
      email: 'bob@example.com',
      name: 'Bob Smith'
    },
    {
      email: 'charlie@example.com',
      name: 'Charlie Brown'
    }
  ]

  for (const userData of sampleUsers) {
    const user = await prisma.user.create({
      data: userData
    })
    console.log(`✅ Created user: ${user.name} (${user.email}) with ID ${user.id}`)
  }

  console.log('🎉 Seeding completed successfully!')
}

main()
  .catch((e) => {
    console.error('❌ Error during seeding:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
