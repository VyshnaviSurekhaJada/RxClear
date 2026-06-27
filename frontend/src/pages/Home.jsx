import React from 'react'
import { Link } from 'react-router-dom'
import { Scan, Pill, BrainCircuit, Salad, ShieldAlert, FileText, ArrowRight } from 'lucide-react'

const features = [
  { icon: Scan,        color: 'var(--teal-700)',   bg: 'var(--teal-50)',   title: 'OCR Extraction',       desc: 'Reads both printed and handwritten prescriptions using EasyOCR.' },
  { icon: Pill,        color: 'var(--blue-600)',    bg: 'var(--blue-100)',  title: 'Medicine Parsing',     desc: 'Extracts name, dosage, frequency, timing and duration for every drug.' },
  { icon: BrainCircuit,color: 'var(--amber-500)',   bg: 'var(--amber-100)', title: 'Disease Prediction',   desc: 'Random Forest model predicts the likely condition from medicine combinations.' },
  { icon: Salad,       color: 'var(--green-600)',   bg: 'var(--green-100)', title: 'Diet Recommendations', desc: 'Personalised food and lifestyle guidance based on the predicted condition.' },
  { icon: ShieldAlert, color: 'var(--red-600)',     bg: 'var(--red-100)',   title: 'Interaction Warnings', desc: 'Flags dangerous drug–drug and drug–substance interactions automatically.' },
  { icon: FileText,    color: 'var(--orange-500)',  bg: 'var(--orange-100)',title: 'PDF Report',           desc: 'One-click download of a professional prescription analysis report.' },
]

export default function Home() {
  return (
    <main style={{ maxWidth: 1100, margin: '0 auto', padding: '0 24px 64px' }}>

      {/* ── Hero ───────────────────────────────────────────────── */}
      <section style={{
        textAlign: 'center',
        padding: '72px 0 56px',
      }}>
        <span style={{
          display: 'inline-flex', alignItems: 'center', gap: 6,
          background: 'var(--teal-50)', color: 'var(--teal-700)',
          border: '1px solid var(--teal-100)',
          borderRadius: 99, padding: '4px 14px',
          fontSize: 12, fontWeight: 600, letterSpacing: '0.4px',
          textTransform: 'uppercase', marginBottom: 24,
        }}>
          <Scan size={12} /> AI-Powered Medical Intelligence
        </span>

        <h1 style={{
          fontFamily: 'var(--font-display)',
          fontSize: 'clamp(38px, 6vw, 64px)',
          fontWeight: 800, lineHeight: 1.1,
          letterSpacing: '-1.5px',
          color: 'var(--ink)',
          marginBottom: 20,
        }}>
          Decode your prescription<br />
          <span style={{
            background: 'linear-gradient(90deg, var(--teal-700), var(--teal-500))',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
          }}>in seconds.</span>
        </h1>

        <p style={{
          fontSize: 18, color: 'var(--muted)',
          maxWidth: 560, margin: '0 auto 40px',
          lineHeight: 1.7,
        }}>
          Upload a prescription image — handwritten or printed — and get structured
          medicine data, a disease prediction, diet guidance, and a downloadable report.
        </p>

        <Link to="/analyze" style={{
          display: 'inline-flex', alignItems: 'center', gap: 10,
          background: 'linear-gradient(135deg, var(--teal-700), var(--teal-500))',
          color: 'var(--white)',
          padding: '14px 32px', borderRadius: 12,
          textDecoration: 'none', fontWeight: 600, fontSize: 16,
          boxShadow: '0 4px 20px rgba(11,110,114,0.35)',
          transition: 'var(--transition)',
        }}>
          Analyze a Prescription <ArrowRight size={18} />
        </Link>
      </section>

      {/* ── Stats strip ────────────────────────────────────────── */}
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(3,1fr)',
        gap: 1, background: 'var(--border)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius-lg)',
        overflow: 'hidden', marginBottom: 64,
      }}>
        {[
          { value: '25+', label: 'Medicines in database' },
          { value: '30+', label: 'Disease patterns trained' },
          { value: '6',   label: 'Analysis stages' },
        ].map(({ value, label }) => (
          <div key={label} style={{
            background: 'var(--white)', padding: '28px 24px', textAlign: 'center',
          }}>
            <div style={{
              fontFamily: 'var(--font-display)', fontSize: 40, fontWeight: 800,
              color: 'var(--teal-700)', lineHeight: 1,
            }}>{value}</div>
            <div style={{ fontSize: 13, color: 'var(--muted)', marginTop: 6 }}>{label}</div>
          </div>
        ))}
      </div>

      {/* ── Feature grid ───────────────────────────────────────── */}
      <h2 style={{
        fontFamily: 'var(--font-display)', fontSize: 28, fontWeight: 700,
        textAlign: 'center', marginBottom: 36,
        letterSpacing: '-0.5px',
      }}>Everything in one analysis</h2>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: 20,
      }}>
        {features.map(({ icon: Icon, color, bg, title, desc }) => (
          <div key={title} style={{
            background: 'var(--white)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-lg)',
            padding: '28px 24px',
            display: 'flex', gap: 16, alignItems: 'flex-start',
            boxShadow: 'var(--shadow-sm)',
            transition: 'var(--transition)',
          }}>
            <span style={{
              flexShrink: 0,
              width: 44, height: 44, borderRadius: 12,
              background: bg, color,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              <Icon size={20} strokeWidth={2} />
            </span>
            <div>
              <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 4 }}>{title}</h3>
              <p style={{ fontSize: 13, color: 'var(--muted)', lineHeight: 1.6 }}>{desc}</p>
            </div>
          </div>
        ))}
      </div>

      {/* ── Disclaimer ──────────────────────────────────────────── */}
      <p style={{
        textAlign: 'center', fontSize: 12, color: 'var(--muted)',
        marginTop: 56, padding: '16px',
        background: 'var(--amber-100)', borderRadius: 8,
        border: '1px solid var(--amber-500)',
      }}>
        ⚕ RxClear is for informational purposes only and does not replace professional medical advice.
        Always consult a licensed healthcare provider before making any medical decisions.
      </p>
    </main>
  )
}
