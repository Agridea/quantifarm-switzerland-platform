FROM php:8.2.35-apache

# Install required PHP extensions
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Harden Apache: deny access to dotfiles (.env), SQL dumps, compose files, etc.
# Placed outside the docroot so the bind mount in docker-compose.yml cannot override it.
COPY apache-security.conf /etc/apache2/conf-enabled/zz-security.conf

# Copy application files
COPY . /var/www/html/

# Set working directory
WORKDIR /var/www/html

# Set proper permissions
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

# Expose port 80
EXPOSE 80
