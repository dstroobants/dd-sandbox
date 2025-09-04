# GraphQL Setup for Rails Application

This Rails application has been configured with GraphQL support

## What's Included

### 1. GraphQL Gem
- GraphQL gem version 2.5.11
- GraphQL Batch for efficient data loading
- HTTParty for making GraphQL requests

### 2. Schema Structure
- **ApiSchema**: Main GraphQL schema with Datadog tracing
- **Types::Api::QueryType**: Query operations
- **Types::Api::MutationType**: Mutation operations
- **Analysis modules**: ScopeChecker and LogQueryDepth for query analysis

### 3. GraphiQL Interface
- Available at `http://localhost:3000/` (root path)
- Also accessible at `http://localhost:3000/api/graphiql`
- Web-based GraphQL IDE for testing queries

### 4. Datadog Integration
- GraphQL tracing enabled via `GraphQL::Tracing::DataDogTracing`
- Configurable via `DD_TRACING_STATE` environment variable

## Getting Started

### 1. Install Dependencies
```bash
bundle install
```

### 2. Start the Server
```bash
rails server
```

### 3. Access GraphiQL
Open your browser and go to `http://localhost:3000`

## Sample Queries

### Simple Hello Query
```graphql
query {
  hello
  currentTime
}
```

### Query with Variables
```graphql
query EchoMessage($message: String!) {
  echo(message: $message)
}
```

Variables:
```json
{
  "message": "Hello GraphQL!"
}
```

### Sample Mutation
```graphql
mutation CreateSample($name: String!) {
  createSample(name: $name)
  updateMessage(message: "Sample created")
}
```

Variables:
```json
{
  "name": "Test Sample"
}
```

## Using the GraphQL Client

### In Rails Console
```ruby
client = GraphqlClient.new
result = client.execute_query(GraphqlClient.sample_hello_query)
puts result
```

### Via Rake Tasks
```bash
# Show demo queries
rails graphql:demo

# Test client (requires running server)
rails graphql:test_client
```

## Configuration

### Environment Variables
- `DD_TRACING_STATE=true`: Enable Datadog tracing
- `DD_ENV=ci`: Enable CI mode for Datadog

### Schema Configuration
The schema includes:
- Maximum query depth: 13
- Introspection disabled in production
- Query analyzers for scope checking and depth logging
- GraphQL Batch for efficient data loading

## File Structure

```
app/
├── controllers/
│   └── api/
│       └── graphiql_controller.rb
├── graphql/
│   ├── analysis/
│   │   ├── log_query_depth.rb
│   │   └── scope_checker.rb
│   ├── types/
│   │   ├── api/
│   │   │   ├── mutation_type.rb
│   │   │   └── query_type.rb
│   │   ├── base_*.rb (base types)
│   └── api_schema.rb
├── services/
│   └── graphql_client.rb
└── views/
    └── api/
        └── graphiql/
            └── show.html.erb
```

## Next Steps

1. Add your own GraphQL types for your models
2. Implement authentication if needed
3. Add more complex queries and mutations
4. Set up proper error handling
5. Configure Datadog environment variables for production

## Troubleshooting

- Make sure all gems are installed: `bundle install`
- Check that the server is running on port 3000
- Verify Datadog configuration if tracing isn't working
- Check Rails logs for any GraphQL execution errors
