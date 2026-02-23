import React from 'react';

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="py-12 border-t border-gray-100 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary rounded-lg"></div>
            <div className="font-display font-bold text-xl text-gray-900 tracking-tight">
              CLAUDE CODE
            </div>
          </div>

          <div className="text-gray-400 text-sm">
            © {year} Anthropic. Engineering Intelligence.
          </div>

          <div className="flex gap-8">
            <a href="#" className="text-gray-500 hover:text-primary transition-colors font-medium">
              Documentation
            </a>
            <a href="#" className="text-gray-500 hover:text-primary transition-colors font-medium">
              GitHub
            </a>
            <a href="#" className="text-gray-500 hover:text-primary transition-colors font-medium">
              Twitter
            </a>
            <a href="#" className="text-gray-500 hover:text-primary transition-colors font-medium">
              Privacy
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
