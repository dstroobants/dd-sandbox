# frozen_string_literal: true

namespace :graphql do
  desc "Demo GraphQL queries"
  task demo: :environment do
    puts "🚀 Running GraphQL Demo Queries"
    puts "=" * 50

    # Note: These would work if the server is running
    # For demo purposes, we'll show what the queries would look like

    puts "\n1. Simple Hello Query:"
    puts GraphqlClient.sample_hello_query

    puts "\n2. Echo Query with Variables:"
    echo_query = GraphqlClient.sample_echo_query("Hello from Rails!")
    puts "Query: #{echo_query[:query]}"
    puts "Variables: #{echo_query[:variables]}"

    puts "\n3. Sample Mutation:"
    mutation = GraphqlClient.sample_mutation
    puts "Mutation: #{mutation[:query]}"
    puts "Variables: #{mutation[:variables]}"

    puts "\n" + "=" * 50
    puts "🎯 To test these queries:"
    puts "1. Start the Rails server: rails server"
    puts "2. Visit http://localhost:3000 for GraphiQL interface"
    puts "3. Copy and paste the queries above"
    puts "4. Or use the GraphqlClient service in Rails console"
    puts "\nExample in Rails console:"
    puts "client = GraphqlClient.new"
    puts "result = client.execute_query(GraphqlClient.sample_hello_query)"
    puts "puts result"
  end

  desc "Test GraphQL client (requires running server)"
  task test_client: :environment do
    puts "🧪 Testing GraphQL Client"
    puts "=" * 30

    client = GraphqlClient.new('http://localhost:3000')
    
    # Test simple query
    puts "\n1. Testing Hello Query:"
    result = client.execute_query(GraphqlClient.sample_hello_query)
    puts result

    # Test query with variables
    puts "\n2. Testing Echo Query:"
    echo_query = GraphqlClient.sample_echo_query("Hello from Rake task!")
    result = client.execute_query(echo_query[:query], variables: echo_query[:variables])
    puts result

    # Test mutation
    puts "\n3. Testing Mutation:"
    mutation = GraphqlClient.sample_mutation
    result = client.execute_query(mutation[:query], variables: mutation[:variables])
    puts result

    puts "\n✅ GraphQL Client Test Complete"
  rescue => e
    puts "❌ Error: #{e.message}"
    puts "Make sure the Rails server is running on localhost:3000"
  end
end
