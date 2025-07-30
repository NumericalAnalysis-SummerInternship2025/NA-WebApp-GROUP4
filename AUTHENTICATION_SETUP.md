# Authentication System Setup

## Overview

The authentication system has been successfully integrated with the database for user registration and login functionality.

## Features Implemented

### Backend (Python/FastAPI)
- ✅ User registration with password hashing
- ✅ User login with password verification
- ✅ Password security using SHA-256 with salt
- ✅ Duplicate email prevention
- ✅ User role management (professeur/etudiant)

### Frontend (React/TypeScript)
- ✅ Registration form with validation
- ✅ Login form with validation
- ✅ Authentication context for state management
- ✅ Protected routes
- ✅ User session persistence
- ✅ Logout functionality
- ✅ Role-based access control

## Database Schema

The `utilisateur` table includes:
- `id_utilisateur` (Primary Key)
- `nom` (Full name)
- `email` (Unique)
- `mot_de_passe` (Hashed password)
- `role` (professeur/etudiant)
- `date_creation` (Timestamp)
- `derniere_connexion` (Timestamp)
- `actif` (Boolean)

## API Endpoints

### User Registration
```
POST /users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "professeur"
}
```

### User Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

## How to Use

### 1. Start the Backend
```bash
cd backend
python -m uvicorn main:app --reload
```

### 2. Start the Frontend
```bash
npm install
npm run dev
```

### 3. Register a New User
1. Navigate to `/auth`
2. Click on "Inscription" tab
3. Fill in the form:
   - Prénom (First name)
   - Nom (Last name)
   - Email
   - Rôle (Role: professeur or etudiant)
   - Mot de passe (Password)
   - Confirmer le mot de passe (Confirm password)
4. Click "Créer mon compte"

### 4. Login
1. Navigate to `/auth`
2. Click on "Connexion" tab
3. Enter your email and password
4. Click "Se connecter"

### 5. Access Protected Pages
- `/modules` - Requires authentication
- `/module/:id` - Requires authentication
- `/module-wizard` - Requires professeur role

## Security Features

- **Password Hashing**: Passwords are hashed using SHA-256 with a random salt
- **Input Validation**: Frontend and backend validation for all inputs
- **Duplicate Prevention**: Email addresses must be unique
- **Session Management**: User sessions persist across browser refreshes
- **Role-Based Access**: Different access levels for professors and students

## File Structure

```
src/
├── components/
│   ├── AuthPage.tsx          # Registration/Login form
│   ├── ProtectedRoute.tsx    # Route protection component
│   └── AppSidebar.tsx        # Sidebar with logout
├── contexts/
│   └── AuthContext.tsx       # Authentication state management
└── App.tsx                   # Main app with AuthProvider

backend/
├── main.py                   # FastAPI server with auth endpoints
├── database.py              # Database management
└── models.py                # Pydantic models
```

## Testing the System

1. **Register as a Professor**:
   - Use role "professeur"
   - Access `/module-wizard` (should work)

2. **Register as a Student**:
   - Use role "etudiant"
   - Try to access `/module-wizard` (should redirect to home)

3. **Test Login/Logout**:
   - Login with registered credentials
   - Check sidebar shows user name
   - Click logout to sign out

## Error Handling

The system handles various error scenarios:
- Invalid email format
- Password mismatch
- Duplicate email registration
- Invalid login credentials
- Missing required fields
- Network errors

All errors are displayed to the user via toast notifications. 