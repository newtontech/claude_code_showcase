import React from 'react';

const Marquee = () => {
  return (
    <section className="py-8 bg-primary overflow-hidden">
      <div className="whitespace-nowrap animate-marquee">
        <span className="inline-block px-8 font-display font-bold text-lg text-black">
          AI驱动开发 ★ 实时代码生成 ★ 智能重构 ★ 自动测试 ★ 多语言支持 ★ 端到端解决方案
          ★ AI驱动开发 ★ 实时代码生成 ★ 智能重构 ★ 自动测试 ★ 多语言支持 ★ 端到端解决方案
        </span>
      </div>
    </section>
  );
};

export default Marquee;
