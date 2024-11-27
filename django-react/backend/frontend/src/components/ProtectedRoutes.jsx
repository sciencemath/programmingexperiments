import { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { jwtDecode } from 'jwt-decode'
import api from '../api'
import { REFRESH_TOKEN, ACCESS_TOKEN } from '../constants'

const ProtectedRoute = ({children}) => {
  const [isAuthorized, setIsAuthorized] = useState(null)

  useEffect(() => {
    auth().catch(() => setIsAuthorized(false))
  }, [])

  const refreshToken = async () => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN)
    try {
      const res = await api('/api/token/refresh/',
        'POST',
        { refresh: refreshToken }
      )

      localStorage.setItem(ACCESS_TOKEN, res.data.access)
      setIsAuthorized(true)
    } catch (error) {
      console.error(error)
      setIsAuthorized(false)
    }
  }

  const auth = async () => {
    const token = localStorage.getItem(ACCESS_TOKEN)
    if (!token) {
      setIsAuthorized(false)
      return
    }
    const decoded = jwtDecode(token)
    const tokenExpiration = decoded.exp
    const now = Date.now() / 1000
    (tokenExpiration < now) ? await refreshToken() : setIsAuthorized(true)
  }

  if (isAuthorized === null) return <div>Loading...</div>
  return isAuthorized ? children : <Navigate to="/login" />
}

export default ProtectedRoute