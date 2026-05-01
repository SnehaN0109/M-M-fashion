# Environment Setup Guide

## 🔧 Environment Configuration

### Frontend Setup
1. Copy `.env.example` to `.env`
2. Update `VITE_API_URL` if needed (default: `http://localhost:5000`)

### Backend Setup
1. Copy `backend/.env.example` to `backend/.env`
2. Fill in your database credentials:

#### For Local Development (MySQL)
```env
DB_USERNAME=root
DB_PASSWORD=your_local_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=mmfashion
DB_USE_SSL=false
```

#### For Aiven Cloud Database
```env
DB_USERNAME=avnadmin
DB_PASSWORD=your_aiven_password
DB_HOST=mysql-xxxxx-yourproject.aivencloud.com
DB_PORT=25285
DB_NAME=mmfashion
DB_USE_SSL=true
```

3. Set application secrets:
```env
SECRET_KEY=generate-a-strong-random-secret-key
ADMIN_PASSWORD=create-a-strong-admin-password
```

## 🚀 Quick Start
1. `npm install` - Install frontend dependencies
2. `pip install -r backend/requirements.txt` - Install backend dependencies
3. Configure environment files as above
4. `npm run dev` - Start both frontend and backend

## 🔒 Security Notes
- Never commit `.env` files to version control
- Use strong, unique passwords for production
- Rotate secrets regularly in production environments