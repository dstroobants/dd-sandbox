FROM ruby:3.3.8

WORKDIR /usr/src/app

COPY my_rails_app/ .

# Fix Puma configuration to bind to 0.0.0.0 instead of localhost
RUN sed -i 's/port ENV.fetch("PORT", 3000)/#port ENV.fetch("PORT", 3000)\n#https:\/\/github.com\/puma\/puma\/issues\/2113\nbind "tcp:\/\/0.0.0.0:#{ENV[\x27PORT\x27] || 3000}"/' config/puma.rb

RUN gem install rails datadog
RUN bundle install

EXPOSE 3000

CMD ["./bin/rails", "server"]
