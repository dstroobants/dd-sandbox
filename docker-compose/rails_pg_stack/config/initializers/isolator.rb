# frozen_string_literal: true

# Isolator configuration

if defined?(Isolator)
  Isolator.configure do |config|
    # Raise errors in development/test
    config.raise_exceptions = !Rails.env.production?

    # Log violations
    config.logger = Rails.logger
  end

  puts "[Isolator] Configured"
end
