import Link from 'next/link';
import RegisterForm from '@/components/RegisterForm';
import { SHELVES } from '@/lib/shelves';

export default function Home() {
  const registerUrl = process.env.NEXT_PUBLIC_REGISTER_FORM_URL;
  return (
    <>
      <div className="hero">
        <span className="orbit" />
        <span className="orbit o2" />
        <div className="shell">
          <span className="kicker">UNITE &middot; Unique Natives Interacting Together Elevating</span>
          <h1>
            Building stronger communities, <em>one step at a time.</em>
          </h1>
          <p className="lede">
            An Afrocentric, youth-led future grounded in truth, love, and science. Learn at home with the Homeschool Hub,
            join us in person at Saturday School, or work with us on a curriculum built for your family or organization.
          </p>
          <div className="ctas">
            {registerUrl ? (
              <a className="btn gold" href={registerUrl} target="_blank" rel="noopener">Register today</a>
            ) : (
              <a className="btn gold" href="#register">Register today</a>
            )}
            <Link className="btn ghost" href="/pricing">See offerings &amp; pricing</Link>
          </div>
        </div>
      </div>

      <div className="shell">
        <div className="statband">
          <div className="stat"><b>275</b><span>youth served in a typical year</span></div>
          <div className="stat"><b>75%</b><span>average gain in STEM confidence</span></div>
          <div className="stat"><b>90%</b><span>report a lift in cultural pride</span></div>
          <div className="stat"><b>1,200+</b><span>instructional hours delivered</span></div>
        </div>
        <p className="statnote">From UNITE&rsquo;s Impact Hub at unitehella.org.</p>

        <div className="sechead">
          <span className="label">Our programs</span>
          <h2>Three ways to learn with UNITE.</h2>
          <p>Pick the one that fits your family. Saturday School always includes the Homeschool Hub.</p>
        </div>
        <div className="progs">
          <Link className="prog" href="/saturday-school">
            <span className="ico">&#127979;</span>
            <h3>Saturday School</h3>
            <p>Weekly in-person STEAM sessions in Oakland with Mr. Domkam and Mr. Johnson. Hands-on, movement-rich, and tied to the Hub so learning continues at home.</p>
            <span className="go">Explore Saturday School &rarr;</span>
          </Link>
          <Link className="prog" href="/library">
            <span className="ico">&#128640;</span>
            <h3>STEAM Curriculum</h3>
            <p>The Homeschool Hub: the Wonder Ship read-aloud series for ages 5 and under today, with more age shelves on the way.</p>
            <span className="go">Open the library &rarr;</span>
          </Link>
          <Link className="prog" href="/pricing#contact">
            <span className="ico">&#127793;</span>
            <h3>Community Projects</h3>
            <p>Lab work, building planter boxes, hip-hop and more. Real projects that connect STEAM to neighborhood life.</p>
            <span className="go">Get involved &rarr;</span>
          </Link>
        </div>
        <div className="custom">
          <div><b>Personalized curriculum</b><span>A consultation-based curriculum built for your child, with regular check-ins.</span></div>
          <div><b>Private tutoring</b><span>A one-on-one version of Saturday School.</span></div>
          <div><b>For organizations</b><span>Curriculum development for schools, nonprofits and youth programs.</span></div>
        </div>

        <div className="sechead" id="register">
          <span className="label">How to register</span>
          <h2>Four steps to get started.</h2>
          <p>Tell us what you&rsquo;re interested in, or go straight to an account and a plan.</p>
        </div>
        <div className="regwrap">
          <ol className="steps">
            <li><div><b>Pick your path</b><span>Homeschool Hub, Saturday School, or a custom offering.</span></div></li>
            <li><div><b>Create your account</b><span>A parent or guardian holds the account. Members log in to reach the library.</span></div></li>
            <li><div><b>Choose a plan</b><span>Pay monthly, by semester, or annually. Longer costs less per month.</span></div></li>
            <li><div><b>Start learning</b><span>The Hub opens right away, and we confirm your Saturday School seat by email.</span></div></li>
          </ol>
          <RegisterForm />
        </div>

        <div className="mission">
          <span className="label">Our mission</span>
          <h3>Truth, love, and science.</h3>
          <p>UNITE supports people in underserved and low-income communities through education, unity, and progress, building skills, boosting learning, and creating strong futures.</p>
        </div>

        <div className="pickline" style={{ marginTop: '3rem' }}>
          <h2>Browse the Homeschool Hub by age</h2>
          <span className="label">1 of 5 shelves built</span>
        </div>
        <div className="ages">
          <Link className="acard on" href="/library">
            <span className="wm">5 &amp; under</span>
            <span className="sub">The Wonder Ship book series</span>
            <span className="count mono">3 books &middot; 20&ndash;30 min each</span>
          </Link>
          {SHELVES.map((s) => (
            <Link key={s.slug} className="acard off" href={`/shelves/${s.slug}`}>
              <span className="wm">{s.name}</span>
              <span className="sub">Coming soon</span>
              <span className="count mono">0 items</span>
            </Link>
          ))}
        </div>
      </div>
    </>
  );
}
