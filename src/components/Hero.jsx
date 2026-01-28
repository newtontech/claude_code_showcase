import React from 'react';
import { motion } from 'framer-motion';

const Hero = () => {
  return (
    <section className="min-h-screen flex items-center justify-center relative overflow-hidden pt-20">
      <motion.div
        className="absolute top-20 right-10 w-96 h-96 bg-primary rounded-full blur-3xl opacity-20"
        animate={{
          y: [0, -20, 0],
          rotate: [0, 3, 0],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      <motion.div
        className="absolute bottom-20 left-10 w-80 h-80 bg-secondary rounded-full blur-3xl opacity-20"
        animate={{
          y: [0, -20, 0],
          rotate: [0, -3, 0],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 1,
        }}
      />

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <motion.div
            className="space-y-8"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="inline-block glass px-4 py-2 rounded-full text-sm font-code">
              <span className="text-primary">◆</span> AI Coding Assistant with Superpowers
            </div>

            <h1 className="font-display font-black leading-none">
              <span className="block text-6xl md:text-8xl">Claude</span>
              <span className="block text-6xl md:text-8xl gradient-text glow">Code</span>
            </h1>

            <p className="text-xl md:text-2xl text-white/70 max-w-xl leading-relaxed">
              Your partner in code. Agentic, autonomous, and integrated directly into your terminal.
            </p>

            <div className="flex flex-wrap gap-4">
              <button className="btn-primary px-8 py-4 rounded-full font-bold text-lg text-white">
                Get Started
              </button>
              <button className="glass px-8 py-4 rounded-full font-bold text-lg hover:bg-white/10 transition-colors">
                View Docs
              </button>
            </div>
          </motion.div>

          <motion.div
            className="relative"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <motion.div
              className="code-block"
              animate={{
                y: [0, -20, 0],
              }}
              transition={{
                duration: 6,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            >
              <div className="code-header flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span className="ml-4 font-code text-sm text-white/50">terminal</span>
              </div>
              <pre className="p-6 font-code text-sm overflow-x-auto text-gray-300">
                <code>
                  <span className="text-green-400">$</span> claude code
                  {'\n\n'}
                  <span className="text-blue-400">?</span> <span className="font-bold text-white">How can I help you today?</span>
                  {'\n'}
                  <span className="text-gray-500">{`>`}</span> Build a desktop agent using OpenManus
                  {'\n\n'}
                  <span className="text-primary">●</span> <span className="text-primary">Planning task...</span>
                  {'\n'}
                  <span className="text-secondary">○</span> Analyzing project structure
                  {'\n'}
                  <span className="text-secondary">○</span> Creating implementation plan
                  {'\n\n'}
                  <span className="text-green-400">✓</span> <span className="text-white">Plan approved. Starting execution.</span>
                </code>
              </pre>
            </motion.div>
          </motion.div>
        </div>
      </div>

      <motion.div
        className="absolute bottom-10 left-1/2 -translate-x-1/2"
        animate={{
          y: [0, 10, 0],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >
        <div className="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center pt-2">
          <div className="w-1 h-3 bg-white/50 rounded-full"></div>
        </div>
      </motion.div>
    </section>
  );
};

export default Hero;
