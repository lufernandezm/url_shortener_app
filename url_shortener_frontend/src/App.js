import React, { useState } from 'react';
import './App.css'

function App() {
  const [url, setUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [error, setError] = useState(null);
  const [visits, setVisits] = useState('');

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

  const handleVisits = async (event) => {
    event.preventDefault();
    try {
      const shortUrlId = shortUrl.split('/').pop()
      console.log('shortUrlId', shortUrlId)
      const response = await fetch(`http://localhost:8000/short_url_visits/${shortUrlId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log('data', data)
      setVisits(data.visits);
      setError(null);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="app">
      <h2 className="title">URL Shortener</h2>
      <form onSubmit={handleSubmit}>
        <input className="input" type="text" value={url} onChange={(e) => setUrl(e.target.value)} placeholder='Enter URL here.' />
        <button className="button" type="submit">Shorten</button>
      </form>
      <div>
        {shortUrl && <a className="space" href={shortUrl} target="_blank" rel="noopener noreferrer">{shortUrl}</a>}
        <button className="space" onClick={handleVisits}>Count visits: </button><span>{visits}</span>
      </div>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;