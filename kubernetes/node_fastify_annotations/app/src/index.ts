import fastify from 'fastify'

const server = fastify()

server.get('/', async (request, reply) => {
  return 'hello\n'
})

server.listen({ port: 3590, host: '0.0.0.0' }, (err, address) => {
  if (err) {
    console.error(err)
    process.exit(1)
  }
  console.log(`Server listening at ${address}`)
})
