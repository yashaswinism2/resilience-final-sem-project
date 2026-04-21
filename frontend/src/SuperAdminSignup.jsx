import { useState } from "react";

const BASE_URL = "http://127.0.0.1:8000";

export default function SuperAdminSignup({ setIsLoggedIn, setUserRole }) {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    username: "",
    password: "",
    institute_name: "",
  });

  const handleSignup = async () => {
    try {
      const res = await fetch(`${BASE_URL}/auth/superadmin-signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (res.ok) {
        alert("SuperAdmin created successfully ✅");

        // ✅ AUTO LOGIN (IMPORTANT FIX)
        setIsLoggedIn(true);
        setUserRole("superadmin");
        localStorage.setItem("role", "superadmin");

      } else {
        alert(data.detail || "Error ❌");
      }
    } catch (error) {
      console.error("Signup error:", error);
      alert("Backend connection error ❌");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-xl shadow-lg w-96">

        <h2 className="text-2xl font-bold mb-6 text-center">
          SuperAdmin Signup
        </h2>

        {/* FIRST NAME */}
        <input
          type="text"
          placeholder="First Name"
          value={form.first_name}
          onChange={(e) =>
            setForm({ ...form, first_name: e.target.value })
          }
          className="w-full mb-3 p-2 border rounded"
        />

        {/* LAST NAME */}
        <input
          type="text"
          placeholder="Last Name"
          value={form.last_name}
          onChange={(e) =>
            setForm({ ...form, last_name: e.target.value })
          }
          className="w-full mb-3 p-2 border rounded"
        />

        {/* USERNAME */}
        <input
          type="text"
          placeholder="Username"
          value={form.username}
          onChange={(e) =>
            setForm({ ...form, username: e.target.value })
          }
          className="w-full mb-3 p-2 border rounded"
        />

        {/* PASSWORD */}
        <input
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={(e) =>
            setForm({ ...form, password: e.target.value })
          }
          className="w-full mb-3 p-2 border rounded"
        />

        {/* INSTITUTE NAME */}
        <input
          type="text"
          placeholder="Institute Name"
          value={form.institute_name}
          onChange={(e) =>
            setForm({ ...form, institute_name: e.target.value })
          }
          className="w-full mb-5 p-2 border rounded"
        />

        {/* BUTTON */}
        <button
          onClick={handleSignup}
          className="w-full bg-purple-500 text-white py-2 rounded hover:bg-purple-600"
        >
          Create SuperAdmin
        </button>
      </div>
    </div>
  );
}