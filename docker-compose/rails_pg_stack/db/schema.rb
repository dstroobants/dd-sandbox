# frozen_string_literal: true

# This file is auto-generated from the current state of the database.
ActiveRecord::Schema[7.0].define(version: 2024_01_01_000000) do
  enable_extension 'plpgsql'

  create_table 'users', force: :cascade do |t|
    t.string 'name', null: false
    t.string 'email', null: false
    t.datetime 'created_at', null: false
    t.datetime 'updated_at', null: false
    t.index ['email'], name: 'index_users_on_email', unique: true
  end
end
