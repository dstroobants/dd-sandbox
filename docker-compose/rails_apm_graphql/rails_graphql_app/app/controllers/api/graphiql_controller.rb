# frozen_string_literal: true

module Api
  class GraphiqlController < ApplicationController
    # Simplified version for development/demo purposes
    # Remove authentication for easier testing
    skip_before_action :verify_authenticity_token, only: [:execute]

    def execute
      variables = ensure_hash(params[:variables])
      query = params[:query]
      operation_name = params[:operationName]

      # Simplified context for demo
      context = {
        # Query context goes here
        api_mode: true,
        graphiql: true
      }

      result = ApiSchema.execute(query, variables: variables, context: context, operation_name: operation_name)
      render json: result
    rescue => e # rubocop:disable Style/RescueStandardError
      handle_error_in_development e
    end

    # GraphiQL interface page
    def show
      # This will render the GraphiQL interface
    end

    private

    # Handle form data, JSON body, or a blank value
    def ensure_hash(ambiguous_param)
      case ambiguous_param
      when String
        if ambiguous_param.present?
          ensure_hash(JSON.parse(ambiguous_param))
        else
          {}
        end
      when Hash, ActionController::Parameters
        ambiguous_param
      when nil
        {}
      else
        raise ArgumentError, "Unexpected parameter: #{ambiguous_param}"
      end
    end

    def handle_error_in_development(e) # rubocop:disable Naming/MethodParameterName
      logger.error e.message
      logger.error e.backtrace.join("\n")

      render json: { error: { message: e.message, backtrace: e.backtrace }, data: {} }, status: 500
    end
  end
end
