# SingleA_Armageddon_Lab2_final
Lab 2 — EC2 Startup Script (User Data Automation)
Objective
This lab introduces Linux automation and cloud initialization by writing a startup script that configures an EC2 instance to host a front-facing static website.

Script Logic Explanation
The startup.sh script automates the complete configuration of a web server through five sequential steps that execute automatically when the EC2 instance launches:
1. System Update (yum update -y)
Updates all installed packages to their latest versions, ensuring security patches are applied before installing new software. The -y flag auto-confirms all prompts.
2. Install Apache (yum install -y httpd)
Installs the Apache web server package (httpd) which handles HTTP requests and serves web content on port 80.
3. Start Apache (systemctl start httpd)
Starts the Apache service immediately so it begins listening for incoming web traffic.
4. Enable Auto-Start (systemctl enable httpd)
Creates a symlink that ensures Apache starts automatically if the instance reboots, maintaining uptime without manual intervention.
5. Create HTML Page (cat <<'EOF' > /var/www/html/index.html)
Uses a heredoc to write a complete HTML file with inline CSS directly to Apache's web root directory. The single quotes around EOF prevent variable interpolation, ensuring the HTML is written exactly as specified.
6. Set Permissions (chmod 644)
Applies standard file permissions (owner read/write, others read-only) so Apache can serve the file securely.