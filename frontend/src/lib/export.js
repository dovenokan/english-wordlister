// Client-side exports: nothing is written to the server, so there are no shared files to clash.

const LEVEL_ORDER = ['a1', 'a2', 'b1', 'b2', 'c1', 'other']

function csvCell(value) {
  const text = String(value)
  return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text
}

function download(content, filename, mime) {
  const blob = new Blob([content], { type: `${mime};charset=utf-8` })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  setTimeout(() => URL.revokeObjectURL(url), 0)
}

function stamp() {
  return new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-')
}

export function exportCsv(words) {
  const rows = [['word', 'count', 'type', 'level'], ...words.map((w) => [w.word, w.count, w.type, w.oxford])]
  const content = rows.map((row) => row.map(csvCell).join(',')).join('\n')
  download(content, `wordlist-${stamp()}.csv`, 'text/csv')
}

export function exportTxt(words) {
  download(words.map((w) => w.word).join('\n'), `wordlist-${stamp()}.txt`, 'text/plain')
}

export function sortWords(words, key) {
  const copy = [...words]
  if (key === 'alphabet') {
    copy.sort((a, b) => a.word.localeCompare(b.word))
  } else if (key === 'level') {
    copy.sort((a, b) => LEVEL_ORDER.indexOf(a.oxford) - LEVEL_ORDER.indexOf(b.oxford) || b.count - a.count)
  } else {
    copy.sort((a, b) => b.count - a.count || a.word.localeCompare(b.word))
  }
  return copy
}
