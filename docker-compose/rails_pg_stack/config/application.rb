# frozen_string_literal: true

require_relative 'boot'

require 'rails'
require 'active_model/railtie'
require 'active_record/railtie'
require 'action_controller/railtie'

# Require the gems listed in Gemfile
Bundler.require(*Rails.groups)

module ReproApp
  class Application < Rails::Application
    config.load_defaults 7.0

    # Don't generate system test files
    config.generators.system_tests = nil

    # Minimal configuration
    config.api_only = true
    config.eager_load = false
  end
end
