import { ACCESS_TOKEN } from "./constants"

/**
 * 
 * @param {string} url 
 * @param {string} method 
 * @param {{}} body 
 * @returns 
 */
const api = async (url, method = 'GET', body = false) => {
  const token = localStorage.getItem(ACCESS_TOKEN)
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}${url}/`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...(token && {'Authorization': `Bearer ${token}`})
      },
      ...(body && {body: JSON.stringify(body) }),
    })
    return await res.json()
  } catch (error) {
    return error
    // throw new Error(error)
  }
}

export default api