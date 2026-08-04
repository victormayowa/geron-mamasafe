import { useState, useEffect } from 'react';
import axios from 'axios';
import { AlertTriangle, Phone, Activity } from 'lucide-react';
import './Mothers.css'; // Reusing some base styles

const API_URL = 'http://localhost:8000';

interface Patient {
  id: string;
  type: 'mother' | 'child';
  name: string;
  contact: string;
  details: string;
  risk_level: string;
}

export function RiskBoard() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHighRiskPatients = async () => {
      try {
        // Fetch high risk mothers
        const mothersRes = await axios.get(`${API_URL}/mothers/?is_high_risk=true&size=50`);
        const mothers = mothersRes.data?.data || [];
        
        // Fetch children (filtering high risk on frontend for now)
        const childrenRes = await axios.get(`${API_URL}/children/?size=100`);
        const allChildren = childrenRes.data?.data || [];
        const highRiskChildren = allChildren.filter((c: any) => c.is_high_risk === true);

        // Map to unified patient structure
        const mappedMothers = mothers.map((m: any) => ({
          id: `m-${m.id}`,
          type: 'mother',
          name: `${m.first_name} ${m.last_name}`,
          contact: m.phone_number,
          details: m.pregnancy_stage.replace('_', ' '),
          risk_level: m.risk_level
        }));

        const mappedChildren = highRiskChildren.map((c: any) => ({
          id: `c-${c.id}`,
          type: 'child',
          name: `${c.first_name} ${c.last_name}`,
          contact: `Mother ID: ${c.mother_id}`,
          details: c.age_group?.replace('_', ' ') || 'Unknown age',
          risk_level: c.risk_level
        }));

        setPatients([...mappedMothers, ...mappedChildren]);
      } catch (error) {
        console.error("Failed to fetch high-risk patients:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchHighRiskPatients();
  }, []);

  return (
    <div className="mothers-page animate-fade-in">
      <div className="page-header" style={{ borderBottom: '2px solid var(--color-danger)', paddingBottom: '1rem' }}>
        <div>
          <h1 style={{ color: 'var(--color-danger)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertTriangle size={28} />
            Risk Board (Critical Cases)
          </h1>
          <p>Immediate attention required for these flagged patients.</p>
        </div>
      </div>

      <div className="card table-container" style={{ borderColor: 'var(--color-danger-light)' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Patient Type</th>
              <th>Name</th>
              <th>Details</th>
              <th>Contact</th>
              <th>Severity</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} className="text-center py-4">Loading critical data...</td>
              </tr>
            ) : patients.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-4" style={{ color: 'var(--color-success)' }}>
                  No high-risk patients currently! Excellent.
                </td>
              </tr>
            ) : (
              patients.map((patient) => (
                <tr key={patient.id} style={{ backgroundColor: 'var(--color-danger-light)' }}>
                  <td>
                    <span className="stage-badge" style={{ backgroundColor: 'white', color: 'var(--color-danger)', fontWeight: 'bold' }}>
                      {patient.type.toUpperCase()}
                    </span>
                  </td>
                  <td>
                    <strong>{patient.name}</strong>
                  </td>
                  <td style={{ textTransform: 'capitalize' }}>{patient.details}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <Phone size={14} />
                      {patient.contact}
                    </div>
                  </td>
                  <td>
                    <span className="badge badge-red" style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', width: 'fit-content' }}>
                      <Activity size={14} />
                      EMERGENCY
                    </span>
                  </td>
                  <td>
                    <button className="btn btn-primary" style={{ backgroundColor: 'var(--color-danger)', padding: '0.25rem 0.75rem' }}>
                      Intervene
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
