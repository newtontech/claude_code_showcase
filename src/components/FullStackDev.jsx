import React from 'react';
import { motion } from 'framer-motion';
import { useScrollReveal } from '../hooks';

const FullStackDev = () => {
  const [ref1, isVisible1] = useScrollReveal();
  const [ref2, isVisible2] = useScrollReveal();

  const techStack = [
    { icon: '⚛️', name: 'React', category: 'Frontend' },
    { icon: '🟢', name: 'Vue', category: 'Frontend' },
    { icon: '▲', name: 'Next.js', category: 'Framework' },
    { icon: '🟨', name: 'JavaScript', category: 'Language' },
    { icon: '🐍', name: 'Python', category: 'Backend' },
    { icon: '🦀', name: 'Rust', category: 'System' },
    { icon: '🐘', name: 'PostgreSQL', category: 'Database' },
    { icon: '🍃', name: 'MongoDB', category: 'Database' },
    { icon: '🐳', name: 'Docker', category: 'DevOps' },
  ];

  const features = [
    {
      icon: '🎨',
      color: 'bg-orange-100 text-orange-600',
      title: 'Modern Frontend Architecture',
      description: 'Scaffolds complete SPAs or SSR applications using React, Vue, or Svelte. Configures routing, state management (Redux/Zustand), and component libraries automatically.',
    },
    {
      icon: '⚙️',
      color: 'bg-slate-100 text-slate-600',
      title: 'Robust Backend Services',
      description: 'Generates production-ready APIs in Node.js, Python, (FastAPI/Django), or Go. Includes authentication, rate limiting, logging, and swagger documentation.',
    },
    {
      icon: '🗄️',
      color: 'bg-yellow-100 text-yellow-600',
      title: 'Database Design & Management',
      description: 'Writes complex SQL queries, designs normalized schemas, and creates migration scripts. Supports PostgreSQL, MySQL, MongoDB, and Redis caching layers.',
    },
    {
      icon: '🚀',
      color: 'bg-blue-100 text-blue-600',
      title: 'DevOps & Deployment',
      description: 'Dockerizes applications, writes CI/CD pipelines (GitHub Actions), and manages cloud infrastructure (AWS/Vercel) via Terraform or CLI tools.',
    },
  ];

  return (
    <section className="h-full flex flex-col justify-center py-20 bg-gray-50 relative">
      <div className="max-w-7xl mx-auto px-8 w-full">
        {/* Header */}
        <motion.div
          ref={ref1}
          initial={{ opacity: 0, y: 30 }}
          animate={isVisible1 ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="mb-16 border-b border-gray-200 pb-8"
        >
          <div className="flex items-center gap-4 mb-4">
            <span className="bg-blue-50 text-blue-600 font-bold px-3 py-1 rounded text-sm uppercase tracking-wider">Engineering</span>
            <span className="text-gray-400 font-mono">03 / 05</span>
          </div>
          <h2 className="text-5xl font-display font-bold text-gray-900 mb-6">
            Full Stack Mastery
          </h2>
          <p className="text-xl text-gray-500 max-w-3xl leading-relaxed">
            From database schemas to css animations, Claude Code navigates the entire technology stack with the expertise of a senior principal engineer.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-16 items-start">
          {/* Left Column: Features */}
          <div className="space-y-6">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all flex gap-5"
                initial={{ opacity: 0, x: -30 }}
                animate={isVisible1 ? { opacity: 1, x: 0 } : {}}
                transition={{ duration: 0.5, delay: 0.2 + index * 0.1 }}
              >
                <div className={`w-14 h-14 min-w-[3.5rem] rounded-xl ${feature.color} flex items-center justify-center text-2xl`}>
                  {feature.icon}
                </div>
                <div>
                  <h4 className="font-display font-bold text-lg text-gray-900 mb-1">{feature.title}</h4>
                  <p className="text-sm text-gray-500 leading-relaxed">{feature.description}</p>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Right Column: Tech Stack Visual */}
          <motion.div
            ref={ref2}
            className="relative"
            initial={{ opacity: 0, x: 30 }}
            animate={isVisible2 ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <div className="bg-white rounded-2xl p-8 border border-gray-200 shadow-lg">
              <h4 className="font-display font-bold text-xl mb-8 text-center text-gray-800">Supported Technologies</h4>

              <div className="grid grid-cols-3 gap-4">
                {techStack.map((tech, index) => (
                  <motion.div
                    key={index}
                    className="aspect-square rounded-xl bg-gray-50 border border-gray-100 flex flex-col items-center justify-center p-4 hover:bg-gray-100 hover:border-gray-300 transition-all cursor-default group"
                    whileHover={{ scale: 1.05 }}
                    transition={{ duration: 0.2 }}
                  >
                    <div className="text-4xl mb-3 grayscale group-hover:grayscale-0 transition-all duration-300">{tech.icon}</div>
                    <span className="text-sm font-bold text-gray-700">{tech.name}</span>
                    <span className="text-[10px] text-gray-400 mt-1 uppercase tracking-wide">{tech.category}</span>
                  </motion.div>
                ))}
              </div>

              <div className="mt-8 pt-6 border-t border-gray-100 text-center">
                <p className="text-xs text-gray-400 uppercase tracking-widest font-bold">And many more</p>
              </div>
            </div>

            {/* Decorative Elements */}
            <div className="absolute -z-10 top-10 -right-10 w-full h-full bg-primary/5 rounded-2xl"></div>
            <div className="absolute -z-20 -bottom-5 -left-5 w-full h-full bg-blue-50 rounded-2xl"></div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default FullStackDev;
