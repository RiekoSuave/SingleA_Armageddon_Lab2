The startup script automates EC2 server setup using Bash scripting.
When the instance launches, the script installs Apache,
starts the web server, enables it on boot, and automatically
creates a custom HTML webpage inside /var/www/html.

This allows the website to become publicly accessible without
manual server configuration.