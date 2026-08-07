import { Link } from 'react-router-dom'

const links = [
  ['/', 'Home'],
  ['/login', 'Login'],
  ['/register', 'Register'],
  ['/dashboard', 'Dashboard'],
  ['/upload-resume', 'Upload Resume'],
  ['/prediction', 'Prediction'],
  ['/ats-report', 'ATS Report'],
  ['/job-comparison', 'Job Comparison'],
  ['/profile', 'Profile'],
  ['/history', 'History'],
  ['/admin', 'Admin Dashboard'],
]

export default function Layout({ children }) {
  return (
    <div className="min-h-screen">
      <nav className="bg-indigo-600 text-white p-4 flex flex-wrap gap-4">
        {links.map(([to, label]) => (
          <Link key={to} to={to} className="hover:underline text-sm">{label}</Link>
        ))}
      </nav>
      <main className="p-6 max-w-6xl mx-auto">{children}</main>
    </div>
  )
}
