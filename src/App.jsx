import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Marquee from './components/Marquee';
import CodeGeneration from './components/CodeGeneration';
import DesignInnovation from './components/DesignInnovation';
import FullStackDev from './components/FullStackDev';
import Collaboration from './components/Collaboration';
import Stats from './components/Stats';
import CTA from './components/CTA';
import Footer from './components/Footer';

function App() {
  return (
    <div className="grid-bg">
      <div className="noise-overlay" />
      <Navbar />
      <Hero />
      <Marquee />
      <CodeGeneration />
      <DesignInnovation />
      <FullStackDev />
      <Collaboration />
      <Stats />
      <CTA />
      <Footer />
    </div>
  );
}

export default App;
