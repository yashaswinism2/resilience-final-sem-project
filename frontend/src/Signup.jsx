import { useState } from "react";

const BASE_URL = "http://127.0.0.1:8000";

export default function Signup({ setShowSignup }) {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    username: "",
    password: "",
    role: "faculty",
    institute_id: "",
  });

  const handleSignup = async () => {
    try {
      const res = await fetch(`${BASE_URL}/auth/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...form,
          institute_id:
            form.role === "superadmin"
              ? null
              : Number(form.institute_id),
        }),
      });

      const data = await res.json();

      if (res.ok) {
        alert("Signup successful ✅");

        // ✅ go back to login
        setShowSignup(false);
      } else {
        alert(data.detail || "Signup failed ❌");
      }
    } catch (err) {
      console.error("Signup error:", err);
      alert("Backend connection error ❌");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-xl shadow-lg w-80">
        <h2 className="text-xl mb-4 text-center font-bold">
          Signup
        </h2>

        {/* FIRST NAME */}
        <input
          type="text"
          placeholder="First Name"
          value={form.first_name}
          onChange={(e) =>
            setForm({ ...form, first_name: e.target.value })
          }
          className="block mb-2 p-2 border w-full"
        />

        {/* LAST NAME */}
        <input
          type="text"
          placeholder="Last Name"
          value={form.last_name}
          onChange={(e) =>
            setForm({ ...form, last_name: e.target.value })
          }
          className="block mb-2 p-2 border w-full"
        />

        {/* USERNAME */}
        <input
          type="text"
          placeholder="Username"
          value={form.username}
          onChange={(e) =>
            setForm({ ...form, username: e.target.value })
          }
          className="block mb-2 p-2 border w-full"
        />

        {/* PASSWORD */}
        <input
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={(e) =>
            setForm({ ...form, password: e.target.value })
          }
          className="block mb-2 p-2 border w-full"
        />

        {/* ROLE */}
        <select
          value={form.role}
          onChange={(e) =>
            setForm({ ...form, role: e.target.value })
          }
          className="block mb-2 p-2 border w-full"
        >
          <option value="coe">COE</option>
          <option value="faculty">Faculty</option>
        </select>

        {/* INSTITUTE ID */}
        <input
          type="number"
          placeholder="Institute ID"
          value={form.institute_id}
          onChange={(e) =>
            setForm({ ...form, institute_id: e.target.value })
          }
          className="block mb-4 p-2 border w-full"
        />

        {/* BUTTON */}
        <button
          onClick={handleSignup}
          className="bg-green-500 text-white p-2 w-full rounded"
        >
          Signup
        </button>

        {/* BACK TO LOGIN */}
        <p className="mt-4 text-sm text-center">
          Already have an account?{" "}
          <span
            onClick={() => setShowSignup(false)}
            className="text-blue-600 cursor-pointer underline"
          >
            Login
          </span>
        </p>
      </div>
    </div>
  );
}