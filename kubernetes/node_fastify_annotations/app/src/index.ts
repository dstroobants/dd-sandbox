import fastify from 'fastify'

const server = fastify()

server.get('/', async (request, reply) => {
  console.log('error')
  throw new Error('test error')
})

server.listen({ port: 3590, host: '0.0.0.0' }, (err, address) => {
  if (err) {
    console.error(err)
    process.exit(1)
  }
  console.log(`Server listening at ${address}`)
})
