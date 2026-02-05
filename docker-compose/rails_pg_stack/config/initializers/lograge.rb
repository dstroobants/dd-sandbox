# frozen_string_literal: true

# Lograge configuration

Rails.application.configure do
  config.lograge.enabled = true
  config.lograge.formatter = Lograge::Formatters::Json.new

  config.lograge.custom_options = lambda do |event|
    {
      time: Time.current.iso8601,
      host: Socket.gethostname
    }
  end
end

puts "[Lograge] Enabled"
