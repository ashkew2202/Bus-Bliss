# 🚌 Bus Bliss

A modern bus ticket booking web application built with Django and Docker.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.1-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)

## Features

- 🎫 **Bus Ticket Booking** - Search and book bus tickets across multiple routes
- 👤 **User Authentication** - Email/password and Google OAuth login
- 💰 **Wallet System** - Add balance and pay for bookings
- 📧 **OTP Verification** - Secure booking confirmation via email
- 📱 **Responsive Design** - Mobile-friendly modern UI

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Bus-Bliss.git
cd Bus-Bliss
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:

```env
# Django Secret Key (generate a new one for production)
SECRET_KEY=your-django-secret-key-here

# Google OAuth (get from Google Cloud Console)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# PostgreSQL Database
DB_USERNAME=postgres
DB_PASSWORD=your-secure-password
SQL_HOST=db
PORT_NUMBER=5432

# Email (Gmail SMTP)
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

#### Getting the Required Credentials

**Django Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Google OAuth Credentials:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Navigate to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth 2.0 Client IDs**
5. Set authorized redirect URI to: `http://localhost:8000/accounts/google/login/callback/`
6. Copy the Client ID and Client Secret

**Gmail App Password:**
1. Enable 2-Factor Authentication on your Google account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password for "Mail"
4. Use this password (not your regular Gmail password)

### 3. Build and Run

```bash
docker compose up --build -d
```

### 4. Access the Application

Open your browser and navigate to: **http://localhost:8000**

## Project Structure

```
Bus-Bliss/
├── docker-compose.yml      # Docker services configuration
├── .env                    # Environment variables (create this)
├── dvm_task/
│   ├── Dockerfile          # Web app container
│   ├── manage.py           # Django management
│   ├── requirements.txt    # Python dependencies
│   ├── entrypoint.sh       # Container startup script
│   ├── booking/            # Main booking app
│   │   ├── models.py       # Database models
│   │   ├── views.py        # View controllers
│   │   ├── urls.py         # URL routing
│   │   └── templates/      # HTML templates
│   └── dvm_task/
│       ├── settings.py     # Django settings
│       └── urls.py         # Root URL config
└── nginx/                  # Nginx config (production)
```

## Docker Commands

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild and start
docker compose up --build -d

# Reset database (removes all data)
docker compose down -v
docker compose up -d
```

## Development

### Running Migrations Manually

```bash
docker compose exec web python manage.py migrate
```

### Creating Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### Accessing Django Admin

Navigate to: **http://localhost:8000/admin**

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key for cryptographic signing | ✅ |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | ✅ |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | ✅ |
| `DB_USERNAME` | PostgreSQL username | ✅ |
| `DB_PASSWORD` | PostgreSQL password | ✅ |
| `SQL_HOST` | Database host (use `db` for Docker) | ✅ |
| `PORT_NUMBER` | PostgreSQL port (default: 5432) | ✅ |
| `EMAIL_HOST_PASSWORD` | Gmail app password for SMTP | ✅ |

## Troubleshooting

### Database Connection Error
```bash
# Reset the database volume
docker compose down -v
docker compose up -d
```

### Permission Denied on entrypoint.sh
```bash
chmod +x dvm_task/entrypoint.sh
docker compose build --no-cache
```

### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000
# Or change the port in docker-compose.yml
```

## Tech Stack

- **Backend:** Django 5.1, Python 3.11
- **Database:** PostgreSQL 17
- **Authentication:** django-allauth (Email + Google OAuth)
- **Containerization:** Docker, Docker Compose
- **Email:** Gmail SMTP

## License

This project is for educational purposes.

---

Made with ❤️ using Django and Docker