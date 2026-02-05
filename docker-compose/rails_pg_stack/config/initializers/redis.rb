# frozen_string_literal: true

# Redis configuration
REDIS_URL = ENV.fetch('REDIS_URL', 'redis://localhost:6379/0')

# Configure Redis for Rails cache
Rails.application.config.cache_store = :redis_cache_store, { url: REDIS_URL }

puts "[Redis] Configured with URL: #{REDIS_URL}"
