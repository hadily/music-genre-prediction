# Use the official PHP Apache image
FROM php:8.0-apache

# Change the Apache configuration to listen on port 82
RUN echo "Listen 82" >> /etc/apache2/ports.conf

# Update the default virtual host to listen on port 82
RUN sed -i 's/80/82/' /etc/apache2/sites-available/000-default.conf

# Set the ServerName to avoid the warning
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Copy your index.html and PHP files to the Apache server
COPY ./index.html /var/www/html/

# Expose port 82
EXPOSE 82