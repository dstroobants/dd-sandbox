# frozen_string_literal: true

module Types
  module Api
    class MutationType < Types::BaseObject
      description "The mutation root of this schema"

      # Example mutation
      field :update_message, String, description: "Update a message" do
        argument :message, String, required: true, description: "New message"
      end
      def update_message(message:)
        "Updated message: #{message}"
      end

      # Example mutation that could interact with models
      field :create_sample, String, description: "Create a sample record" do
        argument :name, String, required: true, description: "Name for the sample"
      end
      def create_sample(name:)
        "Created sample with name: #{name}"
      end
    end
  end
end
