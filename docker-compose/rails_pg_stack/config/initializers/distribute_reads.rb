# frozen_string_literal: true

# Distribute Reads configuration

DistributeReads.default_options = {
  # Fallback to primary if replicas are unavailable
  failover: true,
  # Fallback to primary if replica lag exceeds threshold
  lag_failover: true
}

puts "[DistributeReads] Configuration loaded"
