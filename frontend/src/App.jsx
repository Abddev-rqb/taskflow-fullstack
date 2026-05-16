import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import { useAuth } from "./context/AuthContext";

import Login from "./pages/Login";
import AdminDashboard from "./pages/AdminDashboard";
import UserDashboard from "./pages/UserDashboard";
import TaskList from "./pages/TaskList";
import TaskCreate from "./pages/TaskCreate";

const App = () => {
  const { user } = useAuth();

  return (
    <>
      <Navbar />

      <main className={user ? "container py-4" : ""}>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route
            path="/admin/dashboard"
            element={
              <ProtectedRoute allowedRoles={["ADMIN"]}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/user/dashboard"
            element={
              <ProtectedRoute allowedRoles={["USER"]}>
                <UserDashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/tasks"
            element={
              <ProtectedRoute allowedRoles={["ADMIN", "USER"]}>
                <TaskList />
              </ProtectedRoute>
            }
          />

          <Route
            path="/tasks/create"
            element={
              <ProtectedRoute allowedRoles={["ADMIN"]}>
                <TaskCreate />
              </ProtectedRoute>
            }
          />

          <Route
            path="/"
            element={
              user ? (
                user.role === "ADMIN" ? (
                  <Navigate to="/admin/dashboard" replace />
                ) : (
                  <Navigate to="/user/dashboard" replace />
                )
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </>
  );
};

export default App;