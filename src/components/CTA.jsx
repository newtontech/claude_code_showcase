import React from 'react';
import { motion } from 'framer-motion';
import { useScrollReveal } from '../hooks';

const CTA = () => {
  const [ref, isVisible] = useScrollReveal();

  return (
    <section className="py-32 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-r from-primary/10 via-transparent to-secondary/10"></div>
      <div className="max-w-4xl mx-auto px-6 text-center relative z-10">
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 60 }}
          animate={isVisible ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          <h2 className="font-display font-black text-4xl md:text-6xl mb-8">
            <span className="gradient-text">准备好</span>
            <br />
            <span className="text-white">革命你的</span>
            <br />
            <span className="gradient-text">开发流程了吗？</span>
          </h2>
          <p className="text-xl text-white/70 mb-12 max-w-2xl mx-auto">
            加入数以万计的开发者，让 Claude Code 成为你的超级助手。
            <br />
            从今天开始，体验前所未有的开发效率。
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <button className="btn-primary px-12 py-5 rounded-full font-bold text-lg text-white">
              免费开始使用 →
            </button>
            <button className="glass px-12 py-5 rounded-full font-bold text-lg hover:bg-white/10 transition-colors">
              预约演示
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default CTA;
