import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Marquee from './components/Marquee';
import ComparisonSection from './components/ComparisonSection';
import WorkflowSection from './components/WorkflowSection';
import EcosystemSection from './components/EcosystemSection';
import ShowcaseSection from './components/ShowcaseSection';
import CTA from './components/CTA';
import Footer from './components/Footer';

function App() {
  return (
    <div className="grid-bg font-body bg-bg text-text min-h-screen">
      <div className="noise-overlay" />
      <Navbar />
      <main>
        <Hero />
        <Marquee />
        <ComparisonSection />
        <WorkflowSection />
        <ShowcaseSection />
        <EcosystemSection />
        <CTA />
      </main>
      <Footer />
    </div>
  );
}

export default App;
