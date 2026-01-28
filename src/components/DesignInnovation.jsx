import React from 'react';
import { motion } from 'framer-motion';
import { useScrollReveal } from '../hooks';

const DesignInnovation = () => {
  const [ref1, isVisible1] = useScrollReveal();
  const [ref2, isVisible2] = useScrollReveal();
  const [ref4, isVisible4] = useScrollReveal();

  return (
    <section id="design" className="py-32 bg-gradient-to-b from-transparent via-[rgba(255,72,0,0.05)] to-transparent">
      <div className="max-w-7xl mx-auto px-6">
        <motion.div
          ref={ref1}
          initial={{ opacity: 0, y: 60 }}
          animate={isVisible1 ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          <div className="flex items-end gap-4 mb-16">
            <span className="vertical-text font-display font-bold text-8xl text-white/5 absolute right-10">
              DESIGN
            </span>
            <h2 className="font-display font-black text-5xl md:text-7xl">
              <span className="text-white/20">02.</span>
              <span className="gradient-text">设计创新</span>
            </h2>
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          <motion.div
            ref={ref2}
            className="feature-card glass rounded-2xl p-8"
            initial={{ opacity: 0, y: 60 }}
            animate={isVisible2 ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
          >
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-3xl mb-6">
              🎨
            </div>
            <h3 className="font-display font-bold text-2xl mb-4">独特视觉语言</h3>
            <p className="text-white/60 leading-relaxed">
              拒绝千篇一律的模板。Claude 创建具有鲜明个性的设计，每个项目都是独特的艺术作品。
            </p>
            <ul className="mt-6 space-y-3 text-sm">
              <li className="flex items-center gap-3">
                <span className="w-2 h-2 rounded-full bg-primary"></span>
                <span>大胆的色彩方案</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="w-2 h-2 rounded-full bg-secondary"></span>
                <span>独特的字体组合</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="w-2 h-2 rounded-full bg-accent"></span>
                <span>创新的布局结构</span>
              </li>
            </ul>
          </motion.div>

          <motion.div
            className="feature-card glass rounded-2xl p-8"
            initial={{ opacity: 0, y: 60 }}
            animate={isVisible2 ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.1 }}
          >
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-secondary to-accent flex items-center justify-center text-3xl mb-6">
              ✨
            </div>
            <h3 className="font-display font-bold text-2xl mb-4">微交互动画</h3>
            <p className="text-white/60 leading-relaxed">
              让界面活起来。精心设计的动效引导用户注意力，提供即时反馈，创造愉悦体验。
            </p>
            <div className="mt-6 space-y-4">
              <div className="bg-white/5 rounded-lg p-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm">悬停效果</span>
                  <span className="text-secondary font-code text-xs">60fps</span>
                </div>
              </div>
              <div className="bg-white/5 rounded-lg p-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm">滚动动画</span>
                  <span className="text-primary font-code text-xs">GPU加速</span>
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div
            className="feature-card glass rounded-2xl p-8"
            initial={{ opacity: 0, y: 60 }}
            animate={isVisible2 ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-accent to-primary flex items-center justify-center text-3xl mb-6">
              📱
            </div>
            <h3 className="font-display font-bold text-2xl mb-4">响应式完美</h3>
            <p className="text-white/60 leading-relaxed">
              在任何设备上完美呈现。从手机到 4K 显示器，设计自动适配，体验始终如一。
            </p>
            <div className="mt-6 flex gap-2">
              <div className="px-3 py-1 bg-white/10 rounded-full text-xs">📱 Mobile</div>
              <div className="px-3 py-1 bg-white/10 rounded-full text-xs">💻 Desktop</div>
              <div className="px-3 py-1 bg-white/10 rounded-full text-xs">🖥️ 4K</div>
            </div>
          </motion.div>
        </div>

        <motion.div
          ref={ref4}
          className="mt-16"
          initial={{ opacity: 0, y: 60 }}
          animate={isVisible4 ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          <div className="glass rounded-2xl p-8">
            <h4 className="font-display font-bold text-xl mb-6 text-center">设计风格示例</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="aspect-square rounded-xl bg-gradient-to-br from-gray-900 to-gray-800 border border-white/10 p-4 flex items-center justify-center">
                <span className="font-display font-bold text-center text-sm">极简未来</span>
              </div>
              <div className="aspect-square rounded-xl bg-gradient-to-br from-orange-900 to-red-900 border border-orange-500/30 p-4 flex items-center justify-center">
                <span className="font-display font-bold text-center text-sm">复古工业</span>
              </div>
              <div className="aspect-square rounded-xl bg-gradient-to-br from-cyan-900 to-blue-900 border border-cyan-500/30 p-4 flex items-center justify-center">
                <span className="font-display font-bold text-center text-sm">数字海洋</span>
              </div>
              <div className="aspect-square rounded-xl bg-gradient-to-br from-pink-900 to-purple-900 border border-pink-500/30 p-4 flex items-center justify-center">
                <span className="font-display font-bold text-center text-sm">霓虹赛博</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default DesignInnovation;
