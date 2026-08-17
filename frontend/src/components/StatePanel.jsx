import { Link } from 'react-router-dom'

export function StatePanel({ title, description, actionLabel, actionTo = '/' }) {
  return (
    <section className="state-panel" aria-live="polite">
      <div className="state-panel-mark" aria-hidden="true">⌁</div>
      <h1>{title}</h1>
      <p>{description}</p>
      {actionLabel && <Link className="secondary-action" to={actionTo}>{actionLabel}</Link>}
    </section>
  )
}
