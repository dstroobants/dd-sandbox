# frozen_string_literal: true

module Types
  class BaseConnection < Types::BaseObject
    # add `nodes` and `pageInfo` fields, as well as `edge_type(...)` override
    include GraphQL::Types::Relay::ConnectionBehaviors
  end
end
