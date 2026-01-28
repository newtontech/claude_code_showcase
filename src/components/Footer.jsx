import React from 'react';

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="py-12 border-t border-white/10">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="font-display font-bold text-xl gradient-text">
            CLAUDE CODE
          </div>
          <div className="text-white/50 text-sm">
            © {year} Anthropic. 让开发更智能。
          </div>
          <div className="flex gap-6">
            <a href="#" className="text-white/50 hover:text-white transition-colors">
              文档
            </a>
            <a href="#" className="text-white/50 hover:text-white transition-colors">
              GitHub
            </a>
            <a href="#" className="text-white/50 hover:text-white transition-colors">
              Twitter
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
