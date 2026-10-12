export type PlanKey = 'homeschool' | 'saturday';
export type Cadence = 'monthly' | 'semester' | 'annual';

export const CADENCES: Record<Cadence, { label: string; suffix: string; interval: 'month' | 'year'; count: number }> = {
  monthly: { label: 'Monthly', suffix: '/mo', interval: 'month', count: 1 },
  semester: { label: 'Semester', suffix: '/semester', interval: 'month', count: 6 },
  annual: { label: 'Annual', suffix: '/yr', interval: 'year', count: 1 },
};

export const PLANS: Record<PlanKey, { name: string; blurb: string; price: Record<Cadence, number>; features: string[] }> = {
  homeschool: {
    name: 'Homeschool Hub',
    blurb: 'Full digital book library, guided Read mode and homeschool tasks.',
    price: { monthly: 14, semester: 75, annual: 120 },
    features: [
      'All Wonder Ship books, plus every age shelf as it launches',
      'Fullscreen guided Read mode for projector, laptop or tablet',
      'Post and browse community homeschool tasks',
    ],
  },
  saturday: {
    name: 'Saturday School',
    blurb: 'Weekly in-person sessions in Oakland, plus everything in Homeschool Hub.',
    price: { monthly: 89, semester: 420, annual: 750 },
    features: [
      'Weekly Saturday session with our teachers',
      'Small cohorts of about 10 students',
      'Everything in Homeschool Hub included',
      'Progress notes shared with parents',
    ],
  },
};

export function isPlan(v: unknown): v is PlanKey {
  return v === 'homeschool' || v === 'saturday';
}
export function isCadence(v: unknown): v is Cadence {
  return v === 'monthly' || v === 'semester' || v === 'annual';
}
export function lookupKey(plan: PlanKey, cadence: Cadence) {
  return `unite_${plan}_${cadence}`;
}
