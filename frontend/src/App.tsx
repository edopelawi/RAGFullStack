import { useMemo, useState } from 'react'

type RetrievedContext = {
  id: string
  content: string
  metadata?: Record<string, unknown>
  score?: number | null
}

type QueryResponse = {
  answer: string
  contexts: RetrievedContext[]
}

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export default function App() {
  const [question, setQuestion] = useState('')
  const [model, setModel] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [response, setResponse] = useState<QueryResponse | null>(null)

  const subtitle = useMemo(() => `Backend: ${apiBase}`, [])

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    setLoading(true)
    setError(null)
    setResponse(null)

    try {
      const res = await fetch(`${apiBase}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, model: model || undefined }),
      })

      if (!res.ok) {
        const text = await res.text()
        throw new Error(text || `Request failed with status ${res.status}`)
      }

      const data = (await res.json()) as QueryResponse
      setResponse(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ maxWidth: 860, margin: '0 auto', padding: '2rem', fontFamily: 'Inter, system-ui, sans-serif' }}>
      <header style={{ marginBottom: '1.5rem' }}>
        <h1 style={{ margin: 0 }}>RAG Full Stack</h1>
        <p style={{ margin: '0.25rem 0', color: '#555' }}>{subtitle}</p>
      </header>

      <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '0.75rem' }}>
        <label style={{ display: 'grid', gap: '0.35rem' }}>
          <span>Question</span>
          <textarea
            required
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            rows={3}
            style={{ padding: '0.75rem', fontSize: '1rem' }}
            placeholder="Ask anything about your ingested docs"
          />
        </label>

        <label style={{ display: 'grid', gap: '0.35rem' }}>
          <span>Model (optional override)</span>
          <input
            value={model}
            onChange={(e) => setModel(e.target.value)}
            placeholder="gpt-4o-mini"
            style={{ padding: '0.6rem', fontSize: '1rem' }}
          />
        </label>

        <button type="submit" disabled={loading} style={{ padding: '0.75rem 1rem', fontSize: '1rem' }}>
          {loading ? 'Sending...' : 'Ask'}
        </button>
      </form>

      {error && (
        <p style={{ color: 'red', marginTop: '1rem' }}>
          Error: {error}
        </p>
      )}

      {response && (
        <section style={{ marginTop: '1.5rem', display: 'grid', gap: '1rem' }}>
          <div>
            <h2 style={{ margin: '0 0 0.5rem 0' }}>Answer</h2>
            <p style={{ whiteSpace: 'pre-wrap' }}>{response.answer}</p>
          </div>

          <div>
            <h3 style={{ margin: '0 0 0.5rem 0' }}>Contexts</h3>
            <ul style={{ paddingLeft: '1.2rem', display: 'grid', gap: '0.6rem' }}>
              {response.contexts.map((ctx, idx) => (
                <li key={ctx.id || idx}>
                  <strong>[{idx + 1}]</strong>{' '}
                  <span style={{ color: '#555' }}>{ctx.metadata ? JSON.stringify(ctx.metadata) : ''}</span>
                  <div style={{ whiteSpace: 'pre-wrap', marginTop: '0.25rem' }}>{ctx.content}</div>
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}
    </main>
  )
}
