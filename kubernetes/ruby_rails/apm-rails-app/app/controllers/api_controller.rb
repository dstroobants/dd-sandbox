class ApiController < ApplicationController
  def trigger_request
    ApiRequestJob.perform_later
    render json: { message: "API request job triggered", timestamp: Time.current }
  end

  def status
    render json: { 
      message: "API request scheduler is running", 
      timestamp: Time.current,
      environment: Rails.env,
      api_requests_enabled: Rails.env.production? || ENV['ENABLE_API_REQUESTS'] == 'true'
    }
  end

  def database_health
    begin
      # Simple database connectivity check
      ActiveRecord::Base.connection.execute("SELECT 1")
      render json: { 
        status: "healthy", 
        message: "Database connection successful",
        timestamp: Time.current,
        check_type: "database_connectivity"
      }
    rescue => e
      render json: { 
        status: "unhealthy", 
        message: "Database connection failed: #{e.message}",
        timestamp: Time.current,
        check_type: "database_connectivity"
      }, status: 503
    end
  end

  def services_health
    # Simulate checking various service dependencies
    services_status = {
      redis: check_redis_health,
      external_api: check_external_api_health,
      background_jobs: check_background_jobs_health
    }
    
    all_healthy = services_status.values.all? { |status| status[:healthy] }
    
    render json: {
      status: all_healthy ? "healthy" : "degraded",
      message: "Services health check completed",
      timestamp: Time.current,
      check_type: "services_health",
      services: services_status
    }, status: all_healthy ? 200 : 503
  end

  private

  def check_redis_health
    # Simulate Redis health check
    { healthy: [true, false].sample, response_time: rand(10..50) }
  end

  def check_external_api_health
    # Simulate external API health check
    { healthy: [true, false].sample, response_time: rand(100..300) }
  end

  def check_background_jobs_health
    # Simulate background jobs health check
    { healthy: true, queue_size: rand(0..10) }
  end
end
