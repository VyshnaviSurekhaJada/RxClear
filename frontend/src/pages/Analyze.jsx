import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import {
  Upload, Loader2, CheckCircle2, AlertTriangle, Info,
  Pill, BrainCircuit, Salad, FileDown, ChevronDown, ChevronUp,
  User, Calendar, Stethoscope, RefreshCw, ShieldAlert,
} from 'lucide-react'

/* ── tiny helpers ─────────────────────────────────────────────────────── */
const Card = ({ children, style = {} }) => (
  <div style={{
    background: 'var(--white)', border: '1px solid var(--border)',
    borderRadius: 'var(--radius-lg)', padding: '24px',
    boxShadow: 'var(--shadow-sm)', ...style,
  }}>{children}</div>
)

const SectionTitle = ({ icon: Icon, color, label }) => (
  <h2 style={{
    display: 'flex', alignItems: 'center', gap: 8,
    fontFamily: 'var(--font-display)', fontSize: 17, fontWeight: 700,
    color: 'var(--ink)', marginBottom: 16,
  }}>
    <span style={{
      width: 30, height: 30, borderRadius: 8,
      background: color + '22', color,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
    }}><Icon size={16} /></span>
    {label}
  </h2>
)

const Badge = ({ children, color, bg }) => (
  <span style={{
    display: 'inline-flex', alignItems: 'center',
    padding: '2px 10px', borderRadius: 99, fontSize: 11,
    fontWeight: 600, color, background: bg,
  }}>{children}</span>
)

const sevConfig = {
  HIGH:   { color: 'var(--red-600)',    bg: 'var(--red-100)',    label: 'HIGH' },
  MEDIUM: { color: 'var(--orange-500)', bg: 'var(--orange-100)', label: 'MEDIUM' },
  INFO:   { color: 'var(--blue-600)',   bg: 'var(--blue-100)',   label: 'INFO' },
}

/* ── Collapsible section ─────────────────────────────────────────────── */
function Collapsible({ title, icon, children, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div style={{ borderBottom: '1px solid var(--border)', paddingBottom: open ? 0 : 0 }}>
      <button onClick={() => setOpen(o => !o)} style={{
        width: '100%', display: 'flex', alignItems: 'center',
        justifyContent: 'space-between',
        background: 'none', border: 'none', cursor: 'pointer',
        padding: '12px 0', color: 'var(--muted)', fontSize: 13, fontWeight: 500,
      }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          {icon} {title}
        </span>
        {open ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
      </button>
      {open && <div style={{ paddingBottom: 12 }}>{children}</div>}
    </div>
  )
}

/* ── Main page ───────────────────────────────────────────────────────── */
export default function Analyze() {
  const [file, setFile]       = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)
  const [result, setResult]   = useState(null)

  const onDrop = useCallback((accepted) => {
    const f = accepted[0]
    if (!f) return
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setResult(null)
    setError(null)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/jpeg': [], 'image/png': [], 'image/webp': [] },
    maxFiles: 1,
  })

  const analyze = async () => {
    if (!file) return
    setLoading(true); setError(null)
    try {
      const fd = new FormData()
      fd.append('file', file)
      const { data } = await axios.post('/analyze', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Analysis failed. Check the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const reset = () => { setFile(null); setPreview(null); setResult(null); setError(null) }

  return (
    <main style={{ maxWidth: 1100, margin: '0 auto', padding: '36px 24px 64px' }}>
      <h1 style={{
        fontFamily: 'var(--font-display)', fontSize: 28, fontWeight: 800,
        letterSpacing: '-0.5px', marginBottom: 6,
      }}>Prescription Analyzer</h1>
      <p style={{ color: 'var(--muted)', marginBottom: 28, fontSize: 14 }}>
        Upload a prescription image to extract medicines, predict disease and get dietary guidance.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: result ? '340px 1fr' : '1fr', gap: 24 }}>

        {/* ── Left: Upload panel ─────────────────────────────── */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {/* Dropzone */}
          <div {...getRootProps()} style={{
            border: `2px dashed ${isDragActive ? 'var(--teal-500)' : 'var(--border)'}`,
            borderRadius: 'var(--radius-lg)',
            background: isDragActive ? 'var(--teal-50)' : 'var(--white)',
            padding: '40px 24px',
            textAlign: 'center', cursor: 'pointer',
            transition: 'var(--transition)',
          }}>
            <input {...getInputProps()} />
            {preview ? (
              <img src={preview} alt="Preview" style={{
                maxHeight: 220, maxWidth: '100%',
                borderRadius: 8, objectFit: 'contain',
              }} />
            ) : (
              <>
                <Upload size={36} color="var(--teal-500)" style={{ margin: '0 auto 12px' }} />
                <p style={{ fontWeight: 500, marginBottom: 4 }}>
                  {isDragActive ? 'Drop it here' : 'Drag & drop prescription image'}
                </p>
                <p style={{ fontSize: 12, color: 'var(--muted)' }}>or click to browse — JPG, PNG, WEBP</p>
              </>
            )}
          </div>

          {/* Action buttons */}
          <div style={{ display: 'flex', gap: 10 }}>
            <button onClick={analyze} disabled={!file || loading} style={{
              flex: 1,
              display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
              background: 'linear-gradient(135deg, var(--teal-700), var(--teal-500))',
              color: 'var(--white)', border: 'none',
              padding: '12px 0', borderRadius: 10,
              fontWeight: 600, fontSize: 15, cursor: 'pointer',
              opacity: !file || loading ? 0.6 : 1,
              transition: 'var(--transition)',
            }}>
              {loading
                ? <><Loader2 size={18} style={{ animation: 'spin 1s linear infinite' }} /> Analyzing…</>
                : <><BrainCircuit size={18} /> Analyze</>}
            </button>
            {(file || result) && (
              <button onClick={reset} style={{
                display: 'flex', alignItems: 'center', gap: 6,
                border: '1px solid var(--border)', background: 'var(--white)',
                padding: '12px 16px', borderRadius: 10,
                cursor: 'pointer', fontSize: 13, color: 'var(--muted)',
              }}>
                <RefreshCw size={15} /> Reset
              </button>
            )}
          </div>

          {error && (
            <div style={{
              background: 'var(--red-100)', color: 'var(--red-600)',
              borderRadius: 8, padding: '12px 14px', fontSize: 13,
              display: 'flex', alignItems: 'flex-start', gap: 8,
            }}>
              <AlertTriangle size={15} style={{ flexShrink: 0, marginTop: 2 }} /> {error}
            </div>
          )}

          {/* OCR text box */}
          {result?.raw_text && (
            <Card style={{ padding: '16px 18px' }}>
              <Collapsible title="Extracted OCR Text" icon={<Info size={13} />}>
                <pre style={{
                  fontSize: 11, color: 'var(--muted)',
                  whiteSpace: 'pre-wrap', fontFamily: 'monospace',
                  maxHeight: 180, overflowY: 'auto',
                }}>{result.raw_text}</pre>
              </Collapsible>
            </Card>
          )}
        </div>

        {/* ── Right: Results ─────────────────────────────────── */}
        {result && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>

            {/* Patient info */}
            <Card>
              <SectionTitle icon={User} color="var(--teal-700)" label="Patient Information" />
              <div style={{
                display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 12,
              }}>
                {[
                  { label: 'Name',      value: result.patient_info?.patient_name },
                  { label: 'Age',       value: result.patient_info?.age },
                  { label: 'Gender',    value: result.patient_info?.gender },
                  { label: 'Date',      value: result.patient_info?.date, icon: Calendar },
                  { label: 'Prescriber',value: result.patient_info?.prescriber, icon: Stethoscope },
                  { label: 'Diagnosis', value: result.patient_info?.diagnosis },
                ].map(({ label, value }) => (
                  <div key={label} style={{
                    background: 'var(--teal-50)', borderRadius: 8,
                    padding: '10px 12px',
                  }}>
                    <div style={{ fontSize: 10, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: 2 }}>{label}</div>
                    <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--ink)' }}>{value || '—'}</div>
                  </div>
                ))}
              </div>
            </Card>

            {/* Medicines table */}
            {result.medicines?.length > 0 && (
              <Card>
                <SectionTitle icon={Pill} color="var(--blue-600)" label={`Medicines (${result.medicines.length})`} />
                <div style={{ overflowX: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
                    <thead>
                      <tr style={{ background: 'var(--teal-700)', color: 'var(--white)' }}>
                        {['Medicine', 'Dosage', 'Frequency', 'Timing', 'Duration', 'Category'].map(h => (
                          <th key={h} style={{ padding: '9px 12px', textAlign: 'left', fontSize: 11, fontWeight: 600 }}>{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {result.medicines.map((m, i) => (
                        <tr key={i} style={{ background: i % 2 === 0 ? 'var(--white)' : 'var(--teal-50)' }}>
                          <td style={{ padding: '8px 12px', fontWeight: 600 }}>{m.name}</td>
                          <td style={{ padding: '8px 12px' }}>{m.dosage}</td>
                          <td style={{ padding: '8px 12px' }}>{m.frequency}</td>
                          <td style={{ padding: '8px 12px' }}>{m.timing}</td>
                          <td style={{ padding: '8px 12px' }}>{m.duration}</td>
                          <td style={{ padding: '8px 12px' }}>
                            <Badge color="var(--teal-700)" bg="var(--teal-50)">{m.category || '—'}</Badge>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Medicine details accordion */}
                <div style={{ marginTop: 16 }}>
                  {result.medicines.map((m, i) => (
                    <Collapsible key={i}
                      title={`${m.name}${m.generic_name ? ` (${m.generic_name})` : ''} – details`}
                      icon={<Pill size={12} />}
                    >
                      <div style={{
                        display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, fontSize: 12,
                      }}>
                        {[
                          { label: 'Uses', value: m.uses },
                          { label: 'Side Effects', value: m.side_effects },
                          { label: 'Max Adult Dose', value: m.max_adult_dose },
                          { label: 'Max Child Dose', value: m.max_child_dose },
                          { label: 'Contraindications', value: m.contraindications },
                          { label: 'Interactions', value: m.interactions },
                        ].map(({ label, value }) => value && (
                          <div key={label} style={{ borderLeft: '2px solid var(--teal-100)', paddingLeft: 8 }}>
                            <div style={{ color: 'var(--muted)', fontSize: 10, textTransform: 'uppercase', letterSpacing: '0.4px' }}>{label}</div>
                            <div style={{ color: 'var(--ink-light)', marginTop: 1 }}>{value}</div>
                          </div>
                        ))}
                      </div>
                    </Collapsible>
                  ))}
                </div>
              </Card>
            )}

            {/* Disease + confidence */}
            <Card>
              <SectionTitle icon={BrainCircuit} color="var(--amber-500)" label="Disease Prediction" />
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 12 }}>
                <div>
                  <div style={{
                    fontFamily: 'var(--font-display)', fontSize: 22, fontWeight: 800,
                    color: 'var(--teal-700)', lineHeight: 1.2,
                  }}>{result.disease_prediction?.top_disease || '—'}</div>
                  <div style={{ fontSize: 12, color: 'var(--muted)', marginTop: 2 }}>Primary prediction</div>
                </div>
                <div style={{
                  background: 'var(--amber-100)', color: 'var(--amber-500)',
                  borderRadius: 12, padding: '8px 18px', textAlign: 'center',
                }}>
                  <div style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 800 }}>
                    {result.disease_prediction?.confidence?.toFixed(1)}%
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--muted)' }}>confidence</div>
                </div>
              </div>

              {/* Confidence bar */}
              <div style={{ marginTop: 14 }}>
                <div style={{ height: 6, background: 'var(--border)', borderRadius: 99, overflow: 'hidden' }}>
                  <div style={{
                    height: '100%', borderRadius: 99,
                    width: `${result.disease_prediction?.confidence || 0}%`,
                    background: 'linear-gradient(90deg, var(--teal-700), var(--teal-300))',
                    transition: 'width 0.8s ease',
                  }} />
                </div>
              </div>

              {/* Alt predictions */}
              {result.disease_prediction?.predictions?.length > 1 && (
                <div style={{ marginTop: 12 }}>
                  <div style={{ fontSize: 11, color: 'var(--muted)', marginBottom: 6 }}>Other possibilities</div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                    {result.disease_prediction.predictions.slice(1).map(p => (
                      <span key={p.disease} style={{
                        background: 'var(--surface)', border: '1px solid var(--border)',
                        borderRadius: 6, padding: '4px 10px', fontSize: 12,
                        color: 'var(--ink-light)',
                      }}>{p.disease} <strong>{p.confidence.toFixed(0)}%</strong></span>
                    ))}
                  </div>
                </div>
              )}
            </Card>

            {/* Warnings */}
            {(result.interaction_warnings?.length > 0 || result.dosage_warnings?.length > 0) && (
              <Card>
                <SectionTitle icon={ShieldAlert} color="var(--red-600)" label="Warnings & Alerts" />
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                  {[...result.interaction_warnings, ...result.dosage_warnings].map((w, i) => {
                    const cfg = sevConfig[w.severity] || sevConfig.INFO
                    return (
                      <div key={i} style={{
                        display: 'flex', alignItems: 'flex-start', gap: 10,
                        background: cfg.bg, borderRadius: 8, padding: '10px 12px',
                        borderLeft: `3px solid ${cfg.color}`,
                      }}>
                        <AlertTriangle size={14} color={cfg.color} style={{ flexShrink: 0, marginTop: 2 }} />
                        <span style={{ fontSize: 13, color: 'var(--ink-light)', flex: 1 }}>{w.message}</span>
                        <Badge color={cfg.color} bg={cfg.bg}>{cfg.label}</Badge>
                      </div>
                    )
                  })}
                </div>
              </Card>
            )}

            {/* Diet recommendations */}
            {result.diet_recommendations && (
              <Card>
                <SectionTitle icon={Salad} color="var(--green-600)" label="Diet & Lifestyle" />
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 16 }}>
                  {[
                    { key: 'eat',       label: '✅ Eat',      color: 'var(--green-600)', bg: 'var(--green-100)' },
                    { key: 'avoid',     label: '❌ Avoid',    color: 'var(--red-600)',   bg: 'var(--red-100)' },
                    { key: 'lifestyle', label: '💪 Lifestyle',color: 'var(--blue-600)',  bg: 'var(--blue-100)' },
                  ].map(({ key, label, color, bg }) => (
                    <div key={key}>
                      <div style={{
                        fontSize: 12, fontWeight: 700, color,
                        marginBottom: 8, padding: '4px 10px',
                        background: bg, borderRadius: 6, display: 'inline-block',
                      }}>{label}</div>
                      <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: 4 }}>
                        {(result.diet_recommendations[key] || []).map(item => (
                          <li key={item} style={{
                            fontSize: 13, color: 'var(--ink-light)',
                            display: 'flex', alignItems: 'flex-start', gap: 6,
                          }}>
                            <span style={{ color, marginTop: 2 }}>›</span> {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </Card>
            )}

            {/* Download report */}
            {result.report_url && (
              <a
                href={result.report_url}
                download
                style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10,
                  background: 'linear-gradient(135deg, var(--teal-900), var(--teal-700))',
                  color: 'var(--white)', borderRadius: 12,
                  padding: '14px 0', textDecoration: 'none',
                  fontWeight: 700, fontSize: 15,
                  boxShadow: '0 4px 20px rgba(11,77,82,0.35)',
                }}
              >
                <FileDown size={18} /> Download PDF Report
              </a>
            )}
          </div>
        )}
      </div>

      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
      `}</style>
    </main>
  )
}
