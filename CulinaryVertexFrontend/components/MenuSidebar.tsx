import React from 'react';
import { CloseIcon } from "@/components/CloseIcon";

interface MenuSidebarProps {
    isOpen: boolean;
    toggleSidebar: () => void;
  }

function MenuSidebar({ isOpen, toggleSidebar }: MenuSidebarProps) {
    return (
        <div className={`menu-sidebar fixed left-0 top-16 h-[calc(100%-64px)] bg-[var(--lk-bg)] border-r border-white/10 w-80 transition-transform duration-300 z-40 ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
          <div className="p-4 border-b border-white/10 flex justify-between items-center">
            <h3 className="text-white font-semibold">Our Menu</h3>
            <button onClick={toggleSidebar} className="text-white/70 hover:text-white">
              <CloseIcon />
            </button>
          </div>
          
          <div className="p-4 h-[calc(100%-64px)] overflow-y-auto">
            {/* Appetizers */}
            <div className="mb-6">
              <h4 className="text-amber-500 font-semibold mb-3 text-lg">Appetizers</h4>
              <div className="space-y-4">
                <div className="border-b border-white/10 pb-3">
                  <div className="flex justify-between">
                    <h5 className="text-white font-medium">Truffle Arancini</h5>
                    <span className="text-white">$16</span>
                  </div>
                  <p className="text-white/70 text-sm mt-1">Crispy risotto balls with black truffle and parmesan</p>
                </div>
                <div className="border-b border-white/10 pb-3">
                  <div className="flex justify-between">
                    <h5 className="text-white font-medium">Tuna Tartare</h5>
                    <span className="text-white">$18</span>
                  </div>
                  <p className="text-white/70 text-sm mt-1">Fresh tuna with avocado, sesame, and yuzu ponzu</p>
                </div>
                <div className="border-b border-white/10 pb-3">
                  <div className="flex justify-between">
                    <h5 className="text-white font-medium">Burrata Salad</h5>
                    <span className="text-white">$14</span>
                  </div>
                  <p className="text-white/70 text-sm mt-1">Creamy burrata with heirloom tomatoes and basil oil</p>
                </div>
              </div>
            </div>
            
            {/* Main Courses */}
            <div className="mb-6">
              <h4 className="text-amber-500 font-semibold mb-3 text-lg">Main Courses</h4>
              <div className="space-y-4">
                <div className="border-b border-white/10 pb-3">
                  <div className="flex justify-between">
                    <h5 className="text-white font-medium">Wagyu Ribeye</h5>
                    <span className="text-white">$55</span>
                  </div>
                  <p className="text-white/70 text-sm mt-1">A5 Japanese Wagyu with roasted vegetables and red wine jus</p>
                </div>
                <div className="border-b border-white/10 pb-3">
                  <div className="flex justify-between">
                    <h5 className="text-white font-medium">Chilean Sea Bass</h5>
                    <span className="text-white">$42</span>
                  </div>
                  <p className="text-white/70 text-sm mt-1">Miso-glazed sea bass with bok choy and ginger scallion sauce</p>
                </div>
                <div className="border-b border-white/10 pb-3">
                  <div className="flex justify-between">
                    <h5 className="text-white font-medium">Wild Mushroom Risotto</h5>
                    <span className="text-white">$28</span>
                  </div>
                  <p className="text-white/70 text-sm mt-1">Creamy Arborio rice with seasonal wild mushrooms and white truffle oil</p>
                </div>
              </div>
            </div>
            
            {/* Desserts */}
            <div className="mb-6">
              <h4 className="text-amber-500 font-semibold mb-3 text-lg">Desserts</h4>
              <div className="space-y-4">
                <div className="border-b border-white/10 pb-3">
                  <div className="flex justify-between">
                    <h5 className="text-white font-medium">Chocolate Soufflé</h5>
                    <span className="text-white">$14</span>
                  </div>
                  <p className="text-white/70 text-sm mt-1">Warm chocolate soufflé with vanilla bean ice cream</p>
                </div>
                <div className="border-b border-white/10 pb-3">
                  <div className="flex justify-between">
                    <h5 className="text-white font-medium">Crème Brûlée</h5>
                    <span className="text-white">$12</span>
                  </div>
                  <p className="text-white/70 text-sm mt-1">Classic vanilla bean custard with caramelized sugar</p>
                </div>
              </div>
            </div>
            
            {/* Beverages */}
            <div>
              <h4 className="text-amber-500 font-semibold mb-3 text-lg">Beverages</h4>
              <div className="space-y-4">
                <div className="border-b border-white/10 pb-3">
                  <div className="flex justify-between">
                    <h5 className="text-white font-medium">Wine Selection</h5>
                    <span className="text-white">$12-25</span>
                  </div>
                  <p className="text-white/70 text-sm mt-1">Ask our voice assistant about our curated wine list</p>
                </div>
                <div className="border-b border-white/10 pb-3">
                  <div className="flex justify-between">
                    <h5 className="text-white font-medium">Signature Cocktails</h5>
                    <span className="text-white">$16</span>
                  </div>
                  <p className="text-white/70 text-sm mt-1">Handcrafted cocktails with premium spirits</p>
                </div>
              </div>
            </div>
          </div>
          <button onClick={toggleSidebar} className="px-4 py-1 rounded bg-amber-600 text-white text-sm hover:bg-amber-500">Menu</button>
        </div>
      );
    }
    
    export default MenuSidebar;
