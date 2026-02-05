# frozen_string_literal: true

# Active Record Query Trace configuration

if defined?(ActiveRecordQueryTrace)
  ActiveRecordQueryTrace.enabled = true
  ActiveRecordQueryTrace.level = :app # :full, :rails, :app
  ActiveRecordQueryTrace.lines = 5
  ActiveRecordQueryTrace.colorize = false # Disable in production

  puts "[ActiveRecordQueryTrace] Enabled"
end
