import { useState } from "react";
import Login from "./Login";
import Signup from "./Signup";
import COEDashboard from "./COEDashboard";
import FacultyDashboard from "./FacultyDashboard";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState(null);
  const [selectedRole, setSelectedRole] = useState(null);
  const [showSignup, setShowSignup] = useState(false);

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserRole(null);
    setSelectedRole(null);
    localStorage.clear();
  };

  // ---------------- LANDING ----------------
  if (!selectedRole) {
    return (
      <div className="h-screen flex items-center justify-center bg-gray-100">
        <div className="flex gap-6 text-xl font-semibold">
          <button onClick={() => setSelectedRole("superadmin")}>
            SuperAdmin
          </button>
          <button onClick={() => setSelectedRole("coe")}>
            COE
          </button>
          <button onClick={() => setSelectedRole("faculty")}>
            Faculty
          </button>
        </div>
      </div>
    );
  }

  // ---------------- LOGIN ----------------
  if (!isLoggedIn) {
    return showSignup ? (
      <Signup setShowSignup={setShowSignup} />
    ) : (
      <Login
        setIsLoggedIn={setIsLoggedIn}
        setUserRole={setUserRole}
        role={selectedRole} // ✅ important
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
      <div className="p-10">
        <h1 className="text-2xl font-bold">SuperAdmin Dashboard</h1>
        <button
          onClick={handleLogout}
          className="mt-4 bg-red-500 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>
    );
  }

  return <div>Something went wrong</div>;
}

export default App;