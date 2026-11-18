# Library.io Frontend

Modern, responsive React + Vite digital library interface and AI recommendation dashboard.

---

## 🛠 Tech Stack

- **Framework:** React 18 + Vite
- **Routing:** React Router v6
- **Styling:** Tailwind CSS + PostCSS
- **Icons:** Lucide React
- **API Client:** Axios (with centralized JWT interceptors & token refresh)
- **Charts:** Chart.js & react-chartjs-2

---

## 🚀 Setup & Execution

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

---

## 🧭 Routes Structure

### Public:
- `/login` - Member & Staff sign-in
- `/register` - Student self-registration

### Student (Protected):
- `/dashboard` - Overview, KPI counters, AI picks preview, active loans
- `/library` - Interactive book catalog with live search, genre pills, and rating filters
- `/books/:id` - Full book details, 1-click borrow, review submission
- `/my-books` - Active loans with due dates, 1-click return, 7-day renewal
- `/recommendations` - Full AI recommendations with algorithm confidence badges and explanations
- `/analytics` - Visual reading charts (top categories, reading status)
- `/history` - Activity timeline (views, borrows, returns, reviews)
- `/profile` - Digital library membership card & profile settings

### Staff / Librarian (Protected):
- `/admin` - Operational dashboard
- `/admin/books` - Book inventory manager & Add Book modal
- `/admin/members` - Member directory & borrow limits
- `/admin/loans` - Master circulation records
- `/admin/overdue` - Overdue tracker & fine settlement desk
- `/admin/analytics` - Institutional stock distribution & circulation charts
