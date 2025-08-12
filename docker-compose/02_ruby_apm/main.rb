require 'sinatra/base'
require 'logger'
require 'net/http'
require 'uri'

require 'datadog/auto_instrument'

Datadog.configure do |c|
  #c.diagnostics.debug = true
end

class App < Sinatra::Base
  set :bind, '0.0.0.0'
  set :port, 4567

  @@logger = Logger.new(STDOUT)
  @@logger.progname = 'apm-ruby-test'
  @@logger.formatter = proc do |severity, datetime, progname, msg|
    "[#{datetime}][#{progname}][#{severity}][#{Datadog::Tracing.log_correlation}] #{msg}\n"
  end

  get '/' do
    @@logger.info "Navigated to root /"
    'Hello world!'
  end

  get '/log' do
    @@logger.warn('Navigated to the log endpoint /log')
    'Log Endpoint!'
  end
end

API_ENDPOINTS = [
  'https://api.chucknorris.io/jokes/random',
  'https://www.boredapi.com/api/activity',
  'https://dog.ceo/api/breeds/image/random'
]

Thread.new do
  loop do
    begin
      url = URI(API_ENDPOINTS.sample)
      Datadog::Tracing.trace('background.api.poll', resource: url.host, service: 'apm-ruby-test') do |span|
        span.set_tag('component', 'poller')
        span.set_tag('http.method', 'GET')
        span.set_tag('http.url', url.to_s)

        response = Net::HTTP.get_response(url)
        span.set_tag('http.status_code', response.code)

        body = response.body || ''
        preview = body[0, 160]
        App.class_variable_get(:@@logger).info("Polled #{url} status=#{response.code} bytes=#{body.bytesize} body=#{preview}")
      end
    rescue => e
      App.class_variable_get(:@@logger).error("Poller error: #{e.class}: #{e.message}")
    ensure
      sleep 5
    end
  end
end

puts "Starting Sinatra server on 0.0.0.0:4567..."
App.run!