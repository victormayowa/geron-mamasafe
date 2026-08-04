import { Users, AlertTriangle, CheckCircle, Activity } from 'lucide-react';
import './Dashboard.css';

export function Dashboard() {
  return (
    <div className="dashboard animate-fade-in">
      <div className="dashboard-header">
        <h1>Overview</h1>
        <p>Monitor maternal and child health status in real-time.</p>
      </div>

      <div className="stats-grid">
        <div className="card stat-card">
          <div className="stat-icon" style={{ backgroundColor: 'var(--color-primary-light)', color: 'var(--color-primary)' }}>
            <Users size={24} />
          </div>
          <div className="stat-info">
            <h3>Registered Mothers</h3>
            <p className="stat-value">1,248</p>
            <span className="stat-change positive">+12% this month</span>
          </div>
        </div>

        <div className="card stat-card">
          <div className="stat-icon" style={{ backgroundColor: 'var(--color-danger-light)', color: 'var(--color-danger)' }}>
            <AlertTriangle size={24} />
          </div>
          <div className="stat-info">
            <h3>Critical Cases (Red)</h3>
            <p className="stat-value">14</p>
            <span className="stat-change negative">+3 since yesterday</span>
          </div>
        </div>

        <div className="card stat-card">
          <div className="stat-icon" style={{ backgroundColor: 'var(--color-warning-light)', color: 'var(--color-warning)' }}>
            <Activity size={24} />
          </div>
          <div className="stat-info">
            <h3>Warning Cases (Yellow)</h3>
            <p className="stat-value">86</p>
            <span className="stat-change neutral">Stable</span>
          </div>
        </div>

        <div className="card stat-card">
          <div className="stat-icon" style={{ backgroundColor: 'var(--color-success-light)', color: 'var(--color-success)' }}>
            <CheckCircle size={24} />
          </div>
          <div className="stat-info">
            <h3>Safe Cases (Green)</h3>
            <p className="stat-value">1,148</p>
            <span className="stat-change positive">+15% this month</span>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="card recent-alerts">
          <h2>Recent AI Triage Alerts</h2>
          <div className="alert-list">
            <div className="alert-item">
              <span className="badge badge-red">Emergency</span>
              <div className="alert-details">
                <strong>Aisha Mohammed</strong>
                <p>Reported severe bleeding (3rd Trimester)</p>
                <small>10 mins ago</small>
              </div>
            </div>
            <div className="alert-item">
              <span className="badge badge-red">Emergency</span>
              <div className="alert-details">
                <strong>Baby Fatima</strong>
                <p>Difficulty breathing, chest indrawing</p>
                <small>45 mins ago</small>
              </div>
            </div>
            <div className="alert-item">
              <span className="badge badge-yellow">Warning</span>
              <div className="alert-details">
                <strong>Grace Okafor</strong>
                <p>Persistent headache, blurred vision</p>
                <small>2 hours ago</small>
              </div>
            </div>
          </div>
          <button className="btn btn-primary" style={{ marginTop: '1rem', width: '100%' }}>View All Alerts</button>
        </div>

        <div className="card upcoming-appointments">
          <h2>Upcoming ANC Appointments</h2>
          <div className="appointment-list">
            <div className="appointment-item">
              <div className="avatar">ZA</div>
              <div className="appointment-details">
                <strong>Zainab Abubakar</strong>
                <p>Week 24 Checkup</p>
              </div>
              <span className="time">Today, 10:00 AM</span>
            </div>
            <div className="appointment-item">
              <div className="avatar">CN</div>
              <div className="appointment-details">
                <strong>Chioma Nwosu</strong>
                <p>Week 36 Checkup</p>
              </div>
              <span className="time">Today, 11:30 AM</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
