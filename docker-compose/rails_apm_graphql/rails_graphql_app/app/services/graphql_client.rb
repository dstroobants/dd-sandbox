# frozen_string_literal: true

# Simple GraphQL client service for making requests
class GraphqlClient
  include HTTParty
  
  def initialize(base_url = nil)
    @base_url = base_url || 'http://localhost:3000'
  end

  def execute_query(query, variables: {}, operation_name: nil)
    response = self.class.post(
      "#{@base_url}/api/graphiql",
      body: {
        query: query,
        variables: variables.to_json,
        operationName: operation_name
      }.to_json,
      headers: {
        'Content-Type' => 'application/json',
        'Accept' => 'application/json'
      }
    )
    
    JSON.parse(response.body)
  rescue => e
    { "errors" => [{ "message" => e.message }] }
  end

  # Sample queries
  def self.sample_hello_query
    <<~GRAPHQL
      query {
        hello
        currentTime
      }
    GRAPHQL
  end

  def self.sample_echo_query(message = "Hello GraphQL!")
    {
      query: <<~GRAPHQL,
        query EchoMessage($message: String!) {
          echo(message: $message)
        }
      GRAPHQL
      variables: { message: message }
    }
  end

  def self.sample_mutation
    {
      query: <<~GRAPHQL,
        mutation CreateSample($name: String!) {
          createSample(name: $name)
          updateMessage(message: "Sample created")
        }
      GRAPHQL
      variables: { name: "Test Sample" }
    }
  end
end
