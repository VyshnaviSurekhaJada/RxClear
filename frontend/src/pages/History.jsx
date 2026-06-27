import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Clock, FileDown, Trash2, RefreshCw, Pill } from 'lucide-react'

export default function History() {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState(null)

  const load = async () => {
    setLoading(true)
    try {
      const { data } = await axios.get('/history')
      setHistory(data.history)
    } catch {
      setError('Could not load history. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  const remove = async (id) => {
    await axios.delete(`/history/${id}`)
    setHistory(h => h.filter(r => r.id !== id))
  }

  useEffect(() => { load() }, [])

  return (
    <main style={{ maxWidth: 900, margin: '0 auto', padding: '36px 24px 64px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 28 }}>
        <div>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 28, fontWeight: 800, letterSpacing: '-0.5px' }}>
            Analysis History
          </h1>
          <p style={{ color: 'var(--muted)', fontSize: 14 }}>Recent prescription analyses</p>
        </div>
        <button onClick={load} style={{
          display: 'flex', alignItems: 'center', gap: 6,
          border: '1px solid var(--border)', background: 'var(--white)',
          padding: '8px 16px', borderRadius: 8, cursor: 'pointer', fontSize: 13,
        }}>
          <RefreshCw size={14} /> Refresh
        </button>
      </div>

      {loading && (
        <div style={{ textAlign: 'center', padding: 60, color: 'var(--muted)' }}>
          <RefreshCw size={28} style={{ animation: 'spin 1s linear infinite', marginBottom: 8 }} />
          <p>Loading history…</p>
        </div>
      )}

      {error && (
        <div style={{ background: 'var(--red-100)', color: 'var(--red-600)', borderRadius: 8, padding: 16 }}>
          {error}
        </div>
      )}

      {!loading && !error && history.length === 0 && (
        <div style={{
          textAlign: 'center', padding: '64px 24px',
          background: 'var(--white)', border: '1px solid var(--border)',
          borderRadius: 'var(--radius-lg)',
        }}>
          <Clock size={40} color="var(--border)" style={{ margin: '0 auto 12px' }} />
          <p style={{ fontWeight: 600, marginBottom: 4 }}>No analyses yet</p>
          <p style={{ color: 'var(--muted)', fontSize: 13 }}>Upload a prescription to get started.</p>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
        {history.map(record => (
          <div key={record.id} style={{
            background: 'var(--white)', border: '1px solid var(--border)',
            borderRadius: 'var(--radius-md)', padding: '18px 20px',
            display: 'flex', alignItems: 'center', gap: 16,
            boxShadow: 'var(--shadow-sm)',
          }}>
            {/* Icon */}
            <span style={{
              width: 44, height: 44, borderRadius: 10,
              background: 'var(--teal-50)', color: 'var(--teal-700)',
              display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
            }}>
              <Pill size={20} />
            </span>

            {/* Info */}
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontWeight: 600, fontSize: 14 }}>
                {record.patient_name || 'Unknown Patient'}
              </div>
              <div style={{ fontSize: 12, color: 'var(--muted)', marginTop: 2 }}>
                {new Date(record.timestamp).toLocaleString('en-IN')}
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 6 }}>
                {(record.medicines || []).map(m => (
                  <span key={m} style={{
                    fontSize: 11, padding: '2px 8px',
                    background: 'var(--teal-50)', color: 'var(--teal-700)',
                    borderRadius: 99, fontWeight: 500,
                  }}>{m}</span>
                ))}
              </div>
            </div>

            {/* Disease + confidence */}
            <div style={{ textAlign: 'right', flexShrink: 0 }}>
              <div style={{ fontWeight: 700, color: 'var(--teal-700)', fontSize: 13 }}>
                {record.disease || '—'}
              </div>
              <div style={{ fontSize: 11, color: 'var(--amber-500)', fontWeight: 600 }}>
                {record.confidence?.toFixed(1)}% confidence
              </div>
            </div>

            {/* Actions */}
            <div style={{ display: 'flex', gap: 8, flexShrink: 0 }}>
              <a href={`/report/${record.id}`} download style={{
                display: 'flex', alignItems: 'center', gap: 4,
                background: 'var(--teal-50)', color: 'var(--teal-700)',
                border: '1px solid var(--teal-100)',
                padding: '7px 12px', borderRadius: 7,
                textDecoration: 'none', fontSize: 12, fontWeight: 600,
              }}>
                <FileDown size={13} /> PDF
              </a>
              <button onClick={() => remove(record.id)} style={{
                display: 'flex', alignItems: 'center',
                background: 'var(--red-100)', color: 'var(--red-600)',
                border: 'none', padding: '7px 10px', borderRadius: 7,
                cursor: 'pointer',
              }}>
                <Trash2 size={13} />
              </button>
            </div>
          </div>
        ))}
      </div>

      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </main>
  )
}
