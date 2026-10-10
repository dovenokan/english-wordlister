import { useMemo, useState } from 'react'
import { exportCsv, exportTxt, sortWords } from '../lib/export.js'

const TYPES = [
  { key: 'verb', label: 'Verb' },
  { key: 'noun', label: 'Noun' },
  { key: 'adj', label: 'Adjective' },
  { key: 'phrverb', label: 'Phrasal verb' },
]
const LEVELS = ['a1', 'a2', 'b1', 'b2', 'c1', 'other']
const PAGE_SIZES = [25, 50, 100, 250]

function toggle(set, key) {
  const next = new Set(set)
  next.has(key) ? next.delete(key) : next.add(key)
  return next
}

export default function Results({ words }) {
  const [query, setQuery] = useState('')
  const [types, setTypes] = useState(() => new Set())
  const [levels, setLevels] = useState(() => new Set())
  const [sortKey, setSortKey] = useState('count')
  const [pageSize, setPageSize] = useState(50)
  const [page, setPage] = useState(1)

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase()
    const matches = words.filter(
      (w) =>
        (types.size === 0 || types.has(w.type)) &&
        (levels.size === 0 || levels.has(w.oxford)) &&
        (!needle || w.word.includes(needle)),
    )
    return sortWords(matches, sortKey)
  }, [words, query, types, levels, sortKey])

  const pageCount = Math.max(1, Math.ceil(filtered.length / pageSize))
  const current = Math.min(page, pageCount)
  const start = (current - 1) * pageSize
  const visible = filtered.slice(start, start + pageSize)

  const typeCounts = useMemo(() => {
    const counts = {}
    for (const w of words) counts[w.type] = (counts[w.type] || 0) + 1
    return counts
  }, [words])

  const resetPage = () => setPage(1)

  return (
    <section className="card results" aria-label="Word list">
      <div className="toolbar">
        <input
          type="search"
          className="search"
          placeholder="Search words…"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value)
            resetPage()
          }}
          aria-label="Search words"
        />
        <select
          value={sortKey}
          onChange={(e) => {
            setSortKey(e.target.value)
            resetPage()
          }}
          aria-label="Sort"
        >
          <option value="count">Sort: frequency</option>
          <option value="alphabet">Sort: A–Z</option>
          <option value="level">Sort: level</option>
        </select>
        <div className="export">
          <button onClick={() => exportCsv(filtered)} disabled={!filtered.length}>
            Export CSV
          </button>
          <button onClick={() => exportTxt(filtered)} disabled={!filtered.length}>
            Export TXT
          </button>
        </div>
      </div>

      <div className="chips" role="group" aria-label="Filter by type">
        {TYPES.map((t) => (
          <button
            key={t.key}
            className={`chip t-${t.key} ${types.has(t.key) ? 'on' : ''}`}
            aria-pressed={types.has(t.key)}
            onClick={() => {
              setTypes(toggle(types, t.key))
              resetPage()
            }}
          >
            {t.label} <span>{(typeCounts[t.key] || 0).toLocaleString()}</span>
          </button>
        ))}
      </div>
      <div className="chips" role="group" aria-label="Filter by level">
        {LEVELS.map((l) => (
          <button
            key={l}
            className={`chip l-${l} ${levels.has(l) ? 'on' : ''}`}
            aria-pressed={levels.has(l)}
            onClick={() => {
              setLevels(toggle(levels, l))
              resetPage()
            }}
          >
            {l.toUpperCase()}
          </button>
        ))}
        {(types.size > 0 || levels.size > 0 || query) && (
          <button
            className="link"
            onClick={() => {
              setTypes(new Set())
              setLevels(new Set())
              setQuery('')
              resetPage()
            }}
          >
            Reset filters
          </button>
        )}
      </div>

      <p className="muted count-line">
        Showing {filtered.length ? start + 1 : 0}–{Math.min(start + pageSize, filtered.length)} of{' '}
        {filtered.length.toLocaleString()} words
      </p>

      {visible.length === 0 ? (
        <p className="empty">No words match these filters.</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Word</th>
                <th className="num">Count</th>
                <th>Type</th>
                <th>Level</th>
              </tr>
            </thead>
            <tbody>
              {visible.map((w) => (
                <tr key={w.word}>
                  <td className="word">{w.word}</td>
                  <td className="num">{w.count.toLocaleString()}</td>
                  <td>
                    <span className={`tag t-${w.type}`}>{w.type === 'phrverb' ? 'phrasal' : w.type}</span>
                  </td>
                  <td>
                    <span className={`tag l-${w.oxford}`}>{w.oxford.toUpperCase()}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="pager">
        <label className="muted">
          Per page{' '}
          <select
            value={pageSize}
            onChange={(e) => {
              setPageSize(Number(e.target.value))
              resetPage()
            }}
          >
            {PAGE_SIZES.map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
        </label>
        <div className="pager-buttons">
          <button onClick={() => setPage(1)} disabled={current === 1}>
            «
          </button>
          <button onClick={() => setPage(current - 1)} disabled={current === 1}>
            Previous
          </button>
          <span className="muted">
            Page {current} of {pageCount}
          </span>
          <button onClick={() => setPage(current + 1)} disabled={current >= pageCount}>
            Next
          </button>
          <button onClick={() => setPage(pageCount)} disabled={current >= pageCount}>
            »
          </button>
        </div>
      </div>
    </section>
  )
}
