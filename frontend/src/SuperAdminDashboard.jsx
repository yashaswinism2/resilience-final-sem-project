import { useEffect, useState } from "react";

const BASE_URL = "http://127.0.0.1:8000";

export default function SuperAdminDashboard() {
  const [institutes, setInstitutes] = useState([]);
  const [selectedInstitute, setSelectedInstitute] = useState(null);

  // ✅ Fetch institutes
  useEffect(() => {
    fetch(`${BASE_URL}/institutes`)
      .then((res) => res.json())
      .then((data) => setInstitutes(data));
  }, []);

  // ✅ Fetch institute details
  const handleClick = async (id) => {
    const res = await fetch(`${BASE_URL}/institutes/${id}`);
    const data = await res.json();
    setSelectedInstitute(data);
  };

  // ---------------- DETAILS VIEW ----------------
  if (selectedInstitute) {
    return (
      <div className="p-10">
        <button
          onClick={() => setSelectedInstitute(null)}
          className="mb-4 text-blue-600 underline"
        >
          ← Back
        </button>

        <h2 className="text-2xl font-bold mb-4">
          {selectedInstitute.name}
        </h2>

        <p><strong>ID:</strong> {selectedInstitute.id}</p>

        {/* Later we add COE / Faculty / Papers here */}
      </div>
    );
  }

  // ---------------- CARD VIEW ----------------
  return (
    <div className="p-10">
      <h2 className="text-2xl font-bold mb-6">Institutes</h2>

      <div className="grid grid-cols-3 gap-4">
        {institutes.map((inst) => (
          <div
            key={inst.id}
            onClick={() => handleClick(inst.id)}
            className="bg-white p-6 rounded-xl shadow cursor-pointer hover:scale-105 transition"
          >
            <h3 className="text-lg font-semibold">
              {inst.name}
            </h3>
          </div>
        ))}
      </div>
    </div>
  );
}