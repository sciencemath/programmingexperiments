import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants"
import api from "../api"
import "../styles/Form.css"

const Form = ({route, method}) => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (event) => {
    setIsLoading(true)
    event.preventDefault()

    try {
      const res = await api(route, 'post', {username, password})
      if (method !== 'login') {
        navigate('/login')
        return
      }
      localStorage.setItem(ACCESS_TOKEN, res.access)
      localStorage.setItem(REFRESH_TOKEN, res.refresh)
      navigate('/')
      
    } catch (error) {
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  return <form onSubmit={handleSubmit} className="form-container">
    <h1>{method}</h1>
    <input
      className="form-input"
      type="text"
      value={username}
      onChange={(e) => setUsername(e.target.value)}
      placeholder="Username"
    />
    <input
      className="form-input"
      type="password"
      value={password}
      onChange={(e) => setPassword(e.target.value)}
      placeholder="Password"
    />
    <button className="form-button" type="submit">
      {method}
    </button>
  </form>
}

export default Form