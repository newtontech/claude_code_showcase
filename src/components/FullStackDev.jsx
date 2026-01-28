import React from 'react';
import { motion } from 'framer-motion';
import { useScrollReveal } from '../hooks';

const FullStackDev = () => {
  const [ref1, isVisible1] = useScrollReveal();
  const [ref2, isVisible2] = useScrollReveal();

  const techStack = [
    { icon: '⚛️', name: 'React' },
    { icon: '🟢', name: 'Vue' },
    { icon: '▲', name: 'Next.js' },
    { icon: '🟨', name: 'JavaScript' },
    { icon: '🐍', name: 'Python' },
    { icon: '🦀', name: 'Rust' },
    { icon: '🐘', name: 'PostgreSQL' },
    { icon: '🍃', name: 'MongoDB' },
    { icon: '🐳', name: 'Docker' },
  ];

  const features = [
    {
      icon: '🎨',
      color: 'primary',
      title: '前端框架',
      description: 'React, Vue, Next.js, Svelte',
    },
    {
      icon: '⚙️',
      color: 'secondary',
      title: '后端服务',
      description: 'Node.js, Python, Go, Rust',
    },
    {
      icon: '🗄️',
      color: 'accent',
      title: '数据库',
      description: 'PostgreSQL, MongoDB, Redis',
    },
    {
      icon: '🚀',
      gradient: true,
      title: '部署运维',
      description: 'Docker, Kubernetes, CI/CD',
    },
  ];

  return (
    <section id="fullstack" className="py-32 relative">
      <div className="max-w-7xl mx-auto px-6">
        <motion.div
          ref={ref1}
          initial={{ opacity: 0, y: 60 }}
          animate={isVisible1 ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          <div className="flex items-end gap-4 mb-16">
            <span className="vertical-text font-display font-bold text-8xl text-white/5 absolute right-10">
              FULLSTACK
            </span>
            <h2 className="font-display font-black text-5xl md:text-7xl">
              <span className="text-white/20">03.</span>
              <span className="gradient-text">全栈开发</span>
            </h2>
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <motion.p
              className="text-xl text-white/70 leading-relaxed"
              initial={{ opacity: 0 }}
              animate={isVisible1 ? { opacity: 1 } : {}}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              从前端到后端，从数据库到部署，Claude Code 涵盖完整的开发生命周期。
              <span className="text-primary">一个助手，全部搞定。</span>
            </motion.p>

            <div className="space-y-4">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  className="feature-card glass rounded-xl p-6"
                  initial={{ opacity: 0, x: -50 }}
                  animate={isVisible1 ? { opacity: 1, x: 0 } : {}}
                  transition={{ duration: 0.5, delay: 0.3 + index * 0.1 }}
                >
                  <div className="flex items-center gap-4">
                    <div
                      className={`w-12 h-12 rounded-xl ${
                        feature.gradient
                          ? 'bg-gradient-to-r from-primary/20 to-secondary/20'
                          : `bg-${feature.color}/20`
                      } flex items-center justify-center text-2xl`}
                    >
                      {feature.icon}
                    </div>
                    <div>
                      <h4 className="font-display font-bold text-lg">{feature.title}</h4>
                      <p className="text-sm text-white/50">{feature.description}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          <motion.div
            ref={ref2}
            initial={{ opacity: 0, x: 50 }}
            animate={isVisible2 ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <div className="glass rounded-2xl p-8">
              <h4 className="font-display font-bold text-xl mb-8 text-center">技术栈覆盖</h4>
              <div className="grid grid-cols-3 gap-4">
                {techStack.map((tech, index) => (
                  <motion.div
                    key={index}
                    className="aspect-square rounded-xl bg-white/5 flex flex-col items-center justify-center p-4 hover:bg-white/10 transition-colors cursor-pointer"
                    whileHover={{ scale: 1.05 }}
                    transition={{ duration: 0.2 }}
                  >
                    <div className="text-3xl mb-2">{tech.icon}</div>
                    <span className="text-xs text-center">{tech.name}</span>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default FullStackDev;
