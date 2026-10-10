import { useRef, useState } from 'react'

const ACCEPTED = ['txt', 'srt', 'md', 'csv']
const MAX_BYTES = 16 * 1024 * 1024

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export default function InputPanel({ mode, setMode, text, setText, file, setFile, busy, error, onAnalyse, onClear, hasResult }) {
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)
  const [localError, setLocalError] = useState('')

  const acceptFile = (picked) => {
    if (!picked) return
    const ext = picked.name.split('.').pop().toLowerCase()
    if (!ACCEPTED.includes(ext)) {
      setLocalError(`Unsupported file type .${ext}. Use ${ACCEPTED.join(', ')}.`)
      return
    }
    if (picked.size > MAX_BYTES) {
      setLocalError('File is larger than 16 MB.')
      return
    }
    setLocalError('')
    setFile(picked)
    setMode('file')
  }

  const onDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    acceptFile(e.dataTransfer.files[0])
  }

  const onKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault()
      onAnalyse()
    }
  }

  const shownError = localError || error

  return (
    <section className="card input-card" aria-label="Input">
      <div className="tabs" role="tablist">
        <button role="tab" aria-selected={mode === 'text'} className={mode === 'text' ? 'tab active' : 'tab'} onClick={() => setMode('text')}>
          Paste text
        </button>
        <button role="tab" aria-selected={mode === 'file'} className={mode === 'file' ? 'tab active' : 'tab'} onClick={() => setMode('file')}>
          Upload file
        </button>
      </div>

      {mode === 'text' ? (
        <div className="field">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="Paste or type English text here…"
            spellCheck="false"
            aria-label="Text to analyse"
          />
          <div className="field-foot">
            <span className="muted">{text.trim() ? `${text.trim().split(/\s+/).length.toLocaleString()} words` : 'Ctrl/⌘ + Enter to analyse'}</span>
            <button className="link" onClick={onClear} disabled={!text && !hasResult}>
              Clear
            </button>
          </div>
        </div>
      ) : (
        <div
          className={`dropzone ${dragging ? 'dragging' : ''}`}
          onDragOver={(e) => {
            e.preventDefault()
            setDragging(true)
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={onDrop}
          onClick={() => inputRef.current?.click()}
          onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && inputRef.current?.click()}
          role="button"
          tabIndex={0}
        >
          <input
            ref={inputRef}
            type="file"
            accept={ACCEPTED.map((ext) => `.${ext}`).join(',')}
            hidden
            onChange={(e) => {
              acceptFile(e.target.files[0])
              e.target.value = ''
            }}
          />
          {file ? (
            <div className="file-chosen">
              <strong>{file.name}</strong>
              <span className="muted">{formatBytes(file.size)}</span>
              <button
                className="link"
                onClick={(e) => {
                  e.stopPropagation()
                  setFile(null)
                }}
              >
                Remove
              </button>
            </div>
          ) : (
            <div className="dropzone-hint">
              <strong>Drop a file here</strong>
              <span className="muted">or click to browse · {ACCEPTED.join(', ')} · up to 16 MB</span>
              <span className="muted small">Subtitle (.srt) timings and markup are stripped automatically.</span>
            </div>
          )}
        </div>
      )}

      {shownError && <p className="error" role="alert">{shownError}</p>}

      <button className="primary" onClick={onAnalyse} disabled={busy}>
        {busy ? 'Analysing…' : 'Analyse'}
      </button>
    </section>
  )
}
