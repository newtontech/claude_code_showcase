import React from 'react';
import Hero from './components/Hero';
import TerminalDemo from './components/TerminalDemo';
import FeatureCard from './components/FeatureCard';
import { features } from './data';
import './App.css';

function App() {
  return (
    <div className="container">
      <Hero />
      
      <TerminalDemo />
      
      <section className="features-section">
        <h2>Supercharge Your Workflow</h2>
        <div className="features-grid">
          {features.map((feature, index) => (
            <FeatureCard 
              key={index}
              title={feature.title} 
              description={feature.description} 
              icon={feature.icon} 
            />
          ))}
        </div>
      </section>

      <footer>
        <p>© 2026 Gemini CLI Showcase. Built with React & Vite.</p>
      </footer>
    </div>
  );
}

export default App;