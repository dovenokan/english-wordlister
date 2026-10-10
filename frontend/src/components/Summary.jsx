const TYPE_LABELS = { verb: 'Verb', noun: 'Noun', adj: 'Adjective', phrverb: 'Phrasal verb', undef: 'Undefined' }
const LEVEL_LABELS = { a1: 'A1', a2: 'A2', b1: 'B1', b2: 'B2', c1: 'C1', other: 'Other' }

function Bar({ parts }) {
  const total = parts.reduce((sum, p) => sum + p.value, 0)
  return (
    <div className="bar" aria-hidden="true">
      {total > 0 &&
        parts
          .filter((p) => p.value > 0)
          .map((p) => (
            <span
              key={p.key}
              className={`bar-seg ${p.className}`}
              style={{ width: `${(p.value / total) * 100}%` }}
              title={`${p.label}: ${p.value.toLocaleString()}`}
            />
          ))}
    </div>
  )
}

export default function Summary({ stats, info }) {
  const { count, percentage, type, oxford } = stats
  const typeParts = ['verb', 'noun', 'adj', 'phrverb', 'undef'].map((key) => ({
    key,
    label: TYPE_LABELS[key],
    value: type[key] || 0,
    className: `t-${key}`,
  }))
  const levelParts = ['a1', 'a2', 'b1', 'b2', 'c1', 'other'].map((key) => ({
    key,
    label: LEVEL_LABELS[key],
    value: oxford[key] || 0,
    className: `l-${key}`,
  }))

  return (
    <section className="summary" aria-label="Summary">
      <div className="stat-grid">
        <Stat label="Tokens read" value={count.raw} hint={`from ${info.source}`} />
        <Stat label="Unique classified" value={count.total} hint={`${(info.time * 1000).toFixed(0)} ms`} />
        <Stat label="Typical words" value={`${percentage.typical}%`} hint="share of unique words that are classified" />
        <Stat label="Oxford A1–A2" value={`${percentage.oxford_A}%`} hint={`of leveled words · B ${percentage.oxford_B}% · C ${percentage.oxford_C}%`} />
      </div>

      <div className="bars">
        <div>
          <h3>By type</h3>
          <Bar parts={typeParts} />
          <Legend parts={typeParts} />
        </div>
        <div>
          <h3>By level</h3>
          <Bar parts={levelParts} />
          <Legend parts={levelParts} />
        </div>
      </div>
    </section>
  )
}

function Stat({ label, value, hint }) {
  return (
    <div className="stat">
      <span className="stat-label">{label}</span>
      <span className="stat-value">{typeof value === 'number' ? value.toLocaleString() : value}</span>
      <span className="stat-hint">{hint}</span>
    </div>
  )
}

function Legend({ parts }) {
  return (
    <ul className="legend">
      {parts.map((p) => (
        <li key={p.key}>
          <span className={`swatch ${p.className}`} />
          {p.label} <b>{p.value.toLocaleString()}</b>
        </li>
      ))}
    </ul>
  )
}
