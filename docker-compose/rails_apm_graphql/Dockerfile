FROM ruby:3.4.4

WORKDIR /usr/src/app

COPY rails_graphql_app/ .

RUN gem install rails --version 7.2.2.1
RUN bundle install

CMD ["./bin/rails", "server", "-b", "0.0.0.0"]
