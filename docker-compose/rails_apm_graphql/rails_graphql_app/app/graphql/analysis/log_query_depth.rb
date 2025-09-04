# frozen_string_literal: true

module Analysis
  class LogQueryDepth < GraphQL::Analysis::AST::Analyzer
    def initialize(query)
      super
      @max_depth = 0
      @current_depth = 0
    end

    def on_enter_field(node, parent, visitor)
      @current_depth += 1
      @max_depth = [@max_depth, @current_depth].max
    end

    def on_leave_field(node, parent, visitor)
      @current_depth -= 1
    end

    def result
      Rails.logger.info "GraphQL Query Depth: #{@max_depth}"
      { max_depth: @max_depth }
    end
  end
end
