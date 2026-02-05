# frozen_string_literal: true

class UsersController < ApplicationController
  def index
    # This query will trigger PG instrumentation
    @users = User.all
    render json: @users
  end
end
