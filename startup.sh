#!/bin/bash

# Update system packages
yum update -y

# Install Apache web server
yum install -y httpd

# Start Apache
systemctl start httpd

# Enable Apache on boot
systemctl enable httpd

# Create custom webpage
cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Rieko's Lab2</title>

    <style>
        body {
            background-color: lightblue;
            font-family: Arial;
            text-align: center;
        }

        .section {
            background-color: white;
            margin: 20px;
            padding: 20px;
            border-radius: 10px;
        }

        img {
            width: 300px;
            border-radius: 10px;
        }
    </style>
</head>

<body>

    <h1>Welcome to Rieko's EC2 Website</h1>

    <img src="https://picsum.photos/300" alt="Random Image">

    <div class="section">
        <h2>About Me</h2>
        <p>
            My name is Rieko and I am learning cloud computing,
            Linux, Git, and AWS infrastructure automation.
        </p>
    </div>

    <div class="section">
        <h2>Project Description</h2>
        <p>
            This website was automatically deployed using an EC2
            User Data startup script written in Bash.
        </p>
    </div>

    <div class="section">
        <h2>Contact</h2>
        <p>
            Rieko Suave; riekosuave01@gmail.com
        </p>
    </div>

</body>
</html>
EOF