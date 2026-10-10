// Talks to the local Flask server. In dev, Vite proxies /api to it; in production
// Flask serves the built UI from the same origin, so relative URLs always work.

export async function analyse({ text, file }) {
  const body = new FormData()
  if (file) {
    body.append('file', file)
  } else {
    body.append('text', text)
  }

  const res = await fetch('/api/analyze', { method: 'POST', body })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    throw new Error(data.error || `Analysis failed (${res.status})`)
  }
  return data
}

export async function checkServer() {
  try {
    const res = await fetch('/api/health')
    return res.ok
  } catch {
    return false
  }
}
