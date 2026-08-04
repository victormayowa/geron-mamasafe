import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Mothers } from './pages/Mothers';
import { Children } from './pages/Children';
import { RiskBoard } from './pages/RiskBoard';

// Placeholder for future pages
const Placeholder = ({ title }: { title: string }) => (
  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
    <h1 style={{ color: 'var(--color-text-muted)' }}>{title} - Coming Soon</h1>
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="mothers" element={<Mothers />} />
          <Route path="children" element={<Children />} />
          <Route path="risk" element={<RiskBoard />} />
          <Route path="settings" element={<Placeholder title="Settings" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
