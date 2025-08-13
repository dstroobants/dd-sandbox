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
end
