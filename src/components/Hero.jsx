import React from 'react';
import { motion } from 'framer-motion';

const Hero = () => {
  return (
    <div className="h-full flex items-center justify-center relative overflow-hidden bg-white">
      {/* Background Decor */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary/5 rounded-full blur-3xl" />
      <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-blue-500/5 rounded-full blur-3xl" />

      <div className="max-w-7xl mx-auto px-8 w-full z-10 grid lg:grid-cols-2 gap-16 items-center">

        {/* Left Column: Content */}
        <motion.div
          className="space-y-8"
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gray-100 border border-gray-200">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
            <span className="text-sm font-medium text-gray-600 font-code tracking-wide uppercase">Next Gen Development</span>
          </div>

          <div className="space-y-2">
            <h1 className="text-7xl font-display font-bold text-gray-900 leading-tight tracking-tight">
              Claude <span className="text-primary transparent-text bg-clip-text bg-gradient-to-r from-primary to-orange-400">Code</span>
            </h1>
            <p className="text-3xl font-light text-gray-500">
              Agentic Intelligence for your Terminal
            </p>
          </div>

          <p className="text-lg text-gray-600 leading-relaxed max-w-xl border-l-4 border-primary/20 pl-6">
            Claude Code is not just an autocomplete engine. It is a fully autonomous coding agent capable of planning, executing, debugging, and deploying complex software systems directly from your local environment.
          </p>

          <div className="grid grid-cols-2 gap-6 pt-4">
            <div className="space-y-3">
              <h3 className="font-bold text-gray-900 flex items-center gap-2">
                <svg className="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                Deep Context Awareness
              </h3>
              <p className="text-sm text-gray-500">Reads your entire codebase to understand dependencies, architecture, and style conventions.</p>
            </div>
            <div className="space-y-3">
              <h3 className="font-bold text-gray-900 flex items-center gap-2">
                <svg className="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                Autonomous Execution
              </h3>
              <p className="text-sm text-gray-500">Runs commands, edits files, and fixes errors without constant hand-holding.</p>
            </div>
            <div className="space-y-3">
              <h3 className="font-bold text-gray-900 flex items-center gap-2">
                <svg className="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                Science & Research
              </h3>
              <p className="text-sm text-gray-500">Backed by Google DeepMind's latest breakthroughs in agentic reasoning.</p>
            </div>
            <div className="space-y-3">
              <h3 className="font-bold text-gray-900 flex items-center gap-2">
                <svg className="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
                Enterprise Grade
              </h3>
              <p className="text-sm text-gray-500">Secure, sandboxed execution with full audit trails.</p>
            </div>
          </div>
        </motion.div>

        {/* Right Column: Visual */}
        <motion.div
          className="relative"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <div className="bg-white rounded-xl shadow-2xl border border-gray-200 overflow-hidden">
            <div className="bg-gray-50 border-b border-gray-200 px-4 py-3 flex items-center gap-2">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-red-400"></div>
                <div className="w-3 h-3 rounded-full bg-amber-400"></div>
                <div className="w-3 h-3 rounded-full bg-green-400"></div>
              </div>
              <div className="mx-auto text-xs font-medium text-gray-400 font-mono">user@macbook: ~/projects/showcase</div>
            </div>
            <div className="p-6 font-code text-sm">
              <div className="flex gap-2">
                <span className="text-green-600 font-bold">➜</span>
                <span className="text-gray-700">claude code</span>
              </div>
              <div className="mt-4 border-l-2 border-gray-200 pl-4 py-2 bg-gray-50/50 rounded-r">
                <p className="text-gray-900 font-medium">Hello! I'm ready to help you code.</p>
                <p className="text-gray-500 mt-1">I can read files, execute commands, and edit your code.</p>
              </div>

              <div className="mt-4 flex gap-2">
                <span className="text-gray-400">{'>'}</span>
                <span className="text-gray-900">Analyze the 'examples' folder and find the showcase-server</span>
              </div>

              <div className="mt-4 space-y-2">
                <div className="flex items-center gap-2 text-gray-600">
                  <span className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></span>
                  <span>Scanning filesystem structure...</span>
                </div>
                <div className="text-gray-400 pl-6 text-xs font-mono">
                  - found examples/openmanus-agent<br />
                  - found package.json (root)<br />
                  - assessing docker configurations...
                </div>
                <div className="text-green-600 pl-6 flex items-center gap-2">
                  <span>✓</span> Found frontend application in `gemini-showcase`
                </div>
              </div>

              <div className="mt-6 p-3 bg-blue-50 border border-blue-100 rounded text-blue-900 text-xs font-mono">
                <span className="font-bold">PLAN:</span><br />
                1. Explore `openmanus-agent`<br />
                2. Check `PRD.md` for server specs<br />
                3. Locate Python server entry point
              </div>
            </div>
          </div>

          {/* Floating Badge */}
          <motion.div
            className="absolute -bottom-6 -right-6 bg-white p-4 rounded-xl shadow-xl border border-gray-100 flex items-center gap-4"
            animate={{ y: [0, -10, 0] }}
            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
          >
            <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center text-xl">🚀</div>
            <div>
              <div className="text-xs text-gray-400 uppercase font-bold tracking-wider">Velocity</div>
              <div className="font-bold text-gray-900">10x Faster</div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default Hero;
