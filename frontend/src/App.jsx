import { useCallback, useEffect, useState } from 'react'
import InputPanel from './components/InputPanel.jsx'
import Results from './components/Results.jsx'
import Summary from './components/Summary.jsx'
import { analyse, checkServer } from './lib/api.js'

const TEXT_KEY = 'wordlister.text'

// Remembering the last text is a per-browser convenience, so failures are ignored.
function readStoredText() {
  try {
    return localStorage.getItem(TEXT_KEY) || ''
  } catch {
    return ''
  }
}

function storeText(value) {
  try {
    localStorage.setItem(TEXT_KEY, value)
  } catch {
    /* storage unavailable (private mode, quota): the app still works */
  }
}

export default function App() {
  const [mode, setMode] = useState('text')
  const [text, setText] = useState(readStoredText)
  const [file, setFile] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)
  const [online, setOnline] = useState(null)

  useEffect(() => {
    storeText(text)
  }, [text])

  useEffect(() => {
    checkServer().then(setOnline)
  }, [])

  const run = useCallback(async () => {
    if (mode === 'file' && !file) {
      setError('Choose a file first.')
      return
    }
    if (mode === 'text' && !text.trim()) {
      setError('Paste some text first.')
      return
    }
    setBusy(true)
    setError('')
    try {
      setResult(await analyse(mode === 'file' ? { file } : { text }))
      setOnline(true)
    } catch (err) {
      setError(err.message)
      if (err instanceof TypeError) setOnline(false)
    } finally {
      setBusy(false)
    }
  }, [mode, text, file])

  const clear = () => {
    if (mode === 'file') {
      setFile(null)
    } else {
      setText('')
      setResult(null)
    }
    setError('')
  }

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <h1>English Wordlister</h1>
          <p className="muted">Classify the words of any text by part of speech and Oxford level, entirely on this machine.</p>
        </div>
        <span className={`status ${online === false ? 'bad' : online ? 'ok' : ''}`}>
          {online === null ? 'Checking server…' : online ? 'Local server running' : 'Server unreachable'}
        </span>
      </header>

      <main className="layout">
        <InputPanel
          mode={mode}
          setMode={(next) => {
            setMode(next)
            setError('')
          }}
          text={text}
          setText={setText}
          file={file}
          setFile={setFile}
          busy={busy}
          error={error}
          onAnalyse={run}
          onClear={clear}
          hasResult={Boolean(result)}
        />

        <div className="output">
          {result ? (
            <>
              <Summary stats={result.stats} info={result.info} />
              <Results words={result.wordlist} />
            </>
          ) : (
            <section className="card placeholder">
              <h2>No results yet</h2>
              <p className="muted">Paste text or upload a file, then press Analyse. Results appear here with filters, search and export.</p>
            </section>
          )}
        </div>
      </main>
    </div>
  )
}
