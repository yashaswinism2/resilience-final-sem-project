import { useState } from "react";

const BASE_URL = "http://127.0.0.1:8000";

export default function Login({ setIsLoggedIn, setUserRole, role }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [instituteId, setInstituteId] = useState("");

  const handleLogin = async () => {
    try {
      const res = await fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
          role, // ✅ role from Landing
          institute_id: instituteId ? Number(instituteId) : null,
        }),
      });

      const data = await res.json();

      if (res.ok) {
        alert(`Login successful as ${role} ✅`);

        // ✅ SET STATE (FIXED)
        setIsLoggedIn(true);
        setUserRole(role);

        // ✅ STORE CORRECT ROLE
        localStorage.setItem("role", role);
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("institute_id", data.institute_id);

      } else {
        alert(data.detail || "Invalid credentials ❌");
      }
    } catch (err) {
      console.error("Login error:", err);
      alert("Backend connection error ❌");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-100 to-purple-200 px-4">
      
      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-sm text-center">

        <h2 className="text-2xl font-bold mb-2 text-gray-800">
          Login
        </h2>

        <p className="text-sm text-gray-500 mb-6">
          Role: <span className="font-semibold capitalize">{role}</span>
        </p>

        {/* Username */}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="mb-3 p-2 border rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        {/* Password */}
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="mb-3 p-2 border rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        {/* Institute ID */}
        <input
          type="number"
          placeholder="Institute ID"
          value={instituteId}
          onChange={(e) => setInstituteId(e.target.value)}
          className="mb-5 p-2 border rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        {/* Login Button */}
        <button
          onClick={handleLogin}
          className="bg-blue-600 hover:bg-blue-700 text-white py-2 w-full rounded-lg transition"
        >
          Login
        </button>

      </div>
    </div>
  );
}