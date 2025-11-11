import React, { useState, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import Chatbot from './components/Chatbot'
import Auth from './components/Auth'
import './styles.css'

const UniversityInfo = () => (
  <div className="card">
    <h3>Integral University — Quick Info</h3>
    <div className="info-list">
      <div className="info-item"><b>Location</b>: Lucknow, Uttar Pradesh</div>
      <div className="info-item"><b>Programs</b>: B.Tech (CSE, ECE, Civil, Mechanical, Biotech), M.Tech, MBA, BBA, B.Pharm, and more</div>
      <div className="info-item"><b>Admissions</b>: Online portal — register, fill form, upload docs, pay fee</div>
      <div className="info-item"><b>Hostel</b>: Separate boys and girls hostels; charges vary by room & mess plan</div>
      <div className="info-item"><b>Placements</b>: Active Training & Placement Cell; packages vary by program/year</div>
    </div>
  </div>
)

const App = () => {
  const [token, setToken] = useState<string | null>(null)

  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      setToken(storedToken)
    }
  }, [])

  const handleLogin = (newToken: string) => {
    setToken(newToken)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    setToken(null)
  }

  return (
    <div className="app-wrap">
      <div className="navbar">
        <div className="brand">
          <div className="logo" />
          <div>
            <h1 style={{ margin: 0, fontSize: 18 }}>Integral University Chatbot</h1>
            <div className="subtitle">Ask about fees, hostel, placements, and admission process</div>
          </div>
        </div>
        {token && (
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        )}
      </div>

      {token ? (
        <div className="grid">
          <UniversityInfo />
          <div className="card" style={{ padding: 0 }}>
            <Chatbot token={token} />
          </div>
        </div>
      ) : (
        <div className="auth-page">
          <Auth onLogin={handleLogin} />
        </div>
      )}
    </div>
  )
}

const root = createRoot(document.getElementById('root')!)
root.render(<App />)