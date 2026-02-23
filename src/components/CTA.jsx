import React from 'react';
import { motion } from 'framer-motion';
import { useScrollReveal } from '../hooks';

const CTA = () => {
  const [ref, isVisible] = useScrollReveal();

  return (
    <section className="h-full flex flex-col justify-center py-20 bg-white relative overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-orange-50 rounded-full blur-3xl -z-10 opacity-60" />
      <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-blue-50 rounded-full blur-3xl -z-10 opacity-60" />

      <div className="max-w-5xl mx-auto px-6 text-center relative z-10">
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 40 }}
          animate={isVisible ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          <div className="mb-8 inline-block">
            <span className="bg-gray-900 text-white px-4 py-1.5 rounded-full text-sm font-bold tracking-wide uppercase">
              Early Access Available
            </span>
          </div>

          <h2 className="font-display font-black text-5xl md:text-7xl mb-8 text-gray-900 leading-tight">
            Ready to Revolutionize<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-orange-600">Your Workflow?</span>
          </h2>

          <p className="text-xl md:text-2xl text-gray-500 mb-12 max-w-3xl mx-auto leading-relaxed">
            Join the elite circle of developers who are shipping faster, writing cleaner code, and focusing on what truly matters—innovation.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-6">
            <button className="bg-gray-900 text-white px-10 py-5 rounded-xl font-bold text-lg hover:bg-gray-800 hover:scale-105 transition-all shadow-xl hover:shadow-2xl">
              Start Free Trial →
            </button>
            <button className="bg-white text-gray-900 border-2 border-gray-200 px-10 py-5 rounded-xl font-bold text-lg hover:border-gray-900 hover:bg-gray-50 transition-all">
              Schedule Demo
            </button>
          </div>

          <div className="mt-12 flex items-center justify-center gap-6 text-sm text-gray-400">
            <span className="flex items-center gap-2">✓ No credit card required</span>
            <span className="flex items-center gap-2">✓ 14-day free trial</span>
            <span className="flex items-center gap-2">✓ Cancel anytime</span>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default CTA;
