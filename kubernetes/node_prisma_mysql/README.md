# Get all users
curl http://your-service/users

# Get user by ID
curl http://your-service/users/1

# Create a new user
curl -X POST http://your-service/users \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "Test User"}'
