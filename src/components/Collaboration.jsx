import React from 'react';
import { motion } from 'framer-motion';
import { useScrollReveal } from '../hooks';

const Collaboration = () => {
  const [ref1, isVisible1] = useScrollReveal();
  const [ref2, isVisible2] = useScrollReveal();
  const [ref3, isVisible3] = useScrollReveal();

  const roles = [
    {
      icon: '💡',
      color: 'bg-blue-100 text-blue-600',
      title: 'Product Manager',
      description: 'Breaks down high-level ambiguous requirements into structured user stories and acceptance criteria. Prioritizes features based on impact and feasibility.',
    },
    {
      icon: '🎨',
      color: 'bg-purple-100 text-purple-600',
      title: 'UI/UX Designer',
      description: 'Translates functional requirements into visual systems. Generates accessible color palettes, typography hierarchies, and responsive layout grids.',
    },
    {
      icon: '💻',
      color: 'bg-orange-100 text-orange-600',
      title: 'Senior Engineer',
      description: 'Architects scalable solutions, writes clean maintainable code, refactors legacy debt, and ensures test coverage across the entire stack.',
    },
    {
      icon: '🔎',
      color: 'bg-green-100 text-green-600',
      title: 'QA Engineer',
      description: 'Writes comprehensive E2E test suites, performs regression testing, and identifies edge cases before they reach production.',
    },
  ];

  const workflow = [
    { icon: '📝', title: 'Requirements', description: 'Analyze intent & context', color: 'bg-blue-50 text-blue-600 border-blue-100' },
    { icon: '📐', title: 'Planning', description: 'Architectural design', color: 'bg-purple-50 text-purple-600 border-purple-100' },
    { icon: '⚡', title: 'Execution', description: 'Code generation & refinement', color: 'bg-orange-50 text-orange-600 border-orange-100' },
    { icon: '✅', title: 'Verification', description: 'Testing & optimization', color: 'bg-green-50 text-green-600 border-green-100' },
  ];

  return (
    <section className="h-full flex flex-col justify-center py-20 bg-white relative">
      {/* Background */}
      <div className="absolute top-0 right-0 w-full h-1/2 bg-gray-50 -z-10 skew-y-3 origin-top-left transform scale-110"></div>

      <div className="max-w-7xl mx-auto px-8 w-full">
        <motion.div
          ref={ref1}
          initial={{ opacity: 0, y: 30 }}
          animate={isVisible1 ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="mb-16 border-b border-gray-200 pb-8"
        >
          <div className="flex items-center gap-4 mb-4">
            <span className="bg-purple-50 text-purple-600 font-bold px-3 py-1 rounded text-sm uppercase tracking-wider">Workforce Multiplier</span>
            <span className="text-gray-400 font-mono">04 / 05</span>
          </div>
          <h2 className="text-5xl font-display font-bold text-gray-900 mb-6">
            Multimodal Collaboration
          </h2>
          <p className="text-xl text-gray-500 max-w-3xl leading-relaxed">
            Claude isn't just a chatbot; it's an entire product team in your terminal. It creates artifacts, plans tasks, and executes cross-domain workflows seamlessly.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {roles.map((role, index) => (
            <motion.div
              key={index}
              ref={index === 0 ? ref2 : undefined}
              className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-lg transition-all"
              initial={{ opacity: 0, y: 30 }}
              animate={isVisible2 ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <div className={`w-16 h-16 mb-6 rounded-2xl ${role.color} flex items-center justify-center text-3xl`}>
                {role.icon}
              </div>
              <h4 className="font-display font-bold text-lg text-gray-900 mb-3">{role.title}</h4>
              <p className="text-sm text-gray-500 leading-relaxed">{role.description}</p>
            </motion.div>
          ))}
        </div>

        <motion.div
          ref={ref3}
          initial={{ opacity: 0, y: 30 }}
          animate={isVisible3 ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="bg-white rounded-2xl border border-gray-200 shadow-lg p-8 relative overflow-hidden"
        >
          <h4 className="font-display font-bold text-xl mb-8 text-center text-gray-800">End-to-End Autonomous Workflow</h4>

          {/* Connecting Line */}
          <div className="absolute top-1/2 left-0 w-full h-0.5 bg-gray-100 -z-10 hidden md:block"></div>

          <div className="flex flex-col md:flex-row items-center justify-between gap-4 relative z-10">
            {workflow.map((step, index) => (
              <React.Fragment key={index}>
                <div className={`flex-1 text-center p-6 rounded-xl bg-white border ${step.color} transition-transform hover:-translate-y-1 w-full md:w-auto`}>
                  <div className="text-4xl mb-3">{step.icon}</div>
                  <h5 className="font-bold text-gray-900 mb-1">{step.title}</h5>
                  <p className="text-xs text-gray-500">{step.description}</p>
                </div>
                {index < workflow.length - 1 && (
                  <div className="hidden md:block text-gray-300 text-2xl">➔</div>
                )}
                {index < workflow.length - 1 && (
                  <div className="md:hidden text-gray-300 text-2xl my-2">↓</div>
                )}
              </React.Fragment>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Collaboration;
