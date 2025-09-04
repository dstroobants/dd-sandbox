# frozen_string_literal: true

module Types
  module Api
    class QueryType < Types::BaseObject
      description "The query root of this schema"

      # Example field
      field :hello, String, description: "A simple hello world field"
      def hello
        "Hello GraphQL World!"
      end

      # Example field with arguments
      field :echo, String, description: "Echo back the input message" do
        argument :message, String, required: true, description: "Message to echo"
      end
      def echo(message:)
        "Echo: #{message}"
      end

      # Example field that could query models
      field :current_time, String, description: "Current server time"
      def current_time
        Time.current.iso8601
      end
    end
  end
end
