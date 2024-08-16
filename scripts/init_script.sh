#!/bin/bash

# Update the system
yum update -y

# Install Python 3 and pip
yum install -y python3 python3-pip

# Install git
yum install -y git

# Clone the repository (replace with your actual repository URL)
git clone https://github.com/your-username/your-repo-name.git /home/ec2-user/app

# Change to the application directory
cd /home/ec2-user/app

# Install the required Python packages
pip3 install -r requirements.txt

# Set environment variables (replace with your actual database credentials)
export DB_HOST=your-rds-endpoint.rds.amazonaws.com
export DB_USER=your-db-username
export DB_PASSWORD=your-db-password
export DB_NAME=your-db-name

# Start the Flask application
python3 src/app/__init__.py > /home/ec2-user/app.log 2>&1 &

# Set up a cron job to start the application on reboot
(crontab -l 2>/dev/null; echo "@reboot /home/ec2-user/app/scripts/start_app.sh") | crontab -

# Create a start_app.sh script
cat << EOF > /home/ec2-user/app/scripts/start_app.sh
#!/bin/bash
cd /home/ec2-user/app
export DB_HOST=your-rds-endpoint.rds.amazonaws.com
export DB_USER=your-db-username
export DB_PASSWORD=your-db-password
export DB_NAME=your-db-name
python3 src/app/__init__.py > /home/ec2-user/app.log 2>&1 &
EOF

# Make the start_app.sh script executable
chmod +x /home/ec2-user/app/scripts/start_app.sh