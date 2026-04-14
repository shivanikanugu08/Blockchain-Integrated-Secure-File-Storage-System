# Quick Deployment Guide

## 🚀 Fastest Way to Deploy

### Local Development (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env.mysql file
cat > .env.mysql << EOF
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=secure_storage
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=104857600
EOF

# 3. Setup MySQL database
mysql -u root -p -e "CREATE DATABASE secure_storage CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 4. Initialize database
python -c "from app_mysql import app, db; app.app_context().push(); db.create_all()"

# 5. Run application
python run_mysql.py
```

Visit: `http://localhost:5000`

---

## 📦 Production Deployment (3 Options)

### Option 1: Docker (Easiest)
```bash
docker-compose up -d
```

### Option 2: VPS with Gunicorn
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 3 app_mysql:app
```

### Option 3: Cloud Platform
- **Heroku**: `git push heroku main`
- **Railway**: Connect repo → Add MySQL → Deploy
- **DigitalOcean**: Connect repo → Add database → Deploy

---

## ⚙️ Blockchain Configuration (Optional)

**The blockchain feature is OPTIONAL. Your app works fine without it.**

To enable (if you want):

1. **Get Infura account** (free): https://infura.io
2. **Get testnet ETH**: https://sepoliafaucet.com/
3. **Add to .env.mysql**:
```env
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
BLOCKCHAIN_CONTRACT_ADDRESS=0xd9145CCE52D386f254917e481eB44e9943F39138
BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRIVATE_KEY
BLOCKCHAIN_CHAIN_ID=11155111
```

**That's it!** The warning will disappear once configured.

---

## 🔒 Security Checklist

Before going live:
- [ ] Change SECRET_KEY
- [ ] Use strong MySQL password
- [ ] Set FLASK_DEBUG=False
- [ ] Enable HTTPS (Let's Encrypt)
- [ ] Configure firewall
- [ ] Set up backups

---

## 🆘 Troubleshooting

**"Blockchain not configured"** → Normal! App works without it.

**MySQL connection error** → Check credentials in .env.mysql

**Import errors** → Run `pip install -r requirements.txt`

**Port in use** → Change port or kill process

---

## 📚 Full Documentation

See `DEPLOYMENT.md` for complete deployment guide.
