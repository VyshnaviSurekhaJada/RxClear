import React, { useState } from 'react'
import axios from 'axios'
import { Search, Pill, AlertTriangle, ShieldCheck, Info } from 'lucide-react'

const InfoRow = ({ label, value }) => {
  if (!value || value === 'N/A') return null
  return (
    <div style={{ display: 'flex', gap: 10, padding: '6px 0', borderBottom: '1px solid var(--border)', fontSize: 13 }}>
      <span style={{ color: 'var(--muted)', minWidth: 140, fontWeight: 500 }}>{label}</span>
      <span style={{ color: 'var(--ink-light)' }}>{value}</span>
    </div>
  )
}

export default function MedicineSearch() {
  const [query,   setQuery]   = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)
  const [expanded, setExpanded] = useState(null)

  const search = async (e) => {
    e?.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    try {
      const { data } = await axios.get(`/medicines?q=${encodeURIComponent(query)}`)
      setResults(data.results)
      setSearched(true)
    } catch {
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ maxWidth: 900, margin: '0 auto', padding: '36px 24px 64px' }}>
      <h1 style={{
        fontFamily: 'var(--font-display)', fontSize: 28, fontWeight: 800,
        letterSpacing: '-0.5px', marginBottom: 6,
      }}>Medicine Database</h1>
      <p style={{ color: 'var(--muted)', fontSize: 14, marginBottom: 28 }}>
        Search for any medicine to view uses, dosage, side effects and interactions.
      </p>

      {/* Search bar */}
      <form onSubmit={search} style={{ display: 'flex', gap: 10, marginBottom: 32 }}>
        <div style={{ flex: 1, position: 'relative' }}>
          <Search size={16} style={{
            position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)',
            color: 'var(--muted)',
          }} />
          <input
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="e.g. Paracetamol, Metformin, Azithromycin…"
            style={{
              width: '100%', padding: '12px 14px 12px 40px',
              border: '1.5px solid var(--border)', borderRadius: 10,
              fontSize: 14, outline: 'none', background: 'var(--white)',
              color: 'var(--ink)',
              transition: 'border-color var(--transition)',
            }}
            onFocus={e => e.target.style.borderColor = 'var(--teal-500)'}
            onBlur={e => e.target.style.borderColor = 'var(--border)'}
          />
        </div>
        <button type="submit" disabled={loading || !query.trim()} style={{
          background: 'linear-gradient(135deg, var(--teal-700), var(--teal-500))',
          color: 'var(--white)', border: 'none',
          padding: '12px 24px', borderRadius: 10,
          fontWeight: 600, fontSize: 14, cursor: 'pointer',
          opacity: loading || !query.trim() ? 0.6 : 1,
        }}>
          {loading ? 'Searching…' : 'Search'}
        </button>
      </form>

      {/* Results */}
      {searched && results.length === 0 && (
        <div style={{
          textAlign: 'center', padding: '48px 24px',
          background: 'var(--white)', border: '1px solid var(--border)',
          borderRadius: 'var(--radius-lg)',
        }}>
          <Pill size={36} color="var(--border)" style={{ margin: '0 auto 12px' }} />
          <p style={{ fontWeight: 600 }}>No medicines found for "{query}"</p>
          <p style={{ color: 'var(--muted)', fontSize: 13 }}>Try a different name or generic name.</p>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
        {results.map((med, i) => (
          <div key={i} style={{
            background: 'var(--white)', border: '1px solid var(--border)',
            borderRadius: 'var(--radius-lg)', overflow: 'hidden',
            boxShadow: 'var(--shadow-sm)',
          }}>
            {/* Header */}
            <button onClick={() => setExpanded(expanded === i ? null : i)} style={{
              width: '100%', background: 'none', border: 'none',
              padding: '18px 20px', cursor: 'pointer', textAlign: 'left',
              display: 'flex', alignItems: 'center', gap: 14,
            }}>
              <span style={{
                width: 44, height: 44, borderRadius: 10, flexShrink: 0,
                background: 'var(--teal-50)', color: 'var(--teal-700)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
              }}>
                <Pill size={20} />
              </span>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 700, fontSize: 16 }}>{med.name}</div>
                <div style={{ fontSize: 12, color: 'var(--muted)', marginTop: 1 }}>
                  {med.generic_name} · {med.category}
                </div>
              </div>
              <span style={{
                fontSize: 11, fontWeight: 600,
                background: 'var(--teal-50)', color: 'var(--teal-700)',
                borderRadius: 99, padding: '3px 12px',
              }}>{med.category}</span>
            </button>

            {/* Expanded details */}
            {expanded === i && (
              <div style={{ padding: '0 20px 20px', borderTop: '1px solid var(--border)' }}>
                {/* Uses */}
                <div style={{
                  marginTop: 12, marginBottom: 16,
                  padding: 12, background: 'var(--teal-50)',
                  borderRadius: 8, display: 'flex', gap: 10,
                }}>
                  <Info size={14} color="var(--teal-700)" style={{ flexShrink: 0, marginTop: 2 }} />
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--teal-700)', marginBottom: 2 }}>USES</div>
                    <div style={{ fontSize: 13, color: 'var(--ink-light)' }}>{med.uses}</div>
                  </div>
                </div>

                <InfoRow label="Generic Name"     value={med.generic_name} />
                <InfoRow label="Category"         value={med.category} />
                <InfoRow label="Max Adult Dose"   value={med.max_adult_dose} />
                <InfoRow label="Max Child Dose"   value={med.max_child_dose} />

                {/* Side effects */}
                {med.side_effects && (
                  <div style={{
                    marginTop: 14, padding: 12,
                    background: 'var(--orange-100)', borderRadius: 8,
                    display: 'flex', gap: 10,
                  }}>
                    <AlertTriangle size={14} color="var(--orange-500)" style={{ flexShrink: 0, marginTop: 2 }} />
                    <div>
                      <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--orange-500)', marginBottom: 2 }}>SIDE EFFECTS</div>
                      <div style={{ fontSize: 13, color: 'var(--ink-light)' }}>{med.side_effects}</div>
                    </div>
                  </div>
                )}

                {/* Contraindications */}
                {med.contraindications && (
                  <div style={{
                    marginTop: 10, padding: 12,
                    background: 'var(--red-100)', borderRadius: 8,
                    display: 'flex', gap: 10,
                  }}>
                    <ShieldCheck size={14} color="var(--red-600)" style={{ flexShrink: 0, marginTop: 2 }} />
                    <div>
                      <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--red-600)', marginBottom: 2 }}>CONTRAINDICATIONS</div>
                      <div style={{ fontSize: 13, color: 'var(--ink-light)' }}>{med.contraindications}</div>
                    </div>
                  </div>
                )}

                <InfoRow label="Known Interactions" value={med.interactions} />
              </div>
            )}
          </div>
        ))}
      </div>
    </main>
  )
}
