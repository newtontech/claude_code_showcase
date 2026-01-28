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
      gradient: 'from-blue-500/20 to-blue-600/20',
      title: '产品经理',
      description: '需求分析、功能规划、用户故事',
    },
    {
      icon: '🎨',
      gradient: 'from-purple-500/20 to-purple-600/20',
      title: '设计师',
      description: 'UI/UX设计、设计系统、原型',
    },
    {
      icon: '💻',
      gradient: 'from-primary/20 to-primary/30',
      title: '工程师',
      description: '代码开发、测试、调试、重构',
    },
    {
      icon: '📊',
      gradient: 'from-green-500/20 to-green-600/20',
      title: '数据分析师',
      description: '数据处理、可视化、洞察',
    },
  ];

  const workflow = [
    { icon: '📝', title: '需求定义', description: '理解业务目标', color: 'blue' },
    { icon: '🎨', title: '设计原型', description: '创建视觉方案', color: 'purple' },
    { icon: '⚙️', title: '开发实现', description: '编写生产代码', color: 'primary' },
    { icon: '🚀', title: '测试部署', description: '上线监控优化', color: 'green' },
  ];

  return (
    <section id="collaboration" className="py-32 bg-gradient-to-b from-transparent via-[rgba(0,240,255,0.05)] to-transparent">
      <div className="max-w-7xl mx-auto px-6">
        <motion.div
          ref={ref1}
          initial={{ opacity: 0, y: 60 }}
          animate={isVisible1 ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          <div className="flex items-end gap-4 mb-16">
            <span className="vertical-text font-display font-bold text-8xl text-white/5 absolute right-10">
              TEAM
            </span>
            <h2 className="font-display font-black text-5xl md:text-7xl">
              <span className="text-white/20">04.</span>
              <span className="gradient-text">多域协作</span>
            </h2>
          </div>
        </motion.div>

        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0 }}
          animate={isVisible1 ? { opacity: 1 } : {}}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <p className="text-xl text-white/70 max-w-3xl mx-auto">
            Claude 不仅是编码助手，更是全能团队成员。从产品构思到部署上线，
            <span className="text-secondary">无缝衔接每个环节</span>。
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {roles.map((role, index) => (
            <motion.div
              key={index}
              ref={index === 0 ? ref2 : undefined}
              className="feature-card glass rounded-2xl p-6 text-center"
              initial={{ opacity: 0, y: 60 }}
              animate={isVisible2 ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <div className={`w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br ${role.gradient} flex items-center justify-center text-4xl`}>
                {role.icon}
              </div>
              <h4 className="font-display font-bold text-lg mb-2">{role.title}</h4>
              <p className="text-sm text-white/50">{role.description}</p>
            </motion.div>
          ))}
        </div>

        <motion.div
          ref={ref3}
          className="mt-16"
          initial={{ opacity: 0, y: 60 }}
          animate={isVisible3 ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          <div className="glass rounded-2xl p-8">
            <h4 className="font-display font-bold text-xl mb-8 text-center">端到端工作流</h4>
            <div className="flex flex-col md:flex-row items-center justify-between gap-4">
              {workflow.map((step, index) => (
                <React.Fragment key={index}>
                  <div className="flex-1 text-center p-4">
                    <div className={`w-16 h-16 mx-auto mb-4 rounded-xl ${
                      step.color === 'primary'
                        ? 'bg-primary/20'
                        : `bg-${step.color}-500/20`
                    } flex items-center justify-center text-2xl`}>
                      {step.icon}
                    </div>
                    <h5 className="font-bold mb-2">{step.title}</h5>
                    <p className="text-xs text-white/50">{step.description}</p>
                  </div>
                  {index < workflow.length - 1 && (
                    <div className={`text-2xl ${
                      index === 1 ? 'text-secondary' : index === 2 ? 'text-accent' : 'text-primary'
                    }`}>
                      →
                    </div>
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Collaboration;
