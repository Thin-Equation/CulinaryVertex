import React from 'react';

function Header() {
    return (
      <header className="fixed top-0 left-0 right-0 bg-[var(--lk-bg)] border-b border-white/10 p-4 z-50">
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <h1 className="text-white text-xl font-bold">Culinary Vertex</h1>
            <span className="ml-3 text-white/60 text-sm hidden md:inline">Fine Dining Restaurant Agent</span>
          </div>
          <div className="hidden md:flex items-center">
            <span className="text-white/70 mr-4">Reserve: (555) 123-4567</span>
          </div>
        </div>
      </header>
    );
  }

export default Header;
