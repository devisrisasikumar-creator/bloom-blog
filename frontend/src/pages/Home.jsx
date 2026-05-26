import { useEffect, useState } from 'react'
import axios from 'axios'

function Home() {
  const [posts, setPosts] = useState([])

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/posts')
      .then(response => {
        setPosts(response.data)
      })
  }, [])

  return (
  <div>
    <div className="flower">🌸</div>

    <h2>All Blog Posts</h2>

    {posts.map(post => (
      <div key={post.id} className="post-card">
        <h3>{post.title}</h3>
        <p>{post.content}</p>
      </div>
    ))}
  </div>
)
}

export default Home