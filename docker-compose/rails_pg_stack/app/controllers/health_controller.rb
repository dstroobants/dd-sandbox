# frozen_string_literal: true

class HealthController < ApplicationController
  def show
    # Simple health check that triggers a database query
    ActiveRecord::Base.connection.execute('SELECT 1')
    render json: { status: 'ok' }
  end
end
