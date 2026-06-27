import React, { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Activity, Search, Clock, Scan } from 'lucide-react'

const links = [
  { to: '/',          label: 'Home',     icon: Activity },
  { to: '/analyze',   label: 'Analyze',  icon: Scan },
  { to: '/medicines', label: 'Medicines',icon: Search },
  { to: '/history',   label: 'History',  icon: Clock },
]

export default function Navbar() {
  const { pathname } = useLocation()
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <nav style={{
      position: 'sticky', top: 0, zIndex: 100,
      background: scrolled ? 'rgba(255,255,255,0.92)' : 'var(--white)',
      backdropFilter: scrolled ? 'blur(12px)' : 'none',
      borderBottom: '1px solid var(--border)',
      boxShadow: scrolled ? 'var(--shadow-sm)' : 'none',
      transition: 'var(--transition)',
    }}>
      <div style={{
        maxWidth: 1100, margin: '0 auto',
        padding: '0 24px',
        display: 'flex', alignItems: 'center',
        height: 60, gap: 8,
      }}>
        {/* Logo */}
        <Link to="/" style={{
          display: 'flex', alignItems: 'center', gap: 8,
          textDecoration: 'none', marginRight: 'auto',
        }}>
          <span style={{
            width: 34, height: 34,
            background: 'linear-gradient(135deg, var(--teal-700), var(--teal-500))',
            borderRadius: 10,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            color: 'var(--white)',
          }}>
            <Activity size={18} strokeWidth={2.5} />
          </span>
          <span style={{
            fontFamily: 'var(--font-display)',
            fontWeight: 700, fontSize: 20,
            color: 'var(--teal-700)',
            letterSpacing: '-0.3px',
          }}>
            Rx<span style={{ color: 'var(--teal-500)' }}>Clear</span>
          </span>
        </Link>

        {/* Nav links */}
        {links.map(({ to, label, icon: Icon }) => {
          const active = pathname === to
          return (
            <Link key={to} to={to} style={{
              display: 'flex', alignItems: 'center', gap: 6,
              padding: '6px 14px', borderRadius: 8,
              textDecoration: 'none',
              fontSize: 14, fontWeight: active ? 600 : 400,
              color: active ? 'var(--teal-700)' : 'var(--muted)',
              background: active ? 'var(--teal-50)' : 'transparent',
              transition: 'var(--transition)',
            }}>
              <Icon size={15} />
              {label}
            </Link>
          )
        })}
      </div>
    </nav>
  )
}
