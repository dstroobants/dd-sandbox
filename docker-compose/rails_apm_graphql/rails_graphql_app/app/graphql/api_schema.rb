# frozen_string_literal: true

class ApiSchema < GraphQL::Schema
  disable_introspection_entry_points if Rails.env.production?
  max_depth 13

  query_analyzer Analysis::ScopeChecker
  query_analyzer Analysis::LogQueryDepth

  mutation(Types::Api::MutationType)
  query(Types::Api::QueryType)

  use GraphQL::Batch

  # GraphQL tracing is handled by Datadog's unified tracer in the initializer
end
