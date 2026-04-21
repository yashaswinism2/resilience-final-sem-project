import { useState } from "react";
import Login from "./Login";
import SuperAdminSignup from "./SuperAdminSignup";

export default function Landing({ setIsLoggedIn, setUserRole }) {
  const [selectedRole, setSelectedRole] = useState(null);

  if (selectedRole === "superadmin") {
    return <SuperAdminSignup />;
  }

  if (selectedRole === "coe" || selectedRole === "faculty") {
    return (
      <Login
        setIsLoggedIn={setIsLoggedIn}
        setUserRole={setUserRole}
        role={selectedRole}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-200 via-purple-200 to-pink-200 flex items-center justify-center px-4">

      {/* Main Card */}
      <div className="backdrop-blur-lg bg-white/70 shadow-2xl rounded-3xl p-10 w-full max-w-3xl text-center">

        {/* Header */}
        <h1 className="text-4xl font-bold text-gray-800 mb-3">
          Welcome 👋
        </h1>
        <p className="text-gray-600 mb-10 text-lg">
          Select your role to continue
        </p>

        {/* Role Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          {/* Super Admin */}
          <div
            onClick={() => setSelectedRole("superadmin")}
            className="cursor-pointer p-6 rounded-2xl bg-white shadow-md hover:shadow-xl hover:scale-105 transition-all duration-300"
          >
            <div className="text-4xl mb-3">👑</div>
            <h2 className="font-semibold text-lg text-purple-700">
              Super Admin
            </h2>
            <p className="text-sm text-gray-500 mt-2">
              Manage system & users
            </p>
          </div>

          {/* COE */}
          <div
            onClick={() => setSelectedRole("coe")}
            className="cursor-pointer p-6 rounded-2xl bg-white shadow-md hover:shadow-xl hover:scale-105 transition-all duration-300"
          >
            <div className="text-4xl mb-3">🏫</div>
            <h2 className="font-semibold text-lg text-blue-700">
              COE
            </h2>
            <p className="text-sm text-gray-500 mt-2">
              Control exam process
            </p>
          </div>

          {/* Faculty */}
          <div
            onClick={() => setSelectedRole("faculty")}
            className="cursor-pointer p-6 rounded-2xl bg-white shadow-md hover:shadow-xl hover:scale-105 transition-all duration-300"
          >
            <div className="text-4xl mb-3">👩‍🏫</div>
            <h2 className="font-semibold text-lg text-green-700">
              Faculty
            </h2>
            <p className="text-sm text-gray-500 mt-2">
              Generate question papers
            </p>
          </div>

        </div>

        {/* Footer */}
        <p className="text-xs text-gray-500 mt-10">
          Intelligent Question Paper Generator
        </p>

      </div>
    </div>
  );
}