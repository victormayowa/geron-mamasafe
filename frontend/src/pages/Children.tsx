import { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Plus, Filter } from 'lucide-react';
import './Mothers.css'; // Reusing styles from Mothers.css

const API_URL = 'http://localhost:8000';

interface Child {
  id: number;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  age_group: string;
  risk_level: string;
  is_high_risk: boolean;
}

export function Children() {
  const [children, setChildren] = useState<Child[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchChildren = async () => {
      try {
        const response = await axios.get(`${API_URL}/children/`);
        if (response.data && response.data.success) {
          setChildren(response.data.data);
        }
      } catch (error) {
        console.error("Failed to fetch children:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchChildren();
  }, []);

  const calculateAge = (dob: string) => {
    const birthDate = new Date(dob);
    const difference = Date.now() - birthDate.getTime();
    const ageDate = new Date(difference); 
    const years = Math.abs(ageDate.getUTCFullYear() - 1970);
    const months = ageDate.getUTCMonth();
    
    if (years === 0) return `${months} months`;
    if (years === 0 && months === 0) return 'Newborn';
    return `${years} years`;
  };

  return (
    <div className="mothers-page animate-fade-in">
      <div className="page-header">
        <div>
          <h1>Children Directory</h1>
          <p>Manage and monitor registered infants and children.</p>
        </div>
        <button className="btn btn-primary">
          <Plus size={18} />
          <span>Register Child</span>
        </button>
      </div>

      <div className="card table-container">
        <div className="table-actions">
          <div className="search-box">
            <Search size={18} className="text-muted" />
            <input type="text" placeholder="Search by name..." />
          </div>
          <button className="btn btn-outline">
            <Filter size={18} />
            <span>Filter</span>
          </button>
        </div>

        <table className="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Age</th>
              <th>Gender</th>
              <th>Group</th>
              <th>Risk Level</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} className="text-center py-4">Loading data...</td>
              </tr>
            ) : children.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-4">No children registered yet.</td>
              </tr>
            ) : (
              children.map((child) => (
                <tr key={child.id}>
                  <td>
                    <strong>{child.first_name} {child.last_name}</strong>
                  </td>
                  <td>{calculateAge(child.date_of_birth)}</td>
                  <td style={{ textTransform: 'capitalize' }}>{child.gender}</td>
                  <td>
                    <span className="stage-badge">{child.age_group?.replace('_', ' ') || 'Unknown'}</span>
                  </td>
                  <td>
                    <span className={`badge badge-${child.risk_level === 'high' ? 'red' : child.risk_level === 'medium' ? 'yellow' : 'green'}`}>
                      {child.risk_level?.toUpperCase() || 'UNKNOWN'}
                    </span>
                  </td>
                  <td>
                    <a href={`/children/${child.id}`} className="view-link">View Details</a>
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
