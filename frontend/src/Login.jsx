import { useState } from "react";

const BASE_URL = "http://127.0.0.1:8000";

export default function Login({ setIsLoggedIn, setUserRole, role }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [instituteId, setInstituteId] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!username || !password) {
      alert("Please enter username and password ❗");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
          role,
          institute_id: instituteId ? Number(instituteId) : null,
        }),
      });

      const data = await res.json();

      if (res.ok) {
        alert(`Login successful as ${role} ✅`);

        setIsLoggedIn(true);
        setUserRole(role);

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

    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-200 via-purple-200 to-pink-200 px-4">

      {/* Card */}
      <div className="bg-white/80 backdrop-blur-lg shadow-2xl rounded-3xl p-8 w-full max-w-md text-center">

        {/* Title */}
        <h2 className="text-3xl font-bold text-gray-800 mb-2">
          Welcome Back 👋
        </h2>

        <p className="text-sm text-gray-500 mb-6">
          Login as <span className="font-semibold capitalize text-blue-600">{role}</span>
        </p>

        {/* Username */}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="mb-3 p-3 border rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
        />

        {/* Password */}
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="mb-3 p-3 border rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
        />

        {/* Institute ID */}
        <input
          type="number"
          placeholder="Institute ID (optional)"
          value={instituteId}
          onChange={(e) => setInstituteId(e.target.value)}
          className="mb-5 p-3 border rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
        />

        {/* Button */}
        <button
          onClick={handleLogin}
          disabled={loading}
          className={`w-full py-3 rounded-lg text-white font-medium transition ${
            loading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        {/* Footer */}
        <p className="text-xs text-gray-400 mt-6">
          Intelligent Question Paper Generator
        </p>

      </div>
    </div>
  );
}