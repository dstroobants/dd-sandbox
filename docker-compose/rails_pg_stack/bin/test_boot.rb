#!/usr/bin/env ruby
# frozen_string_literal: true

# Simple script to test if the Rails application boots successfully
# This will trigger the SystemStackError if the issue is present

puts "=" * 60
puts "Testing Rails boot with Datadog PG integration + Makara"
puts "=" * 60

begin
  require_relative '../config/environment'

  puts "\n[SUCCESS] Rails booted successfully!"
  puts "\nDatadog configuration:"
  puts "  PG integration enabled: #{Datadog.configuration.tracing[:pg][:enabled]}"
  puts "  ActiveRecord integration enabled: #{Datadog.configuration.tracing[:active_record][:enabled]}"

  # Try a simple database query
  puts "\nTesting database connection..."
  result = ActiveRecord::Base.connection.execute('SELECT 1 as test')
  puts "[SUCCESS] Database query executed successfully!"

rescue SystemStackError => e
  puts "\n[FAILURE] SystemStackError occurred!"
  puts "Error: #{e.message}"
  puts "\nBacktrace (first 20 lines):"
  e.backtrace.first(20).each { |line| puts "  #{line}" }
  puts "  ... (#{e.backtrace.length - 20} more lines)"
  exit 1

rescue => e
  puts "\n[ERROR] An error occurred: #{e.class}"
  puts "Error: #{e.message}"
  puts "\nBacktrace:"
  e.backtrace.first(10).each { |line| puts "  #{line}" }
  exit 1
end
