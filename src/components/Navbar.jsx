import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.pageYOffset > 100);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <motion.nav
      className={`fixed top-0 left-0 right-0 z-50 backdrop-blur-xl border-b border-gray-200 transition-all duration-300 ${scrolled ? 'bg-white/90 shadow-sm' : 'bg-white/0'
        }`}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-2 cursor-pointer" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          <div className="w-8 h-8 bg-black rounded-lg"></div>
          <div className="font-display font-bold text-xl text-gray-900 tracking-tight">
            CLAUDE CODE
          </div>
        </div>

        <div className="hidden md:flex gap-8 text-sm font-semibold tracking-wide text-gray-500">
          <button
            onClick={() => scrollToSection('code')}
            className="hover:text-gray-900 transition-colors"
          >
            Code
          </button>
          <button
            onClick={() => scrollToSection('design')}
            className="hover:text-gray-900 transition-colors"
          >
            Design
          </button>
          <button
            onClick={() => scrollToSection('fullstack')}
            className="hover:text-gray-900 transition-colors"
          >
            Full Stack
          </button>
          <button
            onClick={() => scrollToSection('collaboration')}
            className="hover:text-gray-900 transition-colors"
          >
            Collaboration
          </button>
        </div>

        <button className="bg-gray-900 text-white px-6 py-2 rounded-lg font-bold text-sm hover:bg-gray-800 transition-colors shadow-lg hover:shadow-xl hover:-translate-y-0.5 transform">
          Get Started
        </button>
      </div>
    </motion.nav>
  );
};

export default Navbar;
