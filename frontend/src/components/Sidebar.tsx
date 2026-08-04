import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Users, UserRound, Activity, Settings } from 'lucide-react';
import './Sidebar.css';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
  { icon: Users, label: 'Mothers', path: '/mothers' },
  { icon: UserRound, label: 'Children', path: '/children' },
  { icon: Activity, label: 'Risk Board', path: '/risk' },
  { icon: Settings, label: 'Settings', path: '/settings' },
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo-container">
          <span className="logo-icon">🤱</span>
          <h2>Mamasafe</h2>
        </div>
      </div>
      
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
      
      <div className="sidebar-footer">
        <div className="user-profile">
          <div className="avatar">Dr</div>
          <div className="user-info">
            <strong>Dr. Sarah</strong>
            <span>City Health Center</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
