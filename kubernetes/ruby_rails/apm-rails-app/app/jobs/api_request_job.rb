class ApiRequestJob < ApplicationJob
  queue_as :default

  def perform
    begin
      # Make HTTP request to a public API (Chuck Norris API for demo)
      uri = URI('https://api.chucknorris.io/jokes/random')
      http = Net::HTTP.new(uri.host, uri.port)
      http.use_ssl = true
      http.read_timeout = 5
      http.open_timeout = 5

      Rails.logger.info "📡 Making API request to #{uri.host}..."
      response = http.get(uri)
      
      if response.code == '200'
        data = JSON.parse(response.body)
        Rails.logger.info "✅ API Request Success: #{data['value']}"
      else
        Rails.logger.warn "⚠️  API Request Failed: HTTP #{response.code} - #{response.message}"
      end
      
    rescue Net::TimeoutError => e
      Rails.logger.error "⏰ API Request Timeout: #{e.message}"
    rescue StandardError => e
      Rails.logger.error "❌ API Request Error: #{e.class} - #{e.message}"
    end
  end
end
