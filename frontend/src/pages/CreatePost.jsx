import { useState } from 'react'
import axios from 'axios'

function CreatePost() {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')

  const handlePost = async (e) => {
    e.preventDefault()

    const token = localStorage.getItem('token')

    await axios.post(
      'http://127.0.0.1:5000/posts',
      {
        title,
        content
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    alert('Post Created')
  }

  return (
    <form onSubmit={handlePost}>
      <h2>Create Blog Post</h2>

      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <br /><br />

      <textarea
        placeholder="Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />

      <br /><br />

      <button type="submit">Create</button>
    </form>
  )
}

export default CreatePost