import { useState } from "react";

const BASE_URL = "http://127.0.0.1:8000";

export default function SuperAdminLogin({ setIsLoggedIn, setUserRole, setShowSignup }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

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
          role: "superadmin",
        }),
      });

      const data = await res.json();

      if (res.ok) {
        alert("SuperAdmin Login successful ✅");

        setIsLoggedIn(true);
        setUserRole("superadmin");

        localStorage.setItem("role", "superadmin");
      } else {
        alert(data.detail || "Invalid credentials ❌");
      }
    } catch (err) {
      console.error(err);
      alert("Backend error ❌");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-xl shadow-lg w-80">

        <h2 className="text-xl mb-4 text-center font-bold">
          SuperAdmin Login
        </h2>

        <input
          placeholder="Username"
          onChange={(e) => setUsername(e.target.value)}
          className="block mb-2 p-2 border w-full"
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          className="block mb-4 p-2 border w-full"
        />

        <button
          onClick={handleLogin}
          className="bg-purple-500 text-white p-2 w-full rounded"
        >
          Login
        </button>

        {/* SWITCH TO SIGNUP */}
        <p className="mt-4 text-sm text-center">
          Don’t have an account?{" "}
          <span
            onClick={() => setShowSignup(true)}
            className="text-blue-600 cursor-pointer underline"
          >
            Signup here
          </span>
        </p>

      </div>
    </div>
  );
}