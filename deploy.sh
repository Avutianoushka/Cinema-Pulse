#!/bin/bash
# =============================================================================
# CINEMAPULSE - AWS EC2 DEPLOYMENT SCRIPT
# =============================================================================
# 
# PREREQUISITES:
# 1. EC2 instance running Amazon Linux 2 or Ubuntu 22.04
# 2. Security Group allowing ports: 22, 80, 5000, 3306
# 3. RDS MySQL instance created and accessible
# 4. SSH key pair configured
#
# USAGE:
# 1. SSH into your EC2 instance
# 2. Clone your project repository
# 3. Run: chmod +x deploy.sh && ./deploy.sh
# =============================================================================
echo "=========================================="
echo "CinemaPulse - AWS Deployment Script"
echo "=========================================="
# Update system packages
echo "[1/8] Updating system packages..."
sudo yum update -y 2>/dev/null || sudo apt update -y

# Install Python 3 and pip
echo "[2/8] Installing Python 3..."
sudo yum install python3 python3-pip -y 2>/dev/null || sudo apt install python3 python3-pip python3-venv -y

# Install Git (if not installed)
echo "[3/8] Installing Git..."
sudo yum install git -y 2>/dev/null || sudo apt install git -y

# Create application directory
echo "[4/8] Setting up application directory..."
sudo mkdir -p /opt/cinemapulse
sudo chown $USER:$USER /opt/cinemapulse
# Create virtual environment
echo "[5/8] Creating virtual environment..."
cd /opt/cinemapulse
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "[6/8] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create environment variables file
echo "[7/8] Setting up environment variables..."
cat > /opt/cinemapulse/.env << 'EOF'
# =============================================================================
# CINEMAPULSE ENVIRONMENT CONFIGURATION
# =============================================================================
# IMPORTANT: Update these values with your actual AWS RDS credentials
# =============================================================================

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this-in-production

# AWS RDS MySQL Configuration
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=your-secure-password
DB_NAME=cinemapulse

# Server Configuration
HOST=0.0.0.0
PORT=5000
EOF

echo "⚠️  IMPORTANT: Edit /opt/cinemapulse/.env with your actual credentials!"

# Create systemd service
echo "[8/8] Creating systemd service..."
sudo tee /etc/systemd/system/cinemapulse.service > /dev/null << 'EOF'
[Unit]
Description=CinemaPulse Flask Application
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/opt/cinemapulse
Environment="PATH=/opt/cinemapulse/venv/bin"
EnvironmentFile=/opt/cinemapulse/.env
ExecStart=/opt/cinemapulse/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable cinemapulse
sudo systemctl start cinemapulse

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Edit /opt/cinemapulse/.env with your RDS credentials"
echo "2. Run: sudo systemctl restart cinemapulse"
echo "3. Access: http://YOUR-EC2-PUBLIC-IP:5000"
echo ""
echo "Useful Commands:"
echo "  - Check status: sudo systemctl status cinemapulse"
echo "  - View logs: sudo journalctl -u cinemapulse -f"
echo "  - Restart: sudo systemctl restart cinemapulse"
echo "=========================================="
