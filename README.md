# 🎓 LMS Portal API

A comprehensive Learning Management System (LMS) API built with Django REST Framework, featuring role-based access control, JWT authentication, and complete CRUD operations for educational institutions.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [API Testing](#-api-testing)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Role-Based Access Control](#-role-based-access-control)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Features

### Core Functionality

- **User Management** - Multi-role user system (Admin, Teacher, Student, Staff)
- **Student Management** - Complete student profiles with guardian information
- **Teacher Management** - Teacher profiles with qualifications and subjects
- **Class Management** - Academic classes with grade levels and sections
- **Subject Management** - Subject catalog with codes and credits
- **Assignment Management** - Create and manage assignments with multiple types
- **Grade Management** - Grade assignments with automatic letter grade calculation
- **Attendance Management** - Daily attendance tracking with multiple status options

### Security & Authentication

- **JWT Authentication** - Secure token-based authentication
- **Role-Based Access Control** - Granular permissions based on user roles
- **Token Refresh** - Automatic token refresh functionality
- **Password Security** - Secure password hashing and validation

### API Features

- **RESTful API Design** - Clean, consistent API endpoints
- **Pagination** - Efficient data pagination for large datasets
- **Search & Filtering** - Advanced search and filtering capabilities
- **Comprehensive Documentation** - Auto-generated API documentation
- **Health Monitoring** - API health check endpoints
- **Versioning Support** - API versioning for backward compatibility

## 🛠️ Tech Stack

- **Backend Framework**: Django 5.2 + Django REST Framework
- **Authentication**: Simple JWT (JSON Web Tokens)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **API Documentation**: Built-in endpoint documentation
- **Testing**: Django Test Framework + Postman Collections
- **Deployment**: Ready for Docker, Heroku, or traditional hosting

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/lms_portal.git
   cd lms_portal
   ```
2. **Create virtual environment**

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Set up database**

   ```bash
   # Run migrations
   python manage.py migrate

   # Create superuser (admin)
   python manage.py createsuperuser
   ```
5. **Start development server**

   ```bash
   python manage.py runserver
   ```
6. **Access the application**

   - API Root: http://localhost:8000/api/
   - Admin Panel: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/api/endpoints/
   - Health Check: http://localhost:8000/api/health/

## 🧪 API Testing

### Quick Test

Run the included test script to verify basic API functionality:

```bash
python api_test_script.py
```

### Postman Collection

We provide a comprehensive Postman collection for thorough API testing:

- **📁 Collection File**: [`LMS_Portal_API.postman_collection.json`](./LMS_Portal_API.postman_collection.json)
- **🌍 Environment File**: [`LMS_Portal_API.postman_environment.json`](./LMS_Portal_API.postman_environment.json)
- **📖 Complete Testing Guide**: [POSTMAN_API_TESTING.md](./POSTMAN_API_TESTING.md)

#### Import to Postman

1. Download and install [Postman](https://www.postman.com/downloads/)
2. Import the collection and environment files
3. Select "LMS Portal - Development" environment
4. Follow the [detailed testing guide](./POSTMAN_API_TESTING.md)

#### Test Coverage

- ✅ **48 API endpoints** fully tested
- ✅ **4 user roles** (Admin, Teacher, Student, Staff)
- ✅ **Authentication flows** (Login, Token Refresh, Registration)
- ✅ **CRUD operations** for all resources
- ✅ **Role-based permissions** testing
- ✅ **Error handling** scenarios
- ✅ **Pagination & filtering** functionality

### Manual Testing

```bash
# Test API health
curl http://localhost:8000/api/health/

# Get API documentation
curl http://localhost:8000/api/endpoints/

# Login to get tokens
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

## 📁 Project Structure

```
lms_portal/
├── api/                          # Main API application
│   ├── migrations/              # Database migrations
│   ├── __init__.py
│   ├── admin.py                 # Django admin configuration
│   ├── apps.py                  # App configuration
│   ├── models.py                # Data models
│   ├── permissions.py           # Custom permissions
│   ├── serializers.py           # API serializers
│   ├── urls.py                  # API URL routing
│   └── views.py                 # API views and endpoints
├── lms/                         # Django project settings
│   ├── __init__.py
│   ├── asgi.py                  # ASGI configuration
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Main URL configuration
│   └── wsgi.py                  # WSGI configuration
├── venv/                        # Virtual environment
├── api_test_script.py           # Quick API test script
├── db.sqlite3                   # SQLite database (development)
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── API_ENDPOINTS.md             # Detailed API documentation
├── POSTMAN_API_TESTING.md       # Postman testing guide
├── LMS_Portal_API.postman_collection.json    # Postman collection
├── LMS_Portal_API.postman_environment.json   # Postman environment
└── README.md                    # This file
```

## 📚 API Documentation

### Core Endpoints

#### Authentication

- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh access token
- `POST /api/auth/register/` - Register new user (Admin only)

#### User Management

- `GET /api/users/` - List users (Admin only)
- `GET /api/users/{id}/` - Get user details
- `POST /api/users/convert-to-teacher/` - Convert user to teacher
- `POST /api/users/convert-to-student/` - Convert user to student

#### Academic Management

- `GET|POST /api/students/` - Student operations
- `GET|POST /api/teachers/` - Teacher operations
- `GET|POST /api/classes/` - Class operations
- `GET|POST /api/subjects/` - Subject operations
- `GET|POST /api/assignments/` - Assignment operations
- `GET|POST /api/grades/` - Grade operations
- `GET|POST /api/attendance/` - Attendance operations

#### System

- `GET /api/` - API root with endpoint listing
- `GET /api/endpoints/` - Complete API documentation
- `GET /api/health/` - Health check
- `GET /api/profile/me/` - Current user profile
- `GET /api/dashboard/stats/` - Dashboard statistics

### Detailed Documentation

For complete API documentation with request/response examples, see:

- **[API_ENDPOINTS.md](./API_ENDPOINTS.md)** - Comprehensive endpoint documentation
- **Live API Docs**: http://localhost:8000/api/endpoints/ (when server is running)

## 🔐 Role-Based Access Control

### User Roles

| Role              | Permissions        | Description                                                            |
| ----------------- | ------------------ | ---------------------------------------------------------------------- |
| **Admin**   | Full Access        | Complete system administration, user management, all CRUD operations   |
| **Teacher** | Limited Access     | Manage assigned classes, students, assignments, grades, and attendance |
| **Student** | Read-Only Own Data | View own profile, classes, assignments, grades, and attendance         |
| **Staff**   | Read-Only System   | View most system data but cannot modify                                |

### Permission Matrix

| Resource    | Admin | Teacher                | Student         | Staff |
| ----------- | ----- | ---------------------- | --------------- | ----- |
| Users       | CRUD  | Read (assigned)        | Read (self)     | Read  |
| Students    | CRUD  | Read/Update (assigned) | Read (self)     | Read  |
| Teachers    | CRUD  | Read (self)            | Read            | Read  |
| Classes     | CRUD  | Read (assigned)        | Read (enrolled) | Read  |
| Subjects    | CRUD  | Read                   | Read            | Read  |
| Assignments | CRUD  | CRUD (own classes)     | Read (own)      | Read  |
| Grades      | CRUD  | CRUD (own assignments) | Read (own)      | Read  |
| Attendance  | CRUD  | CRUD (own classes)     | Read (own)      | Read  |

## 💻 Development

### Environment Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/lms_portal.git
cd lms_portal
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Database setup
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Configuration

#### Environment Variables

Create a `.env` file for sensitive settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### Database Configuration

```python
# For PostgreSQL (production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lms_portal',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Adding New Features

1. **Create Models** in `api/models.py`
2. **Create Serializers** in `api/serializers.py`
3. **Create Views** in `api/views.py`
4. **Add URLs** in `api/urls.py`
5. **Create Permissions** in `api/permissions.py`
6. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## 🧪 Testing

### Backend Testing

```bash
# Run Django tests
python manage.py test

# Run with coverage
pip install coverage
coverage run manage.py test
coverage report
coverage html  # Generate HTML report
```

### API Testing Options

1. **Postman Collection** (Recommended)

   - Import collection and environment files
   - Follow [POSTMAN_API_TESTING.md](./POSTMAN_API_TESTING.md)
2. **Quick Test Script**

   ```bash
   python api_test_script.py
   ```
3. **Manual Testing with cURL**

   ```bash
   # Health check
   curl http://localhost:8000/api/health/

   # Login
   curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "your_password"}'
   ```
4. **Django Test Framework**

   ```bash
   # Run specific test
   python manage.py test api.tests.TestUserAPI

   # Run with verbosity
   python manage.py test --verbosity=2
   ```

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "lms.wsgi:application"]
```

### Traditional Server Deployment

```bash
# Install production dependencies
pip install gunicorn psycopg2-binary

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 lms.wsgi:application
```

### Environment Configuration

```bash
# Production settings
export DJANGO_SETTINGS_MODULE=lms.settings
export DEBUG=False
export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Update documentation** if needed
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Create a Pull Request**

### Development Guidelines

- Follow PEP 8 coding standards
- Write comprehensive tests for new features
- Update API documentation for new endpoints
- Update Postman collection for new API endpoints
- Ensure all tests pass before submitting PR

### Testing Your Changes

```bash
# Run backend tests
python manage.py test

# Test API with Postman collection
# Follow POSTMAN_API_TESTING.md

# Run quick API test
python api_test_script.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django and Django REST Framework communities
- Contributors and testers
- Educational institutions providing feedback

## 📞 Support

- **Documentation**: [API_ENDPOINTS.md](./API_ENDPOINTS.md)
- **Testing Guide**: [POSTMAN_API_TESTING.md](./POSTMAN_API_TESTING.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/lms_portal/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/lms_portal/discussions)

---

**Made with ❤️ for educational institutions worldwide**
