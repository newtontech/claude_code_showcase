import React from 'react';
import { motion } from 'framer-motion';
import { useScrollReveal, useCounter } from '../hooks';

const CodeGeneration = () => {
  const [ref1, isVisible1] = useScrollReveal();
  const [ref2, isVisible2] = useScrollReveal();
  const [ref3, isVisible3] = useScrollReveal();
  const [counterRef1, count1] = useCounter(98);
  const [counterRef2, count2] = useCounter(500);

  return (
    <section id="code" className="py-32 relative">
      <div className="max-w-7xl mx-auto px-6">
        <motion.div
          ref={ref1}
          initial={{ opacity: 0, y: 60 }}
          animate={isVisible1 ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          <div className="flex items-end gap-4 mb-16">
            <span className="vertical-text font-display font-bold text-8xl text-white/5 absolute right-10">
              CODE
            </span>
            <h2 className="font-display font-black text-5xl md:text-7xl">
              <span className="text-white/20">01.</span>
              <span className="gradient-text">代码生成</span>
            </h2>
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          <motion.div
            ref={ref2}
            className="feature-card glass rounded-2xl p-8"
            initial={{ opacity: 0, y: 60 }}
            animate={isVisible2 ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.1 }}
          >
            <div className="text-5xl mb-6">⚡️</div>
            <h3 className="font-display font-bold text-2xl mb-4">毫秒级响应</h3>
            <p className="text-white/60 leading-relaxed">
              从需求到代码，仅需数秒。Claude 理解上下文，生成符合项目规范的完整实现。
            </p>
            <div className="mt-6 pt-6 border-t border-white/10">
              <div className="flex justify-between text-sm mb-2">
                <span>生成速度</span>
                <span className="text-primary">100x 更快</span>
              </div>
              <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-primary to-secondary"
                  initial={{ width: 0 }}
                  animate={isVisible2 ? { width: '95%' } : {}}
                  transition={{ duration: 2, delay: 0.5 }}
                />
              </div>
            </div>
          </motion.div>

          <motion.div
            className="feature-card glass rounded-2xl p-8 lg:col-span-2"
            initial={{ opacity: 0, y: 60 }}
            animate={isVisible2 ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="text-5xl mb-6">🎯</div>
            <h3 className="font-display font-bold text-2xl mb-4">精准理解意图</h3>
            <p className="text-white/60 leading-relaxed mb-6">
              不是简单的代码补全，而是深度理解你的需求。Claude 分析上下文、依赖关系、最佳实践，生成可维护的高质量代码。
            </p>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="bg-white/5 rounded-lg p-4 text-center">
                <div ref={counterRef1} className="text-3xl font-display font-bold text-secondary">
                  {count1}
                </div>
                <div className="text-sm text-white/50 mt-2">% 准确率</div>
              </div>
              <div className="bg-white/5 rounded-lg p-4 text-center">
                <div ref={counterRef2} className="text-3xl font-display font-bold text-primary">
                  {count2}
                </div>
                <div className="text-sm text-white/50 mt-2">+ 语言支持</div>
              </div>
              <div className="bg-white/5 rounded-lg p-4 text-center">
                <div className="text-3xl font-display font-bold text-accent">0</div>
                <div className="text-sm text-white/50 mt-2">% 人工修改</div>
              </div>
            </div>
          </motion.div>

          <motion.div
            ref={ref3}
            className="feature-card glass rounded-2xl p-8 lg:col-span-3"
            initial={{ opacity: 0, y: 60 }}
            animate={isVisible3 ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h4 className="font-display font-bold text-xl mb-4 text-secondary">你的输入</h4>
                <div className="bg-black/50 rounded-lg p-4 font-code text-sm text-white/70">
                  "创建一个用户认证系统，包含登录、注册、密码重置功能，使用 JWT 和 bcrypt"
                </div>
              </div>
              <div>
                <h4 className="font-display font-bold text-xl mb-4 text-primary">Claude 输出</h4>
                <div className="bg-black/50 rounded-lg p-4 font-code text-xs overflow-x-auto">
                  <code className="text-green-400">// ✅ 完整的 AuthController</code>
                  <br />
                  <code className="text-green-400">// ✅ JWT 中间件</code>
                  <br />
                  <code className="text-green-400">// ✅ 密码加密服务</code>
                  <br />
                  <code className="text-green-400">// ✅ 单元测试覆盖</code>
                  <br />
                  <code className="text-green-400">// ✅ API 文档</code>
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
