# https://docs.datadoghq.com/tracing/trace_collection/automatic_instrumentation/dd_libraries/ruby/#graphql
Datadog.configure do |c|
  # Enable tracing
  c.tracing.enabled = true
  
  # Instrument Rails
  c.tracing.instrument :rails, service_name: 'rails-graphql-app'
  
  # Instrument GraphQL with unified tracer
  c.tracing.instrument :graphql, with_unified_tracer: true
end
