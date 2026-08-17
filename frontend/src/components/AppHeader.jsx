import { Link } from 'react-router-dom'

export function AppHeader({ theme, onThemeToggle }) {
  const nextTheme = theme === 'light' ? 'dark' : 'light'

  return (
    <header className="site-header">
      <Link className="brand" to="/" aria-label="PulseIQ home">Pulse<span>IQ</span></Link>
      <button
        className="theme-toggle"
        type="button"
        onClick={onThemeToggle}
        aria-label={`Switch to ${nextTheme} theme`}
      >
        {theme === 'light' ? 'Dark mode' : 'Light mode'}
      </button>
    </header>
  )
}
