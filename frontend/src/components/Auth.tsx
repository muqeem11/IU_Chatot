import React, { useState } from 'react'
import Login from './Login'
import Register from './Register'

type AuthProps = {
  onLogin: (token: string) => void
}

const Auth: React.FC<AuthProps> = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true)

  const handleSwitchToLogin = () => setIsLogin(true)

  return (
    <div className="auth-container">
      {isLogin ? (
        <Login onLogin={onLogin} />
      ) : (
        <Register onRegister={handleSwitchToLogin} />
      )}
      <p>
        {isLogin ? "Don't have an account? " : 'Already have an account? '}
        <button className="link-button" onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? 'Register' : 'Login'}
        </button>
      </p>
    </div>
  )
}

export default Auth