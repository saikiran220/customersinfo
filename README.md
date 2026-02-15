# User Data Entry - Full Stack Project

A simple full-stack application with React (Vite) frontend and FastAPI backend, connected to Supabase.

## Project Structure

```
dataentry/
├── frontend/          # React + Vite app
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/           # FastAPI app
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── .env.example
└── README.md
```

## Supabase Setup

### 1. Create a Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign in
2. Create a new project
3. Wait for the project to be provisioned

### 2. Create the `users` Table

Run this SQL in the Supabase SQL Editor (Dashboard → SQL Editor):

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  father_name TEXT NOT NULL,
  mobile_no TEXT NOT NULL
);
```

### 3. Get API Credentials

1. Go to **Project Settings** → **API**
2. Copy the **Project URL** (SUPABASE_URL)
3. Copy the **anon public** key (SUPABASE_KEY)

## Environment Variables

### Backend (.env in backend folder)

Create `backend/.env`:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

### Frontend (.env in frontend folder)

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

## Installation

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## How to Run

### 1. Start the Backend

```bash
cd backend
# Activate venv first if not already active
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at: http://localhost:8000

### 2. Start the Frontend

Open a new terminal:

```bash
cd frontend
npm run dev
```

Frontend runs at: http://localhost:5173

### 3. Test the App

1. Open http://localhost:5173 in your browser
2. Fill in the form: Name, Father Name, Mobile Number (10 digits)
3. Click Submit
4. Check your Supabase table for the new row

## API

### POST /users

Creates a new user in the database.

**Request Body:**
```json
{
  "name": "John Doe",
  "father_name": "Robert Doe",
  "mobile_no": "9876543210"
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "data": [...]
}
```

## Validation Rules

- **Name:** Required
- **Father Name:** Required  
- **Mobile Number:** Required, exactly 10 digits
