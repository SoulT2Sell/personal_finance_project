# Personal Finance Manager

A comprehensive personal finance management application built with Django, featuring multi-currency support, real-time exchange rates, and an intuitive Persian/Farsi interface.

## Features

### Core Functionality
- **Multi-Currency Accounts** - Manage bank accounts, cash, and cards in different currencies
- **Transaction Tracking** - Record income, expenses, transfers with categories
- **Category Management** - Organize transactions with customizable categories
- **Dashboard Analytics** - Visual overview of balances, income, expenses, and spending patterns
- **User Profiles** - Personalized settings including preferred currency and timezone

### Currency & Exchange Rates
- **Smart Currency Formatting** - Automatic formatting per currency (IRR: no decimals, USD/EUR: 2 decimals, BHD/KWD: 3 decimals)
- **Real-time Exchange Rates** - Fetches from free APIs (Frankfurter, ExchangeRate.host, OpenERP) with caching
- **Database Fallback** - Stores rates locally; falls back to database when APIs are unreachable
- **Preferred Currency Display** - All dashboard totals converted to user's preferred currency

### Admin & Management
- **Custom Persian Admin Panel** - Fully localized admin interface at `/admin-persian/`
- **Exchange Rate Management** - Admin interface to manually set/update exchange rates
- **Django Admin Integration** - Standard admin at `/admin/` for developers

### User Experience
- **Persian/Farsi Interface** - Complete RTL support with Vazirmatn font
- **Native Date Pickers** - HTML5 calendar inputs for transaction dates
- **Responsive Design** - Works on desktop and mobile
- **Dark/Light Theme Ready** - CSS variables for easy theming

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Django 6.1 |
| Database | PostgreSQL (production) / SQLite (development) |
| Frontend | Server-side templates, Vanilla JS, CSS Variables |
| Fonts | Vazirmatn (Persian), IBM Plex Mono |
| Icons | Inline SVG |
| Exchange APIs | Frankfurter.app, ExchangeRate.host, OpenERP |
| Caching | Django Cache Framework (1-hour TTL) |
| Containerization | Docker & Docker Compose |

## Project Structure

```
personal_finance_project/
├── apps/
│   ├── accounts/          # Bank accounts & types
│   ├── categories/        # Transaction categories
│   ├── common/            # Shared models (Currency, ExchangeRate), admin site, template tags
│   ├── dashboard/         # Dashboard views & services
│   ├── transactions/      # Transaction CRUD & services
│   └── users/             # Custom User, Profile, Auth
├── config/                # Django settings, URLs, WSGI/ASGI
├── services/              # Business logic services
│   ├── dashboard_service.py
│   ├── exchange_rate_service.py
│   └── transaction_service.py
├── helpers/               # Base models
├── static/                # CSS, JS assets
└── templates/             # Base templates
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.14+ (for local development)

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd personal_finance_project

# Start services
docker compose up -d

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Access at http://localhost:8000
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # Edit with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## Configuration

### Environment Variables (.env)
```env
POSTGRES_DB=personal_finance
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=your-secret-key
DEBUG=True
```

### Key Settings
- `TIME_ZONE` - Default: UTC (user can override in profile)
- `LANGUAGE_CODE` - Default: en-us (UI is Persian)
- `CACHE_BACKEND` - For exchange rate caching

## Usage

### 1. Set Up Your Profile
- Navigate to **پروفایل** (Profile)
- Select your **ارز ترجیحی** (Preferred Currency)
- Set your **منطقه زمانی** (Timezone)

### 2. Create Accounts
- Go to **حساب‌ها** (Accounts) → **حساب جدید**
- Choose account type (Bank, Cash, Card)
- Select currency and initial balance

### 3. Add Categories
- Visit **کتگوری‌ها** (Categories) → **کتگوری جدید**
- Create categories for income/expenses

### 4. Record Transactions
- Click **تراکنش جدید** (New Transaction) from dashboard
- Select account, category, type (Income/Expense)
- Enter amount, date, and description

### 5. View Dashboard
- **موجودی کل** - Total balance across all accounts (in preferred currency)
- **درآمد/هزینه این ماه** - Monthly income/expense
- **آخرین تراکنش‌ها** - Recent transactions
- **هزینه‌ها بر اساس دسته‌بندی** - Spending breakdown

## Currency Formatting

The application automatically formats amounts based on currency:

| Currency | Example | Decimal Places |
|----------|---------|----------------|
| IRR, VND, JPY, KRW | 1،234،568 | 0 |
| USD, EUR, GBP, TRY | 1،234،567.89 | 2 |
| BHD, JOD, KWD, OMR | 1،234،567.890 | 3 |

Template usage:
```django
{% load currency_tags %}
{% format_currency amount "IRR" %}           {# 1،234،568 #}
{% format_currency amount "USD" %}           {# 1،234،567.89 #}
{% format_currency_with_symbol amount "IRR" #} {# 1،234،568 IRR #}
```

## Exchange Rate Service

### Automatic Updates
```python
from services.exchange_rate_service import ExchangeRateService

# Fetch and store latest rates (base: USD)
results = ExchangeRateService.update_rates_from_api("USD")
print(results["success"])  # List of updated rates
```

### Manual Rate Entry
Via admin panel at `/admin-persian/common/exchangerate/` or `/admin/common/exchangerate/`

### API Priority
1. **Frankfurter.app** (ECB rates, no key required)
2. **ExchangeRate.host** (Free, multiple sources)
3. **OpenERP API** (Backup)
4. **Database** (Local fallback)
5. **Reverse calculation** (If direct rate missing)
6. **Default 1.0** (Ultimate fallback)

## API Endpoints

| URL | Description |
|-----|-------------|
| `/` | Redirects to dashboard |
| `/dashboard/` | Main dashboard |
| `/accounts/` | Account list & management |
| `/categories/` | Category list & management |
| `/transactions/` | Transaction list, create, edit |
| `/users/profile/` | User profile |
| `/users/profile/edit/` | Edit profile |
| `/admin/` | Django admin |
| `/admin-persian/` | Persian admin panel |

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
```bash
# Format with Black
black .

# Sort imports
isort .

# Lint
pylint apps/
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use strong `SECRET_KEY`
- [ ] Set up PostgreSQL
- [ ] Configure static files (`collectstatic`)
- [ ] Set up reverse proxy (Nginx)
- [ ] Enable HTTPS
- [ ] Configure caching backend (Redis/Memcached)
- [ ] Set up monitoring/logging

### Docker Production
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Vazirmatn Font](https://github.com/rastikerdar/vazirmatn) for Persian typography
- [Frankfurter.app](https://api.frankfurter.app) for free exchange rates
- [ExchangeRate.host](https://exchangerate.host) for reliable rate API
- Django community for the excellent framework

---

**Built with ❤️ for personal finance management**