# Role-Based Access Control (RBAC) System Documentation

## Overview
This RBAC system implements a hierarchical role structure for the question paper generation application with three main roles:
- **Superadmin**: Can create institutes and assign COEs
- **COE (Controller of Examination)**: Can manage faculty for their assigned institute
- **Faculty**: Can create question papers and submit them for approval

## Database Schema

### Tables Created

#### 1. Users Table (Updated)
```sql
- id (PK)
- first_name, last_name, username, email
- password (hashed)
- is_active, created_at, updated_at
```

#### 2. Institutes Table
```sql
- id (PK)
- name, code (unique)
- address, email, phone
- is_active, created_at, updated_at
```

#### 3. Roles Table
```sql
- id (PK)
- name (unique: superadmin, coe, faculty)
- description, created_at
```

#### 4. User Roles Table (Junction Table)
```sql
- id (PK)
- user_id (FK to users)
- role_id (FK to roles)
- institute_id (FK to institutes, NULL for superadmin)
- is_active, created_at, updated_at
```

## API Endpoints

### Authentication Routes (`/auth`)

#### POST `/auth/signup`
- Create a new user account
- Body: `UserCreate` schema
- Response: Success message

#### POST `/auth/login`
- Authenticate user and return JWT token
- Body: `UserLogin` schema
- Response: `TokenResponse` with user info, roles, and institute

#### GET `/auth/me`
- Get current user information (requires authentication)
- Response: `TokenResponse` without token

#### POST `/auth/initialize-roles`
- Initialize default roles in database
- Response: Success message

### Superadmin Routes (`/admin`) - Requires Superadmin Role

#### POST `/admin/institutes`
- Create a new institute
- Body: `InstituteCreate` schema
- Response: `InstituteResponse`

#### GET `/admin/institutes`
- List all institutes
- Response: Array of `InstituteResponse`

#### POST `/admin/coe`
- Create COE for an institute
- Body: `COECreate` schema
- Response: `UserRoleResponse`

#### GET `/admin/coe`
- List all COEs
- Response: Array of `UserRoleResponse`

### COE Routes (`/coe`) - Requires COE Role

#### POST `/coe/faculty`
- Create faculty for COE's institute
- Body: `FacultyCreate` schema
- Response: `UserRoleResponse`

#### GET `/coe/faculty`
- List faculty for COE's institute
- Response: Array of `UserRoleResponse`

## Security Features

### JWT Authentication
- Uses JWT tokens for authentication
- Token expires after 30 minutes
- Tokens contain user ID and username

### Role-Based Middleware
- `@require_role("role_name")` decorator for single role requirement
- `@require_any_role(["role1", "role2"])` decorator for multiple role options
- Automatic role verification on protected endpoints

### Permission Functions
- `can_manage_institutes()`: Superadmin only
- `can_manage_faculty()`: COE of specific institute only
- `can_create_question_paper()`: Faculty only
- `can_approve_question_paper()`: COE of institute only

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Initialize Database
```bash
cd backend
python3 init_rbac_db.py
```

### 3. Default Credentials
After initialization:
- Username: `superadmin`
- Password: `admin123`
- **IMPORTANT**: Change this password in production!

### 4. Start Server
```bash
uvicorn main:app --reload
```

## Usage Examples

### 1. Superadmin Creates Institute
```bash
curl -X POST "http://localhost:8000/admin/institutes" \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Engineering College",
    "code": "EC001",
    "email": "info@engcollege.edu"
  }'
```

### 2. Superadmin Creates COE
```bash
curl -X POST "http://localhost:8000/admin/coe" \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "username": "john_coe",
    "password": "password123",
    "email": "john@engcollege.edu",
    "institute_id": 1
  }'
```

### 3. COE Creates Faculty
```bash
curl -X POST "http://localhost:8000/coe/faculty" \
  -H "Authorization: Bearer <coe_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "username": "jane_faculty",
    "password": "password123",
    "email": "jane@engcollege.edu",
    "institute_id": 1
  }'
```

## Frontend Integration

### Authentication Flow
1. User logs in via `/auth/login`
2. Store JWT token and user info
3. Include `Authorization: Bearer <token>` header in API calls
4. Use `/auth/me` to get current user info and roles

### Role-Based UI
- Use user roles to show/hide navigation items
- Implement route guards based on user permissions
- Display institute-specific information for COE and Faculty

## Security Considerations

### Production Deployment
1. **Change JWT Secret Key**: Update `SECRET_KEY` in `auth.py`
2. **Environment Variables**: Move sensitive data to `.env`
3. **Database Security**: Use proper database credentials
4. **HTTPS**: Enable SSL/TLS in production
5. **Password Policy**: Implement stronger password requirements

### Token Security
- JWT tokens are signed but not encrypted
- Include minimal necessary data in tokens
- Implement token refresh mechanism for longer sessions
- Consider token blacklisting for logout functionality

## Testing

### Unit Tests
Test each role's permissions:
- Superadmin can create institutes and COEs
- COE can only manage faculty for their institute
- Faculty can only access their assigned features

### Integration Tests
Test complete workflows:
- Institute creation -> COE assignment -> Faculty creation
- Cross-institute access restrictions
- JWT token authentication flow

## Future Enhancements

### Additional Features
1. **Permission System**: Fine-grained permissions beyond roles
2. **Audit Logging**: Track all user actions
3. **Multi-Tenancy**: Enhanced institute isolation
4. **Role Hierarchy**: Complex role inheritance
5. **Session Management**: Token refresh and blacklisting

### Scalability
1. **Database Optimization**: Indexes and query optimization
2. **Caching**: Redis for session and permission caching
3. **Load Balancing**: Multiple application servers
4. **Microservices**: Separate auth service

This RBAC system provides a solid foundation for secure, role-based access control in your question paper generation application.
