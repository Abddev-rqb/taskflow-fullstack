import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  if (!user) {
    return null;
  }

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-4">
      <Link className="navbar-brand fw-bold" to="/">
        TaskFlow
      </Link>

      <div className="navbar-nav me-auto">
        {user.role === "ADMIN" && (
          <>
            <Link className="nav-link" to="/admin/dashboard">
              Dashboard
            </Link>
            <Link className="nav-link" to="/tasks">
              Tasks
            </Link>
            <Link className="nav-link" to="/tasks/create">
              Create Task
            </Link>
          </>
        )}

        {user.role === "USER" && (
          <>
            <Link className="nav-link" to="/user/dashboard">
              Dashboard
            </Link>
            <Link className="nav-link" to="/tasks">
              My Tasks
            </Link>
          </>
        )}
      </div>

      <div className="d-flex align-items-center text-white gap-3">
        <span>
          {user.username} ({user.role})
        </span>
        <button className="btn btn-outline-light btn-sm" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;