import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import SimplePage from './pages/SimplePage'

const pages = {
  home: ['Home', 'AI Resume Screening and Job Recommendation platform.'],
  login: ['Login', 'Authenticate using JWT token-based login.'],
  register: ['Register', 'Create account and manage profile securely.'],
  upload: ['Upload Resume', 'Upload PDF, DOCX, or TXT resumes up to 10 MB.'],
  prediction: ['Prediction', 'Predict best job category from resume text.'],
  ats: ['ATS Report', 'Get ATS score, matched skills, and deductions.'],
  compare: ['Job Comparison', 'Compare resume against job description and get suggestions.'],
  profile: ['Profile', 'View personal profile and upload history.'],
  history: ['History', 'Track previous predictions and ATS reports.'],
  admin: ['Admin Dashboard', 'Manage users, resumes, and platform statistics.'],
}

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<SimplePage title={pages.home[0]} description={pages.home[1]} />} />
        <Route path="/login" element={<SimplePage title={pages.login[0]} description={pages.login[1]} />} />
        <Route path="/register" element={<SimplePage title={pages.register[0]} description={pages.register[1]} />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload-resume" element={<SimplePage title={pages.upload[0]} description={pages.upload[1]} />} />
        <Route path="/prediction" element={<SimplePage title={pages.prediction[0]} description={pages.prediction[1]} />} />
        <Route path="/ats-report" element={<SimplePage title={pages.ats[0]} description={pages.ats[1]} />} />
        <Route path="/job-comparison" element={<SimplePage title={pages.compare[0]} description={pages.compare[1]} />} />
        <Route path="/profile" element={<SimplePage title={pages.profile[0]} description={pages.profile[1]} />} />
        <Route path="/history" element={<SimplePage title={pages.history[0]} description={pages.history[1]} />} />
        <Route path="/admin" element={<SimplePage title={pages.admin[0]} description={pages.admin[1]} />} />
      </Routes>
    </Layout>
  )
}
