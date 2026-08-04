import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import './Layout.css';

export function Layout() {
  return (
    <div className="layout">
      <Sidebar />
      <main className="main-content">
        <header className="main-header glass">
          <div className="header-search">
            <input type="text" placeholder="Search patients, phone numbers..." />
          </div>
          <div className="header-actions">
            <button className="btn btn-primary">
              <span>+ New Patient</span>
            </button>
          </div>
        </header>
        <div className="page-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
