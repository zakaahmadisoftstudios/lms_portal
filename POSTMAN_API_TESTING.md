# LMS Portal API Testing with Postman

This guide will help you set up and use the Postman collection for testing the LMS Portal API with comprehensive role-based access control.

## 📋 Table of Contents
- [Files Included](#files-included)
- [Setup Instructions](#setup-instructions)
- [Collection Structure](#collection-structure)
- [Usage Instructions](#usage-instructions)
- [Environment Variables](#environment-variables)
- [Test Scenarios](#test-scenarios)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)

## 📁 Files Included

- `LMS_Portal_API.postman_collection.json` - Complete Postman collection with all API endpoints
- `LMS_Portal_API.postman_environment.json` - Environment variables for development testing
- `api_test_script.py` - Python script for basic API connectivity testing

## 🚀 Setup Instructions

### 1. Import Files into Postman

1. Open Postman Desktop App or Web Version
2. Click on "Import" button (top-left corner)
3. Import both files:
   - `LMS_Portal_API.postman_collection.json`
   - `LMS_Portal_API.postman_environment.json`
4. You should see "LMS Portal API" collection and "LMS Portal - Development" environment

### 2. Select Environment

1. In the top-right corner of Postman, select "LMS Portal - Development" environment
2. The environment contains pre-configured variables like `base_url`, authentication tokens, and test credentials

### 3. Start Your Django Server

Make sure your Django development server is running:

```bash
# Navigate to project directory
cd /path/to/lms_portal

# Activate virtual environment (if using one)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (if not exists)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

The API should be accessible at `http://localhost:8000/api/`

### 4. Quick Connectivity Test

Run the included Python test script to verify basic connectivity:

```bash
python api_test_script.py
```

## 📚 Collection Structure

The collection is organized into the following folders:

### 🔐 Authentication
- **Login** - Obtain JWT access and refresh tokens with user profile info
- **Refresh Token** - Refresh expired access token
- **Register User** - Register new user (Admin only)

### 👤 Profile & Dashboard
- **Get Current User Profile** - Get authenticated user's profile information
- **Get Dashboard Stats** - Get role-based dashboard statistics

### 👥 Users (Admin Only)
- **List Users** - List all users with pagination
- **Get User Details** - Get specific user details
- **Convert User to Teacher** - Convert existing user to teacher role ⭐ *NEW*
- **Convert User to Student** - Convert existing user to student role ⭐ *NEW*

### 🎓 Students
- **List Students** - List students (role-filtered with pagination)
- **Create Student** - Create new student record
- **Get Student Details** - Get specific student information
- **Update Student** - Full update of student record
- **Partial Update Student** - Partial update of student record
- **Delete Student** - Delete student record

### 👨‍🏫 Teachers
- **List Teachers** - List all teachers
- **Create Teacher** - Create new teacher record
- **Get Teacher Details** - Get specific teacher information
- **Get Teacher Classes** - Get classes taught by specific teacher
- **Get Teacher Students** - Get students taught by specific teacher
- **Update Teacher** - Update teacher record
- **Delete Teacher** - Delete teacher record

### 🏫 Classes
- **List Classes** - List classes (role-filtered)
- **Create Class** - Create new class
- **Get Class Details** - Get specific class information
- **Update Class** - Update class record
- **Delete Class** - Delete class

### 📚 Subjects
- **List Subjects** - List all subjects
- **Create Subject** - Create new subject (Admin only)
- **Get Subject Details** - Get specific subject information
- **Update Subject** - Update subject (Admin only)
- **Delete Subject** - Delete subject (Admin only)

### 📝 Assignments
- **List Assignments** - List assignments (role-filtered)
- **Create Assignment** - Create new assignment
- **Get Assignment Details** - Get specific assignment information
- **Update Assignment** - Update assignment
- **Delete Assignment** - Delete assignment

### 📊 Grades
- **List Grades** - List grades (role-filtered)
- **Create Grade** - Create new grade record
- **Get Grade Details** - Get specific grade information
- **Update Grade** - Update grade record
- **Delete Grade** - Delete grade record

### 📅 Attendance
- **List Attendance** - List attendance records (role-filtered)
- **Create Attendance Record** - Mark student attendance
- **Get Attendance Details** - Get specific attendance record
- **Update Attendance** - Update attendance record
- **Delete Attendance** - Delete attendance record

### ⚙️ System
- **API Root** - Get API root with endpoint listing
- **API Endpoints Documentation** - Get complete endpoint documentation
- **Health Check** - Check API health status

## 🎯 Usage Instructions

### Step 1: Authentication

1. **First Login**:
   - Open "Authentication" → "Login" request
   - Update the request body with valid credentials:
     ```json
     {
         "username": "your_username",
         "password": "your_password"
     }
     ```
   - Send the request
   - The collection will automatically store tokens and user info in environment variables

2. **Token Management**:
   - Access tokens expire after 60 minutes
   - Use "Authentication" → "Refresh Token" when tokens expire
   - The collection automatically handles token refresh

### Step 2: Test API Endpoints

1. **System Health Check**:
   ```bash
   # Test API connectivity first
   GET {{base_url}}/health/
   ```

2. **API Documentation**:
   ```bash
   # View all available endpoints
   GET {{base_url}}/endpoints/
   ```

3. **Role-Based Testing**:
   - Login with different user roles to test access control
   - Each role has specific permissions and data visibility

### Step 3: Data Flow Testing

**Recommended Testing Order:**
1. **System** → Health Check & API Root
2. **Authentication** → Login with admin credentials
3. **Subjects** → Create subjects first
4. **Users** → Create users or convert existing users
5. **Teachers** → Create teacher profiles
6. **Classes** → Create classes and assign teachers
7. **Students** → Create student profiles and enroll in classes
8. **Assignments** → Create assignments for classes
9. **Grades** → Grade student assignments
10. **Attendance** → Mark daily attendance

## 🔧 Environment Variables

### Core Variables
- `base_url` - API base URL (default: `http://localhost:8000/api`)
- `access_token` - JWT access token (auto-populated after login)
- `refresh_token` - JWT refresh token (auto-populated after login)
- `user_id` - Current user ID (auto-populated after login)
- `user_role` - Current user role (auto-populated after login)

### Test Credentials
- `admin_username` / `admin_password` - Admin user credentials
- `teacher_username` / `teacher_password` - Teacher user credentials  
- `student_username` / `student_password` - Student user credentials

### Custom Variables
You can add custom variables for testing:
- Test student IDs, class IDs, assignment IDs
- Custom API endpoints for different environments

## 🧪 Test Scenarios

### Admin User Testing
```javascript
// Admin can access all endpoints
1. Login as admin
2. Create subjects, classes, teachers, and students
3. Test user registration and conversion
4. Access all user data and system management
5. Test dashboard statistics
```

### Teacher User Testing  
```javascript
// Teacher has limited access to assigned data
1. Login as teacher
2. View assigned classes and enrolled students
3. Create assignments for assigned classes
4. Grade student assignments
5. Mark attendance for assigned classes
6. Verify restricted access to other teacher's data
```

### Student User Testing
```javascript
// Student has read-only access to own data
1. Login as student
2. View own profile and class information
3. View assignments and grades for enrolled class
4. View own attendance records
5. Verify no access to other students' data
6. Verify no create/update/delete permissions
```

### Staff User Testing
```javascript
// Staff has read-only access to most resources
1. Login as staff
2. View students, teachers, classes (read-only)
3. View assignments and grades (read-only)
4. Verify no create/update/delete permissions
5. Verify no access to sensitive data
```

## 🔍 Advanced Testing Features

### Pagination Testing
```javascript
// Test pagination parameters
GET {{base_url}}/students/?page=2&page_size=5

// Test search functionality  
GET {{base_url}}/students/?search=john

// Test ordering
GET {{base_url}}/students/?ordering=-created_at
```

### Error Handling Testing
```javascript
// Test authentication errors
1. Send requests without Authorization header
2. Send requests with expired tokens
3. Test with invalid credentials

// Test validation errors
1. Send incomplete data in POST requests
2. Send invalid data types
3. Test required field validation

// Test permission errors
1. Access admin endpoints as student
2. Access other users' data
3. Test cross-role data access
```

### Bulk Operations Testing
```javascript
// Test user conversion workflows
1. Create user with basic profile
2. Convert user to teacher using conversion endpoint
3. Assign subjects and classes to teacher
4. Convert another user to student
5. Enroll student in classes
```

## 🛠️ Troubleshooting

### Common Issues

1. **401 Unauthorized**:
   ```javascript
   // Solution: Re-authenticate
   POST {{base_url}}/auth/login/
   // Or refresh token
   POST {{base_url}}/auth/refresh/
   ```

2. **403 Forbidden**:
   ```javascript
   // Check user role and permissions
   GET {{base_url}}/profile/me/
   // Verify endpoint permissions in API documentation
   ```

3. **404 Not Found**:
   ```javascript
   // Verify resource exists
   GET {{base_url}}/students/  // List all first
   // Check correct resource ID
   GET {{base_url}}/students/1/
   ```

4. **400 Bad Request**:
   ```javascript
   // Check request body format and required fields
   // Verify data types match model requirements
   // Check foreign key relationships exist
   ```

### Server Issues

1. **Connection Refused**:
   ```bash
   # Ensure Django server is running
   python manage.py runserver
   
   # Check server logs for errors
   tail -f /path/to/logs/django.log
   ```

2. **Database Issues**:
   ```bash
   # Run migrations
   python manage.py migrate
   
   # Check database connection
   python manage.py dbshell
   ```

3. **Authentication Issues**:
   ```bash
   # Create superuser
   python manage.py createsuperuser
   
   # Reset user password
   python manage.py changepassword username
   ```

## 🔗 Additional Resources

### API Documentation
- **Live API Docs**: `GET {{base_url}}/endpoints/`
- **API Root**: `GET {{base_url}}/`
- **Health Status**: `GET {{base_url}}/health/`

### Development Tools
- **Django Admin Panel**: `http://localhost:8000/admin/`
- **API Test Script**: `python api_test_script.py`
- **Database Management**: Django ORM through `python manage.py shell`

### Environment Configuration

**Development Environment:**
```json
{
  "base_url": "http://localhost:8000/api",
  "debug_mode": true
}
```

**Staging Environment:**
```json  
{
  "base_url": "https://staging.yourdomain.com/api",
  "debug_mode": false
}
```

**Production Environment:**
```json
{
  "base_url": "https://api.yourdomain.com/api", 
  "debug_mode": false
}
```

## 📊 Testing Metrics & Coverage

### API Endpoint Coverage
- ✅ Authentication endpoints (3/3)
- ✅ User management endpoints (4/4) - *Updated with conversion endpoints*
- ✅ Student management endpoints (6/6)
- ✅ Teacher management endpoints (7/7)
- ✅ Class management endpoints (5/5)
- ✅ Subject management endpoints (5/5)
- ✅ Assignment management endpoints (5/5)
- ✅ Grade management endpoints (5/5)
- ✅ Attendance management endpoints (5/5)
- ✅ System endpoints (3/3)

### Role-Based Testing Coverage
- ✅ Admin role (full access)
- ✅ Teacher role (restricted access)
- ✅ Student role (read-only own data)
- ✅ Staff role (read-only system data)

---

For more detailed information about the API structure, data models, and role-based permissions, refer to the `API_ENDPOINTS.md` file and the main project README.md. 