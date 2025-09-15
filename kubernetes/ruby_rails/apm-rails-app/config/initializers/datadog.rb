Datadog.configure do |c|
  c.tracing.instrument :sidekiq, quantize: { args: { show: :all } }
  c.dynamic_instrumentation.enabled = true
  c.profiling.enabled = true

  c.tracing.sampling.rules = '[
    {"service": "minelist-sidekiq", "resource": "sidekiq.*", "sample_rate": 0.01},
    {"service": "minelist-sidekiq", "sample_rate": 1.0},
    {"sample_rate": 1.0}
  ]'
end
