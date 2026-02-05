Datadog.configure do |c|
  c.tracing.instrument :sidekiq, quantize: { args: { show: :all } }
  c.dynamic_instrumentation.enabled = true
  c.profiling.enabled = true

  c.tracing.sampling.rules = '[
    {"service": "minelist-sidekiq", "resource": "sidekiq.*", "sample_rate": 0.01},
    {"service": "minelist-sidekiq", "sample_rate": 1.0},
    {"sample_rate": 1.0}
  ]'
  
  #agent_settings = Datadog::Core::Configuration::AgentSettingsResolver.call(c)
  #
  #c.tracing.writer = Datadog::Tracing::SyncWriter.new(
  #  agent_settings: agent_settings,
  #  transport: Datadog::Tracing::Transport::HTTP.default(
  #    agent_settings: agent_settings
  #  ) do |t|
  #    t.adapter :test  # No-op adapter, doesn't send to agent
  #  end
  #)
end
