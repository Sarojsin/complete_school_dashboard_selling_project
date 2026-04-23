Frontend Development Rules (React + Vite)
This document defines the rules for building the React frontend that will consume your modular FastAPI backend. It ensures consistency, maintainability, and smooth integration of existing HTML/CSS/JS assets.

1. Project Structure (Mirror Backend)
Your frontend should mirror the modular structure of your backend. This makes it easy to locate code for a feature.

text
frontend/
├── public/                     # static assets (favicon, images)
├── src/
│   ├── modules/                # feature-based modules (mirrors backend)
│   │   ├── auth/               # authentication
│   │   ├── school_teacher/     # teacher module
│   │   ├── school_student/     # student module
│   │   ├── school_parent/      # parent module
│   │   ├── ...                 # other modules
│   │   └── shared/             # shared across modules
│   │       ├── components/     # reusable UI (Button, Input, Modal)
│   │       ├── layouts/        # MainLayout, AuthLayout
│   │       ├── hooks/          # useLocalStorage, useDebounce
│   │       ├── utils/          # dateFormatter, validators
│   │       ├── styles/         # global CSS, variables
│   │       └── api/            # base axios instance, interceptors
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── .env
├── package.json
└── vite.config.js
Each backend module gets a corresponding folder under modules/.

Place code that is truly shared (like UI components, utilities) in shared/.

Keep module-specific code inside the module folder.

2. Integrating Existing HTML/CSS/JS
Your existing Jinja2 templates contain valuable HTML structure, CSS styling, and JavaScript functionality. Instead of rewriting everything, adapt them:

a. HTML → JSX
Copy the HTML structure into a React component.

Replace class attributes with className.

Change inline event handlers (onclick, onchange) to React synthetic events (onClick, onChange).

Use dangerouslySetInnerHTML only if absolutely necessary (e.g., for raw HTML from backend). Prefer standard JSX.

Example:

jsx
// Old HTML
<div class="card">
  <h2>Welcome, {{ user.name }}</h2>
  <button onclick="loadData()">Load</button>
</div>

// New JSX
<div className="card">
  <h2>Welcome, {user.name}</h2>
  <button onClick={loadData}>Load</button>
</div>
b. CSS
Global CSS – place existing CSS files in src/shared/styles/ and import them in main.jsx or in components. Example:

js
import './shared/styles/main.css';
CSS Modules – rename your CSS file to *.module.css to enable scoped styling. Then import as:

jsx
import styles from './styles/TeacherCard.module.css';
// use: className={styles.card}
Inline styles – avoid unless dynamic; use CSS classes instead.

c. JavaScript
Convert JavaScript functions into custom hooks or utility functions.

Use useEffect for DOM manipulations that used to be in <script> tags.

For AJAX calls, replace with Axios calls using the API client.

Example:

jsx
// Old JS (in a script tag)
function showNotification(msg) {
  alert(msg);
}

// New React hook
const useNotification = () => {
  const showNotification = (msg) => alert(msg);
  return { showNotification };
};
3. API Communication
Use Axios with a base instance configured in shared/api/client.js.

Set up interceptors to attach JWT tokens automatically.

Define API calls in each module’s api/ folder.

Example:

javascript
// src/shared/api/client.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
Teacher API:

javascript
// src/modules/school_teacher/api/teachers.js
import api from '../../../shared/api/client';

export const getTeachers = () => api.get('/school/teachers');
export const getTeacherProfile = () => api.get('/school/teachers/me');
4. Authentication Flow
Login Page – call POST /auth/login, store the token (preferably in localStorage or an httpOnly cookie). Use localStorage for simplicity during development.

Protected Routes – create a <PrivateRoute> component that checks for a token and redirects to login.

Logout – clear token and navigate to login.

Example:

jsx
// src/shared/components/PrivateRoute.jsx
import { Navigate } from 'react-router-dom';

export default function PrivateRoute({ children }) {
  const token = localStorage.getItem('access_token');
  return token ? children : <Navigate to="/login" />;
}
5. Routing
Use React Router DOM to define routes that mirror your API structure.

jsx
// src/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './modules/auth/pages/LoginPage';
import TeacherDashboard from './modules/school_teacher/pages/TeacherDashboard';
import StudentDashboard from './modules/school_student/pages/StudentDashboard';
import PrivateRoute from './shared/components/PrivateRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/teacher/*" element={<PrivateRoute><TeacherDashboard /></PrivateRoute>} />
        <Route path="/student/*" element={<PrivateRoute><StudentDashboard /></PrivateRoute>} />
        {/* other routes */}
      </Routes>
    </BrowserRouter>
  );
}
6. State Management
Server state – use TanStack Query (formerly React Query) for data fetching, caching, and background updates. It integrates perfectly with your async API.

Client state – use React hooks (useState, useReducer) for local UI state. For complex client state (e.g., global theme, user session), consider Zustand or Redux Toolkit, but start with React hooks.

Example with TanStack Query:

javascript
// src/modules/school_teacher/hooks/useTeachers.js
import { useQuery } from '@tanstack/react-query';
import { getTeachers } from '../api/teachers';

export const useTeachers = () => {
  return useQuery({
    queryKey: ['teachers'],
    queryFn: getTeachers,
  });
};
7. Development Proxy
To avoid CORS issues, configure Vite to proxy API requests to your FastAPI backend.

javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/auth': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
Now you can use relative URLs like /api/v1/school/teachers in your frontend.

8. Environment Variables
Store backend URL and other secrets in a .env file at the frontend root.

text
VITE_API_URL=http://localhost:8000/api/v1
Use import.meta.env.VITE_API_URL to access it. Never commit .env to version control.



9. Deployment
Build the React app: npm run build → output in dist/.

Serve the static files from your FastAPI backend using StaticFiles and fallback to index.html for SPA routing.

FastAPI example:

python
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# After all API routes
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    return FileResponse("frontend/dist/index.html")
10. Code Quality and Testing
Use ESLint and Prettier to enforce coding style.

Write unit tests for custom hooks and utilities using Vitest.

Write integration tests for pages and API calls using React Testing Library.

11. Final Rule: Keep Modular
Every new feature should be added as a new module under src/modules/. If code can be reused across modules, place it in shared/. Never put module‑specific code outside its folder.