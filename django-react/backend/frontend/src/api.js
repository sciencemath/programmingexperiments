import { ACCESS_TOKEN } from "./constants"

/**
 * 
 * @param {string} url 
 * @param {string} method 
 * @param {{}} body 
 * @returns 
 */
const api = (url, method = 'GET', body) => {
  const token = localStorage.getItem(ACCESS_TOKEN)
  try {
    fetch(`${import.meta.env.VITE_API_URL}/${url}`, {
      method,
      headers: {
        'Authorization': `Bearer ${token}`
      },
      ...(body && body),
    })
  } catch (error) {
    return error
    // throw new Error(error)
  }
}

export default api