// src/components/LoginForm.jsx
import { useState } from 'react'
import api from '../services/api' // 引入管家

function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = async (e) => {
    e.preventDefault()
    try {
      // 现在的请求变得异常清爽！
      const response = await api.post('/api/token/', { username, password })
      
      // 注意：Axios 把数据包在了 .data 里
      localStorage.setItem('access', response.data.access)
      localStorage.setItem('refresh', response.data.refresh)
      localStorage.setItem('username', username)
      onLoginSuccess(username)
    } catch (err) {
      alert("登录失败: 账号或密码错误")
    }
  }

  return (
    <form onSubmit={handleLogin} style={{ marginBottom: '20px' }}>
      <input type="text" placeholder="用户名" onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="密码" onChange={e => setPassword(e.target.value)} />
      <button type="submit">登录</button>
    </form>
  )
}

export default LoginForm