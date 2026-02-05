# frozen_string_literal: true

# Datadog APM configuration

require 'datadog'

Datadog.configure do |c|
  # Basic configuration
  c.service = 'repro-app'
  c.env = ENV.fetch('DD_ENV', 'development')

  # Enable debug logging
  c.diagnostics.debug = ENV.fetch('DD_TRACE_DEBUG', 'false') == 'true'
  c.diagnostics.startup_logs = true

  c.tracing.instrument :pg

  c.tracing.instrument :active_record

  c.tracing.instrument :redis

  # ==========================================================================
  # Other integrations
  # ==========================================================================
  c.tracing.instrument :rack
  c.tracing.instrument :rails
  c.tracing.instrument :faraday
  c.tracing.instrument :aws
  c.tracing.instrument :sidekiq
  c.tracing.instrument :http  # httparty uses net/http
end

puts "[Datadog] Configuration loaded"
puts "[Datadog] PG integration: #{Datadog.configuration.tracing[:pg][:enabled]}"
puts "[Datadog] Redis integration: #{Datadog.configuration.tracing[:redis][:enabled]}"
puts "[Datadog] ActiveRecord integration: #{Datadog.configuration.tracing[:active_record][:enabled]}"
