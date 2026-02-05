FROM ruby:3.2.2

WORKDIR /app

# Install dependencies
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy Gemfile first for better caching
COPY Gemfile Gemfile.lock* ./
RUN bundle install

# Copy the rest of the application
COPY . .

# Make bin files executable
RUN chmod +x bin/*

EXPOSE 3000

CMD ["bundle", "exec", "puma", "-C", "config/puma.rb"]
