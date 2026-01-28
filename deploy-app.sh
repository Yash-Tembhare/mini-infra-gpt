#!/bin/bash
set -e

echo "🚀 Deploying Flask App to AWS EC2"
echo "=================================="
echo ""

# Get IP
PUBLIC_IP=$(terraform -chdir=generated-terraform output -raw instance_public_ip)



echo "📡 Target Server: $PUBLIC_IP"
echo ""

# Copy app to server
echo "📤 Uploading application..."
scp -i mini-infra-gpt-key.pem -o StrictHostKeyChecking=no \
    app.py ec2-user@$PUBLIC_IP:/home/ec2-user/

# Install and run
echo ""
echo "🔧 Installing Flask and starting app..."
ssh -i mini-infra-gpt-key.pem -o StrictHostKeyChecking=no \
    ec2-user@$PUBLIC_IP << 'EOF'
# Install Flask
sudo pip3 install flask

# Stop any existing app
sudo pkill -f "python3 app.py" || true

# Start app in background
nohup sudo python3 /home/ec2-user/app.py > /home/ec2-user/app.log 2>&1 &

# Wait a moment
sleep 3

# Check if running
if pgrep -f "python3 app.py" > /dev/null; then
    echo "✅ App is running!"
else
    echo "❌ App failed to start. Check logs:"
    cat /home/ec2-user/app.log
fi
EOF

echo ""
echo "=================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=================================="
echo ""
echo "🌐 Your app is live at:"
echo "   http://$PUBLIC_IP"
echo ""
echo "📊 Check logs:"
echo "   ssh -i mini-infra-gpt-key.pem ec2-user@$PUBLIC_IP"
echo "   tail -f app.log"
echo ""
