import React, { useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import CodeGeneration from './components/CodeGeneration';
import DesignInnovation from './components/DesignInnovation';
import FullStackDev from './components/FullStackDev';
import Collaboration from './components/Collaboration';
import Stats from './components/Stats';
import CTA from './components/CTA';
import Footer from './components/Footer';
import Marquee from './components/Marquee';
import { useScrollReveal } from './hooks';

function App() {
  return (
    <div className="bg-bg text-text-primary overflow-x-hidden">
      <Navbar />

      <main className="snap-y snap-mandatory h-screen overflow-y-scroll scroll-smooth">
        <section className="snap-start ppt-slide relative">
          <Hero />
        </section>

        <section className="snap-start">
          <Marquee />
        </section>

        <section className="snap-start ppt-slide">
          <CodeGeneration />
        </section>

        <section className="snap-start ppt-slide">
          <DesignInnovation />
        </section>

        <section className="snap-start ppt-slide">
          <FullStackDev />
        </section>

        <section className="snap-start ppt-slide">
          <Collaboration />
        </section>

        <section className="snap-start ppt-slide">
          <Stats />
        </section>

        <section className="snap-start ppt-slide">
          <CTA />
          <Footer />
        </section>
      </main>
    </div>
  );
}

export default App;
