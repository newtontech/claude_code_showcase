import React from 'react';
import { motion } from 'framer-motion';
import { useScrollReveal, useCounter } from '../hooks';

const CodeGeneration = () => {
  const [ref1, isVisible1] = useScrollReveal();
  const [ref2, isVisible2] = useScrollReveal();

  return (
    <section className="h-full flex flex-col justify-center py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-8 w-full">
        {/* Header */}
        <motion.div
          ref={ref1}
          initial={{ opacity: 0, y: 30 }}
          animate={isVisible1 ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="mb-12 border-b border-gray-200 pb-8"
        >
          <div className="flex items-center gap-4 mb-4">
            <span className="bg-primary/10 text-primary font-bold px-3 py-1 rounded text-sm uppercase tracking-wider">Core Capability</span>
            <span className="text-gray-400 font-mono">01 / 05</span>
          </div>
          <h2 className="text-5xl font-display font-bold text-gray-900 mb-4">
            Autonomous Code Generation
          </h2>
          <p className="text-xl text-gray-500 max-w-3xl">
            From natural language intent to production-ready code. Claude acts as a senior engineer, handling implementation details while you focus on architecture.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-12 gap-12">
          {/* Left: Features List */}
          <div className="lg:col-span-5 space-y-8">
            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-lg flex items-center justify-center text-2xl mb-4">⚡️</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Instant Implementation</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Generates boilerplate, utility functions, and complex algorithms in milliseconds. Reduces typing time by 90% and context switching errors to near zero.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-purple-50 text-purple-600 rounded-lg flex items-center justify-center text-2xl mb-4">🧠</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Contextual Understanding</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Analyzes project structure, imports, and style guides before writing a single line. Ensures new code fits seamlessly with existing patterns.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-green-50 text-green-600 rounded-lg flex items-center justify-center text-2xl mb-4">🛡️</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Self-Correcting</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Identifies syntax errors or logic bugs during generation and fixes them autonomously before presenting the final output.
              </p>
            </div>
          </div>

          {/* Right: Code Visualization */}
          <motion.div
            ref={ref2}
            className="lg:col-span-7 flex flex-col justify-center"
            initial={{ opacity: 0, x: 50 }}
            animate={isVisible2 ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="bg-white rounded-xl shadow-2xl border border-gray-200 overflow-hidden">
              <div className="bg-gray-100 px-4 py-2 border-b border-gray-200 flex justify-between items-center">
                <div className="text-xs font-mono text-gray-500">src/controllers/AuthController.ts</div>
                <div className="flex gap-2">
                  <div className="px-2 py-0.5 bg-green-100 text-green-700 text-[10px] rounded font-bold uppercase">Generated</div>
                  <div className="px-2 py-0.5 bg-blue-100 text-blue-700 text-[10px] rounded font-bold uppercase">Linted</div>
                </div>
              </div>
              <div className="p-0 overflow-hidden">
                <pre className="text-xs sm:text-sm leading-relaxed p-6 bg-white overflow-x-auto">
                  <code className="language-typescript">
                    <span className="text-purple-600">import</span> {'{'} Request, Response {'}'} <span className="text-purple-600">from</span> <span className="text-green-600">'express'</span>;{'\n'}
                    <span className="text-purple-600">import</span> {'{'} AuthService {'}'} <span className="text-purple-600">from</span> <span className="text-green-600">'../services/auth'</span>;{'\n\n'}
                    <span className="text-gray-500">/**{'\n'} * Handles user authentication requests{'\n'} * Generated by Claude Code{'\n'} */</span>{'\n'}
                    <span className="text-purple-600">export class</span> <span className="text-yellow-600">AuthController</span> {'{'}{'\n'}
                    {'  '}<span className="text-purple-600">constructor</span>(<span className="text-purple-600">private</span> authService: AuthService) {'{}'}{'\n\n'}
                    {'  '}<span className="text-blue-600">login</span> = <span className="text-purple-600">async</span> (req: Request, res: Response) ={'>'} {'{'}{'\n'}
                    {'    '}<span className="text-purple-600">try</span> {'{'}{'\n'}
                    {'      '}<span className="text-purple-600">const</span> {'{'} email, password {'}'} = req.body;{'\n'}
                    {'      '}<span className="text-purple-600">const</span> token = <span className="text-purple-600">await</span> <span className="text-blue-600">this</span>.authService.<span className="text-blue-600">validate</span>(email, password);{'\n'}
                    {'      '}<span className="text-gray-400">// Automatically handles JWT signing and cookie setting</span>{'\n'}
                    {'      '}res.<span className="text-blue-600">json</span>({'{'} success: <span className="text-orange-600">true</span>, token {'}'});{'\n'}
                    {'    '} {'}'} <span className="text-purple-600">catch</span> (error) {'{'}{'\n'}
                    {'      '}res.<span className="text-blue-600">status</span>(<span className="text-orange-600">401</span>).<span className="text-blue-600">json</span>({'{'} error: <span className="text-green-600">'Invalid credentials'</span> {'}'});{'\n'}
                    {'    '} {'}'}{'\n'}
                    {'  '} {'}'}{'\n'}
                    {'}'}
                  </code>
                </pre>
              </div>
              <div className="bg-gray-50 border-t border-gray-200 p-4">
                <div className="flex items-center gap-4 text-xs font-mono text-gray-500">
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-green-500"></span> 0 Errors</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-blue-500"></span> TypeScript 5.3</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-purple-500"></span> 98% Test Coverage</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default CodeGeneration;
