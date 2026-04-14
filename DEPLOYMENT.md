# SecureCloud Deployment Guide

Complete guide for deploying the Secure File Storage Platform with MySQL backend.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Platform Deployment](#cloud-platform-deployment)
6. [Blockchain Configuration (Optional)](#blockchain-configuration-optional)
7. [Environment Variables](#environment-variables)
8. [Security Checklist](#security-checklist)

---

## Prerequisites

### Required Software
- **Python 3.8+** (Python 3.10+ recommended)
- **MySQL 5.7+** or **MySQL 8.0+**
- **pip** (Python package manager)

### Optional
- **Docker** and **Docker Compose** (for containerized deployment)
- **Nginx** or **Apache** (for reverse proxy)
- **Gunicorn** or **uWSGI** (for production WSGI server)

---

## Local Development Setup

### 1. Clone and Navigate
```bash
cd cloudbased_filestoragedataencryption-main
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Database

#### Option A: Using Existing MySQL
```sql
CREATE DATABASE secure_storage CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'secure_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON secure_storage.* TO 'secure_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Option B: Run Schema Script
```bash
mysql -u root -p < mysql_schema.sql
```

### 5. Configure Environment Variables

Create `.env.mysql` file in the project root:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=secure_user
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=secure_storage

# File Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=104857600

# Optional: Blockchain Configuration (see Blockchain section)
# BLOCKCHAIN_RPC_URL=
# BLOCKCHAIN_CONTRACT_ADDRESS=
# BLOCKCHAIN_PRIVATE_KEY=
# BLOCKCHAIN_CHAIN_ID=
```

**⚠️ Important**: Generate a strong SECRET_KEY:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6. Initialize Database
```bash
python -c "from app_mysql import app, db; app.app_context().push(); db.create_all()"
```

### 7. Run Application
```bash
python run_mysql.py
```

Or directly:
```bash
python app_mysql.py
```

Access at: `http://localhost:5000`

---

## Production Deployment

### Option 1: VPS/Server Deployment (Ubuntu/Debian)

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and MySQL
sudo apt install python3 python3-pip python3-venv mysql-server nginx -y

# Install MySQL client libraries
sudo apt install default-libmysqlclient-dev build-essential -y
```

#### 2. Setup MySQL
```bash
sudo mysql_secure_installation
sudo mysql -u root -p
```

```sql
CREATE DATABASE secure_storage CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'secure_user'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT ALL PRIVILEGES ON secure_storage.* TO 'secure_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 3. Deploy Application
```bash
# Create app directory
sudo mkdir -p /var/www/securecloud
sudo chown $USER:$USER /var/www/securecloud

# Clone/copy your project
cd /var/www/securecloud
# (copy your project files here)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env.mysql (use production values)
nano .env.mysql
```

#### 4. Setup Gunicorn
Create `/etc/systemd/system/securecloud.service`:
```ini
[Unit]
Description=SecureCloud Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/securecloud
Environment="PATH=/var/www/securecloud/venv/bin"
ExecStart=/var/www/securecloud/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/securecloud/securecloud.sock \
    --timeout 120 \
    app_mysql:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start securecloud
sudo systemctl enable securecloud
```

#### 5. Setup Nginx Reverse Proxy
Create `/etc/nginx/sites-available/securecloud`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 100M;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/securecloud/securecloud.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/securecloud/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        alias /var/www/securecloud/uploads;
        internal;  # Only allow internal access
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/securecloud /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. Setup SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

### Option 2: Docker Deployment

#### 1. Create Dockerfile
Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application
COPY . .

# Create uploads directory
RUN mkdir -p uploads uploads/profile_pics

# Set environment variables
ENV FLASK_APP=app_mysql.py
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "120", "app_mysql:app"]
```

#### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - MYSQL_HOST=db
      - MYSQL_USER=secure_user
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_DATABASE=secure_storage
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./.env.mysql:/app/.env.mysql
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=secure_storage
      - MYSQL_USER=secure_user
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./mysql_schema.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./static:/usr/share/nginx/html/static
    depends_on:
      - web
    restart: unless-stopped

volumes:
  mysql_data:
```

#### 3. Build and Run
```bash
docker-compose up -d --build
```

---

## Cloud Platform Deployment

### Heroku

#### 1. Create Procfile
```
web: gunicorn app_mysql:app
```

#### 2. Create runtime.txt
```
python-3.10.12
```

#### 3. Setup Heroku
```bash
heroku login
heroku create your-app-name
heroku addons:create cleardb:ignite  # MySQL database
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
git push heroku main
```

### Railway

1. Connect GitHub repository
2. Add MySQL service
3. Set environment variables
4. Deploy automatically

### AWS Elastic Beanstalk

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init`
3. Create environment: `eb create`
4. Deploy: `eb deploy`

### DigitalOcean App Platform

1. Connect repository
2. Add MySQL database component
3. Configure environment variables
4. Deploy

---

## Blockchain Configuration (Optional)

The blockchain feature is **optional**. The application works perfectly without it. The warning message is informational only.

### If You Want to Enable Blockchain Logging:

#### 1. Install web3
```bash
pip install web3==6.20.1
```

**Note**: On Windows with Python 3.13, you may need Visual C++ Build Tools.

#### 2. Get Infura Account (Free)
1. Sign up at [Infura.io](https://infura.io)
2. Create a new project
3. Copy your Project ID

#### 3. Get Testnet ETH
1. Create a MetaMask wallet
2. Get Sepolia testnet ETH from [Sepolia Faucet](https://sepoliafaucet.com/)

#### 4. Update .env.mysql
```env
# Blockchain Configuration (Optional)
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
BLOCKCHAIN_CONTRACT_ADDRESS=0xd9145CCE52D386f254917e481eB44e9943F39138
BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
BLOCKCHAIN_CHAIN_ID=11155111  # 11155111 for Sepolia, 1 for Mainnet
```

**⚠️ Security Warning**: 
- Never commit private keys to version control
- Use a dedicated account (not your main wallet)
- Use testnet for development
- Keep `.env.mysql` in `.gitignore`

#### 5. Deploy Smart Contract (Optional)
See `BLOCKCHAIN_SETUP.md` for detailed instructions.

---

## Environment Variables

### Required Variables
```env
SECRET_KEY=                    # Flask secret key (generate with: python -c "import secrets; print(secrets.token_hex(32))")
MYSQL_HOST=                   # MySQL host (localhost or IP)
MYSQL_PORT=                   # MySQL port (default: 3306)
MYSQL_USER=                   # MySQL username
MYSQL_PASSWORD=               # MySQL password
MYSQL_DATABASE=               # Database name
```

### Optional Variables
```env
FLASK_ENV=production          # production or development
FLASK_DEBUG=False             # True for development only
UPLOAD_FOLDER=uploads         # Upload directory
MAX_CONTENT_LENGTH=104857600  # Max file size in bytes (100MB)

# Blockchain (Optional)
BLOCKCHAIN_RPC_URL=
BLOCKCHAIN_CONTRACT_ADDRESS=
BLOCKCHAIN_PRIVATE_KEY=
BLOCKCHAIN_CHAIN_ID=
```

---

## Security Checklist

### Before Production Deployment

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use strong MySQL passwords
- [ ] Enable HTTPS/SSL (Let's Encrypt)
- [ ] Configure firewall (only allow 80, 443, 22)
- [ ] Set up regular database backups
- [ ] Configure file upload size limits
- [ ] Enable rate limiting
- [ ] Set secure session cookies
- [ ] Remove default credentials
- [ ] Keep dependencies updated
- [ ] Configure CORS properly
- [ ] Set up monitoring/logging
- [ ] Use environment variables (never hardcode secrets)
- [ ] Add `.env.mysql` to `.gitignore`

### Production Settings in app_mysql.py
```python
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

---

## Troubleshooting

### Common Issues

#### 1. "Blockchain not configured" Warning
**Solution**: This is normal and optional. The app works without blockchain. To enable, see [Blockchain Configuration](#blockchain-configuration-optional).

#### 2. MySQL Connection Error
```bash
# Check MySQL is running
sudo systemctl status mysql

# Test connection
mysql -u secure_user -p -h localhost secure_storage
```

#### 3. Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

#### 4. Permission Errors
```bash
# Fix upload directory permissions
chmod -R 755 uploads
chown -R www-data:www-data uploads
```

#### 5. Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Kill process or change port
```

---

## Monitoring and Maintenance

### Logs
```bash
# Application logs
sudo journalctl -u securecloud -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Database Backups
```bash
# Daily backup script
mysqldump -u secure_user -p secure_storage > backup_$(date +%Y%m%d).sql
```

### Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Restart service
sudo systemctl restart securecloud
```

---

## Support

For issues:
1. Check logs: `sudo journalctl -u securecloud -n 100`
2. Verify environment variables
3. Test database connection
4. Check file permissions

---

## Quick Start Commands

```bash
# Local development
python run_mysql.py

# Production with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 3 app_mysql:app

# Docker
docker-compose up -d

# Check status
sudo systemctl status securecloud
```

---

**Note**: The blockchain feature is completely optional. Your application will function normally without it. The warning is just informational.
