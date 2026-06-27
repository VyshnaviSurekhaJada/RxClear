import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Home from './pages/Home.jsx'
import Analyze from './pages/Analyze.jsx'
import History from './pages/History.jsx'
import MedicineSearch from './pages/MedicineSearch.jsx'

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/"          element={<Home />} />
        <Route path="/analyze"   element={<Analyze />} />
        <Route path="/history"   element={<History />} />
        <Route path="/medicines" element={<MedicineSearch />} />
      </Routes>
    </BrowserRouter>
  )
}
