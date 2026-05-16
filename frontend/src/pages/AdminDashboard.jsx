import { useEffect, useState } from "react";
import api from "../api/axios";

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  const fetchStats = async () => {
    try {
      const response = await api.get("/dashboard/admin/");
      setStats(response.data);
    } catch (err) {
      setError("Failed to load admin dashboard.");
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  if (error) {
    return <div className="alert alert-danger mt-4">{error}</div>;
  }

  if (!stats) {
    return <h5 className="mt-4">Loading dashboard...</h5>;
  }

  const cards = [
    { label: "Total Users", value: stats.total_users },
    { label: "Total Admins", value: stats.total_admins },
    { label: "Total Tasks", value: stats.total_tasks },
    { label: "Pending Tasks", value: stats.pending_tasks },
    { label: "In Progress", value: stats.in_progress_tasks },
    { label: "Completed", value: stats.completed_tasks },
    { label: "High Priority", value: stats.high_priority_tasks },
    { label: "Overdue Tasks", value: stats.overdue_tasks },
  ];

  return (
    <div>
      <h2 className="fw-bold mb-4">Admin Dashboard</h2>

      <div className="row g-3">
        {cards.map((card) => (
          <div className="col-md-3" key={card.label}>
            <div className="card shadow-sm dashboard-card">
              <div className="card-body">
                <p className="text-muted mb-1">{card.label}</p>
                <h3 className="fw-bold">{card.value}</h3>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminDashboard;