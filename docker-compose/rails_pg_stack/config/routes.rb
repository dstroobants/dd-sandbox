# frozen_string_literal: true

Rails.application.routes.draw do
  get '/health', to: 'health#show'
  get '/users', to: 'users#index'
end
