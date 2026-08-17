import { useEffect, useState } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import { AppHeader } from './components/AppHeader'
import { ProductPage } from './pages/ProductPage'
import { SearchPage } from './pages/SearchPage'

function getInitialTheme() {
  const savedTheme = localStorage.getItem('pulseiq-theme')
  if (savedTheme === 'light' || savedTheme === 'dark') return savedTheme
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function App() {
  const [theme, setTheme] = useState(getInitialTheme)

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem('pulseiq-theme', theme)
  }, [theme])

  return (
    <BrowserRouter>
      <main className="app-shell">
        <AppHeader theme={theme} onThemeToggle={() => setTheme(theme === 'light' ? 'dark' : 'light')} />
        <Routes>
          <Route path="/" element={<SearchPage />} />
          <Route path="/products/:productId" element={<ProductPage />} />
          <Route path="*" element={<SearchPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App
