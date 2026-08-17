export function IntelligencePlaceholder({ title, description }) {
  return (
    <section className="intelligence-placeholder">
      <div className="placeholder-marker" aria-hidden="true">+</div>
      <div>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>
      <span className="coming-soon-label">Not available yet</span>
    </section>
  )
}
