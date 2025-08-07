FROM php:8.2

RUN apt-get update && apt-get install -y \
    nodejs \
    npm

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

COPY /php-app/. /usr/src/app
WORKDIR /usr/src/app

# Install PHP dependencies
RUN composer install --optimize-autoloader --no-dev

# Install Node dependencies and build frontend assets
RUN npm install && npm run build

# Clean up node_modules to reduce image size
RUN rm -rf node_modules

# Expose port 8000
EXPOSE 8000

# Use artisan serve for production (or switch to Apache/Nginx for better performance)
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]