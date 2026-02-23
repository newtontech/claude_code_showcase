import React from 'react';
import { motion } from 'framer-motion';
import { useCounter, useScrollReveal } from '../hooks';

const Stats = () => {
  const [ref1, count1] = useCounter(10);
  const [ref2, count2] = useCounter(100);
  const [ref3, count3] = useCounter(99);
  const [ref4, count4] = useCounter(24);
  const [scrollRef, isVisible] = useScrollReveal();

  const stats = [
    {
      ref: ref1,
      count: count1,
      suffix: 'x',
      label: 'Developer Velocity',
      desc: 'Increase in shipping speed for complex features compared to traditional coding workflow.'
    },
    {
      ref: ref2,
      count: count2,
      suffix: '+',
      label: 'Languages Supported',
      desc: 'From Assembly to Zig, Claude adapts to any syntax, framework, or proprietary internal DSL.'
    },
    {
      ref: ref3,
      count: count3,
      suffix: '%',
      label: 'First-Pass Accuracy',
      desc: 'Code that compiles, passes linting checks, and runs correctly on the first generation.'
    },
    {
      ref: ref4,
      count: count4,
      suffix: '/7',
      label: 'Availability',
      desc: 'Your pair programmer never sleeps, takes breaks, or gets tired of refactoring legacy code.'
    },
  ];

  return (
    <section className="h-full flex flex-col justify-center py-20 bg-gray-50 relative">
      {/* Decorative */}
      <div className="absolute top-1/2 left-0 w-full h-px bg-gray-200 -z-10"></div>

      <div className="max-w-7xl mx-auto px-8 w-full">
        <motion.div
          ref={scrollRef}
          initial={{ opacity: 0, y: 30 }}
          animate={isVisible ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-20"
        >
          <span className="text-secondary font-bold tracking-widest uppercase text-sm mb-4 block">Proven Results</span>
          <h2 className="text-5xl font-display font-bold text-gray-900 mb-6">Scale & Impact</h2>
          <p className="text-xl text-gray-500 max-w-2xl mx-auto">
            Numbers that speak for themselves. Join the thousands of engineering teams transforming how software is built.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              ref={stat.ref}
              className="bg-white p-8 rounded-2xl border border-gray-200 shadow-lg text-center group hover:-translate-y-2 transition-transform duration-300"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true, threshold: 0.5 }}
            >
              <div className="font-display text-4xl lg:text-5xl font-bold text-gray-900 mb-2 group-hover:text-primary transition-colors">
                {stat.count}<span className="text-3xl text-gray-400">{stat.suffix}</span>
              </div>
              <h3 className="font-bold text-gray-800 text-lg mb-3">{stat.label}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">
                {stat.desc}
              </p>
            </motion.div>
          ))}
        </div>

        <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
          {/* Logos placeholder using text for now */}
          <div className="flex items-center justify-center font-display font-bold text-2xl text-gray-400">Google</div>
          <div className="flex items-center justify-center font-display font-bold text-2xl text-gray-400">Microsoft</div>
          <div className="flex items-center justify-center font-display font-bold text-2xl text-gray-400">Shopify</div>
          <div className="flex items-center justify-center font-display font-bold text-2xl text-gray-400">Airbnb</div>
        </div>
      </div>
    </section>
  );
};

export default Stats;
