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
      className={`fixed top-0 left-0 right-0 z-50 backdrop-blur-xl border-b border-white/10 transition-all duration-300 ${
        scrolled ? 'bg-black/80' : 'bg-black/50'
      }`}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <div className="font-display font-bold text-2xl gradient-text cursor-pointer">
          CLAUDE CODE
        </div>

        <div className="hidden md:flex gap-8 text-sm font-semibold tracking-wider">
          <button
            onClick={() => scrollToSection('code')}
            className="hover:text-primary transition-colors"
          >
            代码生成
          </button>
          <button
            onClick={() => scrollToSection('design')}
            className="hover:text-secondary transition-colors"
          >
            设计创新
          </button>
          <button
            onClick={() => scrollToSection('fullstack')}
            className="hover:text-accent transition-colors"
          >
            全栈开发
          </button>
          <button
            onClick={() => scrollToSection('collaboration')}
            className="hover:text-primary transition-colors"
          >
            多域协作
          </button>
        </div>

        <button className="btn-primary px-6 py-2 rounded-full font-bold text-sm text-white">
          立即开始
        </button>
      </div>
    </motion.nav>
  );
};

export default Navbar;
