Rails.application.config.after_initialize do
  # Start the recurring API request job when the application boots
  if ENV['ENABLE_API_REQUESTS'] == 'true'
    Rails.logger.info "🚀 Starting API request scheduler..."
    
    # Start the recurring job in a background thread to avoid blocking app startup
    Thread.new do
      # Wait a bit for the app to fully initialize
      sleep 2
      
      Rails.logger.info "🔄 Starting recurring API requests every 5 seconds..."
      
      loop do
        begin
          # Execute the API request job
          ApiRequestJob.perform_now
        rescue => e
          Rails.logger.error "💥 Error in API request scheduler: #{e.class} - #{e.message}"
        end
        
        # Wait 5 seconds before next execution
        sleep 5
      end
    end
    
  else
    Rails.logger.info "⏸️  API request scheduler disabled (set ENABLE_API_REQUESTS=true to enable)"
  end
end
