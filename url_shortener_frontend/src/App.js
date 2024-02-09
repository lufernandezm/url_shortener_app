import React, { useState } from 'react';

function App() {
  const [url, setUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [error, setError] = useState(null);

  const validateUrl = (url) => {
    const urlRegex = /^(ftp|http|https):\/\/[^ "]+$/;
    return urlRegex.test(url);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateUrl(url)) {
      setError('Invalid URL');
      setShortUrl(undefined)
      return;
    }
    try {
      const response = await fetch('http://localhost:8000/shorten', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url })
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setShortUrl(data.shortUrl);
      setError(null);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="text" value={url} onChange={(e) => setUrl(e.target.value)} />
        <button type="submit">Shorten</button>
      </form>
      {shortUrl && <a href={shortUrl} target="_blank" rel="noopener noreferrer">{shortUrl}</a>}
      {error && <p>{error}</p>}
    </div>
  );
}

export default App;