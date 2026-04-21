import { useState } from "react";
import Landing from "./Landing";
import Login from "./Login";
import COEDashboard from "./COEDashboard";
import FacultyDashboard from "./FacultyDashboard";
import SuperAdminSignup from "./SuperAdminSignup";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState(null);
  const [selectedRole, setSelectedRole] = useState(null);

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserRole(null);
    setSelectedRole(null);
    localStorage.clear();
  };

  // ---------------- LANDING ----------------
  if (!selectedRole) {
    return <Landing setSelectedRole={setSelectedRole} />;
  }

  // ---------------- LOGIN / SIGNUP ----------------
  if (!isLoggedIn) {
    if (selectedRole === "superadmin") {
      return <SuperAdminSignup />;
    }

    return (
      <Login
        setIsLoggedIn={setIsLoggedIn}
        setUserRole={setUserRole}
        role={selectedRole}
      />
    );
  }

  // ---------------- DASHBOARDS ----------------
  if (userRole === "coe") {
    return <COEDashboard handleLogout={handleLogout} />;
  }

  if (userRole === "faculty") {
    return <FacultyDashboard handleLogout={handleLogout} />;
  }

  if (userRole === "superadmin") {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
        <h1 className="text-2xl font-bold mb-4">
          SuperAdmin Dashboard
        </h1>

        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>
    );
  }

  return <div>Something went wrong ❌</div>;
}

export default App;