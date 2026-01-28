import React from 'react';
import { motion } from 'framer-motion';
import { useCounter } from '../hooks';

const Stats = () => {
  const [ref1, count1] = useCounter(10);
  const [ref2, count2] = useCounter(100);
  const [ref3, count3] = useCounter(99);
  const [ref4, count4] = useCounter(24);

  const stats = [
    { ref: ref1, count: count1, label: '倍效率提升' },
    { ref: ref2, count: count2, label: '+ 编程语言' },
    { ref: ref3, count: count3, label: '% 代码质量' },
    { ref: ref4, count: count4, label: '/7 全天候' },
  ];

  return (
    <section className="py-20">
      <div className="max-w-7xl mx-auto px-6">
        <div className="glass rounded-3xl p-12">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                ref={stat.ref}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true, threshold: 0.5 }}
              >
                <div className="stat-number font-display gradient-text">
                  {stat.count}
                </div>
                <div className="text-white/50 mt-2">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Stats;
