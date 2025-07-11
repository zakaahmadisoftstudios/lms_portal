# LMS Portal API Documentation

## Base URL
- Production: `https://your-domain.com/api/`
- Development: `http://localhost:8000/api/`

## API Versioning
All endpoints are available under both:
- `/api/v1/` (explicit versioning)
- `/api/` (default to v1 for backward compatibility)

## Authentication
The API uses JWT (JSON Web Token) authentication.

### Authentication Endpoints
- **POST** `/api/auth/login/` - Obtain JWT token pair
- **POST** `/api/auth/refresh/` - Refresh access token
- **POST** `/api/auth/register/` - Register new user (Admin only)

### Authentication Headers
```
Authorization: Bearer <access_token>
```

## API Documentation
- **GET** `/api/` - API root with endpoint listing
- **GET** `/api/endpoints/` - Complete endpoint documentation

## User Profile
- **GET** `/api/profile/me/` - Get current user profile

## Dashboard
- **GET** `/api/dashboard/stats/` - Get dashboard statistics (role-based)

## Core Resources

### Users (Admin only)
- **GET** `/api/users/` - List all users
- **GET** `/api/users/{id}/` - Get user details

### Students
- **GET** `/api/students/` - List students (filtered by role)
- **POST** `/api/students/` - Create new student
- **GET** `/api/students/{id}/` - Get student details
- **PUT** `/api/students/{id}/` - Update student
- **PATCH** `/api/students/{id}/` - Partial update student
- **DELETE** `/api/students/{id}/` - Delete student

### Teachers
- **GET** `/api/teachers/` - List teachers
- **POST** `/api/teachers/` - Create new teacher
- **GET** `/api/teachers/{id}/` - Get teacher details
- **PUT** `/api/teachers/{id}/` - Update teacher
- **PATCH** `/api/teachers/{id}/` - Partial update teacher
- **DELETE** `/api/teachers/{id}/` - Delete teacher
- **GET** `/api/teachers/{id}/classes/` - Get classes taught by teacher
- **GET** `/api/teachers/{id}/students/` - Get students taught by teacher

### Classes
- **GET** `/api/classes/` - List classes (filtered by role)
- **POST** `/api/classes/` - Create new class
- **GET** `/api/classes/{id}/` - Get class details
- **PUT** `/api/classes/{id}/` - Update class
- **PATCH** `/api/classes/{id}/` - Partial update class
- **DELETE** `/api/classes/{id}/` - Delete class

### Subjects
- **GET** `/api/subjects/` - List subjects
- **POST** `/api/subjects/` - Create new subject (Admin only)
- **GET** `/api/subjects/{id}/` - Get subject details
- **PUT** `/api/subjects/{id}/` - Update subject (Admin only)
- **PATCH** `/api/subjects/{id}/` - Partial update subject (Admin only)
- **DELETE** `/api/subjects/{id}/` - Delete subject (Admin only)

### Assignments
- **GET** `/api/assignments/` - List assignments (filtered by role)
- **POST** `/api/assignments/` - Create new assignment
- **GET** `/api/assignments/{id}/` - Get assignment details
- **PUT** `/api/assignments/{id}/` - Update assignment
- **PATCH** `/api/assignments/{id}/` - Partial update assignment
- **DELETE** `/api/assignments/{id}/` - Delete assignment

### Grades
- **GET** `/api/grades/` - List grades (filtered by role)
- **POST** `/api/grades/` - Create new grade
- **GET** `/api/grades/{id}/` - Get grade details
- **PUT** `/api/grades/{id}/` - Update grade
- **PATCH** `/api/grades/{id}/` - Partial update grade
- **DELETE** `/api/grades/{id}/` - Delete grade

### Attendance
- **GET** `/api/attendance/` - List attendance records (filtered by role)
- **POST** `/api/attendance/` - Create attendance record
- **GET** `/api/attendance/{id}/` - Get attendance details
- **PUT** `/api/attendance/{id}/` - Update attendance
- **PATCH** `/api/attendance/{id}/` - Partial update attendance
- **DELETE** `/api/attendance/{id}/` - Delete attendance

## Role-Based Access Control

### Admin
- Full access to all endpoints
- Can create, read, update, delete all resources
- Can register new users

### Teacher
- Can view and manage students in their assigned classes
- Can create and grade assignments
- Can mark attendance for their classes
- Can view all assignments (for grading purposes)

### Student
- Can view their own profile
- Can view assignments for their class
- Can view their own grades and attendance
- Read-only access to their data

### Staff
- Read-only access to most resources
- Cannot create or modify data

## Request/Response Format

### Request Headers
```
Content-Type: application/json
Authorization: Bearer <access_token>
```

### Response Format
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/students/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error Response Format
```json
{
  "detail": "Error message",
  "field_errors": {
    "field_name": ["Error message for field"]
  }
}
```

## Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Filtering and Pagination

### Query Parameters
- `page` - Page number for pagination
- `page_size` - Number of items per page (default: 20)
- `search` - Search term (where applicable)
- `ordering` - Field to order by (prefix with `-` for descending)

### Example
```
GET /api/students/?page=2&page_size=10&search=john&ordering=-created_at
``` 