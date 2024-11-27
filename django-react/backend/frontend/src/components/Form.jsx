import { useState } from "react"
import { useNavigate } from "react-router-dom"

const Form = ({route, method}) => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = () => {}

  return <form onSubmit={handleSubmit}></form>
}