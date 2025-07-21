require 'sinatra/base'
require 'logger'

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

puts "Starting Sinatra server on 0.0.0.0:4567..."
App.run!