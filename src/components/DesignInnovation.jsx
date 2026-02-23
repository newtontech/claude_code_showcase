import React from 'react';
import { motion } from 'framer-motion';
import { useScrollReveal } from '../hooks';

const DesignInnovation = () => {
  const [ref1, isVisible1] = useScrollReveal();
  const [ref2, isVisible2] = useScrollReveal();
  const [ref3, isVisible3] = useScrollReveal();

  return (
    <section className="h-full flex flex-col justify-center py-20 bg-white relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-gray-50 rounded-full blur-3xl -z-10" />

      <div className="max-w-7xl mx-auto px-8 w-full">
        {/* Header */}
        <motion.div
          ref={ref1}
          initial={{ opacity: 0, y: 30 }}
          animate={isVisible1 ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="mb-16 border-b border-gray-100 pb-8"
        >
          <div className="flex items-center gap-4 mb-4">
            <span className="bg-orange-50 text-orange-600 font-bold px-3 py-1 rounded text-sm uppercase tracking-wider">Aesthetics & UX</span>
            <span className="text-gray-400 font-mono">02 / 05</span>
          </div>
          <h2 className="text-5xl font-display font-bold text-gray-900 mb-6">
            Design Innovation
          </h2>
          <p className="text-xl text-gray-500 max-w-3xl leading-relaxed">
            Claude Code doesn't just write logic; it understands modern UI/UX paradigms. It generates beautiful, accessible, and responsive interfaces that feel premium out of the box.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Feature 1: Unique Visual Language */}
          <motion.div
            ref={ref2}
            className="group relative bg-white rounded-2xl p-8 border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300"
            initial={{ opacity: 0, y: 50 }}
            animate={isVisible2 ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6 }}
          >
            <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
              <svg className="w-24 h-24 text-primary" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" /></svg>
            </div>

            <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-orange-100 to-orange-50 flex items-center justify-center text-3xl mb-6 shadow-inner">
              🎨
            </div>

            <h3 className="font-display font-bold text-2xl text-gray-900 mb-4">Bespoke Visual Systems</h3>
            <p className="text-gray-600 leading-relaxed mb-6">
              Escapes the "Bootstrap look" by generating custom design tokens. creates harmonious color palettes, fluid typography scales, and consistent spacing variables tailored to your brand identity.
            </p>

            <div className="space-y-3">
              <div className="flex items-center gap-3 p-2 rounded-lg bg-gray-50 border border-gray-100">
                <div className="flex gap-1">
                  <div className="w-6 h-6 rounded-full bg-[#D97757]"></div>
                  <div className="w-6 h-6 rounded-full bg-[#5E6A75]"></div>
                  <div className="w-6 h-6 rounded-full bg-[#B89B6D]"></div>
                </div>
                <span className="text-xs font-mono text-gray-500">Semantic Palettes</span>
              </div>
              <div className="flex items-center gap-3 p-2 rounded-lg bg-gray-50 border border-gray-100">
                <span className="font-display font-bold text-gray-900">Aa</span>
                <span className="text-xs font-mono text-gray-500">Fluid Typography</span>
              </div>
            </div>
          </motion.div>

          {/* Feature 2: Micro-interactions */}
          <motion.div
            className="group relative bg-white rounded-2xl p-8 border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300"
            initial={{ opacity: 0, y: 50 }}
            animate={isVisible2 ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
              <svg className="w-24 h-24 text-blue-500" fill="currentColor" viewBox="0 0 24 24"><path d="M7 2v11h3v9l7-12h-4l4-8z" /></svg>
            </div>

            <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-100 to-blue-50 flex items-center justify-center text-3xl mb-6 shadow-inner">
              ✨
            </div>

            <h3 className="font-display font-bold text-2xl text-gray-900 mb-4">Motion & Interaction</h3>
            <p className="text-gray-600 leading-relaxed mb-6">
              Breathes life into static layouts. Automatically integrates libraries like Framer Motion to add stagger effects, hover states, and smooth layout transitions without performance penalties.
            </p>

            <div className="space-y-4 pt-2">
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg group-hover:bg-white group-hover:shadow-md transition-all cursor-default">
                <span className="text-sm font-medium text-gray-700">Hover Me</span>
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              </div>
              <div className="h-1 w-full bg-gray-100 rounded-full overflow-hidden">
                <div className="h-full bg-blue-500 w-2/3 rounded-full"></div>
              </div>
            </div>
          </motion.div>

          {/* Feature 3: Responsive Architecture */}
          <motion.div
            className="group relative bg-white rounded-2xl p-8 border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300"
            initial={{ opacity: 0, y: 50 }}
            animate={isVisible2 ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
              <svg className="w-24 h-24 text-purple-500" fill="currentColor" viewBox="0 0 24 24"><path d="M4 6h18V4H4c-1.1 0-2 .9-2 2v11H0v3h14v-3H4V6zm19 2h-6c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h6c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1zm-1 9h-4v-7h4v7z" /></svg>
            </div>

            <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-purple-100 to-purple-50 flex items-center justify-center text-3xl mb-6 shadow-inner">
              📱
            </div>

            <h3 className="font-display font-bold text-2xl text-gray-900 mb-4">Device Agnostic</h3>
            <p className="text-gray-600 leading-relaxed mb-6">
              "Write once, run everywhere" is a standard, not a feature. Ensures semantic HTML structure and mobile-first CSS grid/flexbox layouts that adapt perfectly to any viewport size.
            </p>

            <div className="flex gap-2 pt-2">
              <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs font-bold rounded-full border border-gray-200">Mobile</span>
              <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs font-bold rounded-full border border-gray-200">Tablet</span>
              <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs font-bold rounded-full border border-gray-200">Desktop</span>
              <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs font-bold rounded-full border border-gray-200">4K</span>
            </div>
          </motion.div>
        </div>

        {/* Bottom Gallery Grid */}
        <motion.div
          ref={ref3}
          className="mt-12"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={isVisible3 ? { opacity: 1, scale: 1 } : {}}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          <div className="bg-gray-50 border border-gray-200 rounded-2xl p-8">
            <h4 className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-6 text-center">Style Generation Capability</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {/* Style Card 1 */}
              <div className="aspect-square bg-white rounded-xl shadow-sm hover:shadow-lg transition-shadow p-4 flex flex-col items-center justify-center gap-3 border border-gray-100">
                <div className="w-12 h-12 rounded-lg bg-gray-900 shadow-xl"></div>
                <span className="font-display font-bold text-gray-800 text-sm">Minimal Dark</span>
                <span className="text-[10px] text-gray-400">Clean & Sharp</span>
              </div>

              {/* Style Card 2 */}
              <div className="aspect-square bg-white rounded-xl shadow-sm hover:shadow-lg transition-shadow p-4 flex flex-col items-center justify-center gap-3 border border-gray-100">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-tr from-amber-200 to-orange-400 shadow-xl"></div>
                <span className="font-display font-bold text-gray-800 text-sm">Warm Gradient</span>
                <span className="text-[10px] text-gray-400">Friendly & Vibrant</span>
              </div>

              {/* Style Card 3 */}
              <div className="aspect-square bg-white rounded-xl shadow-sm hover:shadow-lg transition-shadow p-4 flex flex-col items-center justify-center gap-3 border border-gray-100">
                <div className="w-12 h-12 rounded-lg bg-blue-50 border border-blue-200 shadow-xl relative overflow-hidden">
                  <div className="absolute inset-0 bg-grid-slate-200/50 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))]" style={{ backgroundSize: '4px 4px' }}></div>
                </div>
                <span className="font-display font-bold text-gray-800 text-sm">Enterprise Blue</span>
                <span className="text-[10px] text-gray-400">Trusted & Secure</span>
              </div>

              {/* Style Card 4 */}
              <div className="aspect-square bg-white rounded-xl shadow-sm hover:shadow-lg transition-shadow p-4 flex flex-col items-center justify-center gap-3 border border-gray-100">
                <div className="w-12 h-12 rounded-lg bg-white border-2 border-black shadow-[4px_4px_0px_rgba(0,0,0,1)]"></div>
                <span className="font-display font-bold text-gray-800 text-sm">Neo-Brutalist</span>
                <span className="text-[10px] text-gray-400">Bold & Trendy</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default DesignInnovation;
