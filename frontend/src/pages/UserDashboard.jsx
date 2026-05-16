import { useEffect, useState } from "react";
import api from "../api/axios";

const UserDashboard = () => {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  const fetchStats = async () => {
    try {
      const response = await api.get("/dashboard/user/");
      setStats(response.data);
    } catch (err) {
      setError("Failed to load user dashboard.");
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
    { label: "My Total Tasks", value: stats.total_tasks },
    { label: "Pending", value: stats.pending_tasks },
    { label: "In Progress", value: stats.in_progress_tasks },
    { label: "Completed", value: stats.completed_tasks },
    { label: "High Priority", value: stats.high_priority_tasks },
  ];

  return (
    <div>
      <h2 className="fw-bold mb-4">User Dashboard</h2>

      <div className="row g-3 mb-4">
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

      <div className="card shadow-sm">
        <div className="card-body">
          <h5 className="fw-bold mb-3">Upcoming Due Tasks</h5>

          {stats.upcoming_due_tasks.length === 0 ? (
            <p className="text-muted mb-0">No upcoming due tasks.</p>
          ) : (
            <div className="table-responsive">
              <table className="table table-bordered align-middle">
                <thead>
                  <tr>
                    <th>Title</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Due Date</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.upcoming_due_tasks.map((task) => (
                    <tr key={task.id}>
                      <td>{task.title}</td>
                      <td>{task.status}</td>
                      <td>{task.priority}</td>
                      <td>{task.due_date}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;