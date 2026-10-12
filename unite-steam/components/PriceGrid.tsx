'use client';
import { useState } from 'react';
import { CADENCES, PLANS, type Cadence, type PlanKey } from '@/lib/plans';

type Props = { order: PlanKey[]; featured: PlanKey; currentPlan?: PlanKey | null; showToggle?: boolean };

export default function PriceGrid({ order, featured, currentPlan, showToggle = true }: Props) {
  const [cadence, setCadence] = useState<Cadence>('monthly');
  return (
    <>
      {showToggle && (
        <div className="cadence-toggle" role="group" aria-label="Billing period">
          {(Object.keys(CADENCES) as Cadence[]).map((c) => (
            <button key={c} type="button" className={c === cadence ? 'active' : undefined} onClick={() => setCadence(c)} aria-pressed={c === cadence}>
              {CADENCES[c].label}
            </button>
          ))}
        </div>
      )}
      <div className="pricegrid">
        {order.map((key) => {
          const p = PLANS[key];
          const isFeatured = key === featured;
          const monthlyEquiv = cadence === 'monthly' ? null : p.price[cadence] / (cadence === 'semester' ? 6 : 12);
          const isCurrent = currentPlan === key;
          return (
            <div key={key} className={'pricecard' + (isFeatured ? ' featured' : '')}>
              {isFeatured && <span className="badge">Most complete</span>}
              <h3>{p.name}</h3>
              <p style={{ color: 'var(--ink-muted)', fontSize: '0.86rem', marginTop: '-0.4rem' }}>{p.blurb}</p>
              <div className="price">
                ${p.price[cadence]}
                <span>{CADENCES[cadence].suffix}</span>
              </div>
              {monthlyEquiv && (
                <p className="label" style={{ marginTop: '-0.5rem' }}>
                  about ${monthlyEquiv.toFixed(2)}/mo &middot; save {Math.round((1 - monthlyEquiv / p.price.monthly) * 100)}%
                </p>
              )}
              <ul>
                {p.features.map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
              <form action="/api/checkout" method="post">
                <input type="hidden" name="plan" value={key} />
                <input type="hidden" name="cadence" value={cadence} />
                <button type="submit" disabled={isCurrent} style={{ width: '100%' }}>
                  {isCurrent ? 'Your current plan' : `Choose ${p.name}`}
                </button>
              </form>
            </div>
          );
        })}
      </div>
    </>
  );
}
