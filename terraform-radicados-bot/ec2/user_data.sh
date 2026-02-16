#!/bin/bash
set -e

exec > >(tee /var/log/user-data.log)
exec 2>&1

echo "Starting bot setup..."

yum update -y
yum install -y python3 python3-pip git

mkdir -p /opt/radicados-bot
cd /opt/radicados-bot

git clone ${git_repo_url} .
cd radicados-bot

pip3 install -r requirements.txt

cat > .env << 'EOF'
MONGODB_URI=${mongodb_uri}
TELEGRAM_BOT_TOKEN=${telegram_bot_token}
EOF

cat > /etc/systemd/system/radicados-bot.service << 'EOF'
[Unit]
Description=Radicados Telegram Bot
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/radicados-bot/radicados-bot
ExecStart=/usr/bin/python3 src/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

chown -R ec2-user:ec2-user /opt/radicados-bot
chmod 600 /opt/radicados-bot/radicados-bot/.env

systemctl daemon-reload
systemctl enable radicados-bot
systemctl start radicados-bot

echo "Bot setup completed!"
