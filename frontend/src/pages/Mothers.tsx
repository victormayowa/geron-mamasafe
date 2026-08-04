import { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Plus, Filter } from 'lucide-react';
import './Mothers.css';

// Using local API url, in production this should be from env
const API_URL = 'http://localhost:8000';

interface Mother {
  id: number;
  first_name: string;
  last_name: string;
  phone_number: string;
  pregnancy_stage: string;
  risk_level: string;
  is_high_risk: boolean;
}

export function Mothers() {
  const [mothers, setMothers] = useState<Mother[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMothers = async () => {
      try {
        const response = await axios.get(`${API_URL}/mothers/`);
        if (response.data && response.data.success) {
          setMothers(response.data.data);
        }
      } catch (error) {
        console.error("Failed to fetch mothers:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchMothers();
  }, []);

  return (
    <div className="mothers-page animate-fade-in">
      <div className="page-header">
        <div>
          <h1>Mothers Directory</h1>
          <p>Manage and monitor registered pregnant women and mothers.</p>
        </div>
        <button className="btn btn-primary">
          <Plus size={18} />
          <span>Register Mother</span>
        </button>
      </div>

      <div className="card table-container">
        <div className="table-actions">
          <div className="search-box">
            <Search size={18} className="text-muted" />
            <input type="text" placeholder="Search by name or phone..." />
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
              <th>Phone</th>
              <th>Pregnancy Stage</th>
              <th>Risk Level</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} className="text-center py-4">Loading data...</td>
              </tr>
            ) : mothers.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-4">No mothers registered yet.</td>
              </tr>
            ) : (
              mothers.map((mother) => (
                <tr key={mother.id}>
                  <td>
                    <strong>{mother.first_name} {mother.last_name}</strong>
                  </td>
                  <td>{mother.phone_number}</td>
                  <td>
                    <span className="stage-badge">{mother.pregnancy_stage.replace('_', ' ')}</span>
                  </td>
                  <td>
                    <span className={`badge badge-${mother.risk_level === 'high' ? 'red' : mother.risk_level === 'medium' ? 'yellow' : 'green'}`}>
                      {mother.risk_level.toUpperCase()}
                    </span>
                  </td>
                  <td>
                    {mother.is_high_risk ? (
                      <span className="text-danger font-semibold">High Priority</span>
                    ) : (
                      <span className="text-success">Routine</span>
                    )}
                  </td>
                  <td>
                    <a href={`/mothers/${mother.id}`} className="view-link">View Details</a>
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
