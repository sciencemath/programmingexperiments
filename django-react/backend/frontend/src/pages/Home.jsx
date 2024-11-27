import { useEffect, useState } from "react";
import api from "../api";

const Home = () => {
  const [notes, setNotes] = useState([])
  const [content, setContent] = useState('')
  const [title, setTitle] = useState('')

  useEffect(() => {
    fetchNotes()
  }, [])

  const fetchNotes = async () => {
    try {
      const response = await api('/api/notes')
      setNotes(response)
    } catch (error) {
      console.error(error)
    }
  }

  const onDeleteNote = async (id) => {
    try {
      const response = await api(`/api/notes/delete/${id}`)
      console.log('note deleted')
    } catch (error) {
      console.error(error)
    }
    // hack for now lets upgrade react 19 and use useOptimistic for this
    fetchNotes()
  }

  const onCreateNote = async (event) => {
    event.preventDefault()
    try {
      const response = await api('/api/notes', 'post', { content, title })
      console.log('note created')
    } catch (error) {
      console.error(error)
    }
    // hack for now lets upgrade react 19 and use useOptimistic for this
    fetchNotes()
  }

  return <div><div>
      <h2>Notes</h2>
    </div>
      <h2>Create a Note</h2>
      <form onSubmit={onCreateNote}>
        <label htmlFor="title">Title:</label>
        <br />
        <input
          type="text"
          id="title"
          name="title"
          required
          onChange={(e) => setTitle(e.target.value)}
          value={title}
        />
        <label htmlFor="content">Content:</label>
        <br />
        <textarea
          id="content"
          name="content"
          required
          value={content}
          onChange={(e) => setContent(e.target.value)}
        ></textarea>
        <br />
        <input type="submit" value="Submit"></input>
      </form>
    </div>
}

export default Home;