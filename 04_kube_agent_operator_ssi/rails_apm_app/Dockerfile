FROM ruby:3.4.2

WORKDIR /usr/src/app

COPY apm-rails-app/ .

RUN gem install rails
RUN bundle install

EXPOSE 3000

CMD ["./bin/rails", "server"]
