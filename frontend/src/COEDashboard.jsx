import { useEffect, useState } from "react";

const BASE_URL = "http://127.0.0.1:8000";

export default function COEDashboard({ handleLogout }) {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);

  const instituteId = localStorage.getItem("institute_id");

  // ---------------- FETCH PAPERS ----------------
  const fetchPapers = () => {
    setLoading(true);

    fetch(`${BASE_URL}/papers/institute/${instituteId}`)
      .then((res) => res.json())
      .then((data) => {
        setPapers(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchPapers();
  }, []);

  // ---------------- UPDATE STATUS ----------------
  const updateStatus = async (paperId, status) => {
    try {
      const res = await fetch(`${BASE_URL}/papers/${paperId}/status`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status }),
      });

      if (res.ok) {
        alert(`Paper ${status} ✅`);
        fetchPapers();
      } else {
        alert("Failed to update ❌");
      }
    } catch (err) {
      console.error(err);
      alert("Server error ❌");
    }
  };

  // ---------------- PARSE QUESTIONS ----------------
  const parseQuestions = (content) => {
    try {
      if (Array.isArray(content)) return content;
      if (typeof content === "string") return JSON.parse(content);
      return [];
    } catch {
      return [];
    }
  };

  // ---------------- STATUS COLOR ----------------
  const getStatusStyle = (status) => {
    if (status === "approved") return "bg-green-100 text-green-700";
    if (status === "rejected") return "bg-red-100 text-red-700";
    return "bg-yellow-100 text-yellow-700";
  };

  if (loading)
    return (
      <div className="p-10 text-center text-gray-600">
        Loading papers...
      </div>
    );

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 to-purple-200 p-6">

      {/* HEADER */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">
          COE Dashboard
        </h1>

        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>

      {/* NO DATA */}
      {papers.length === 0 ? (
        <p className="text-center text-gray-600">
          No question papers submitted yet
        </p>
      ) : (
        papers.map((paper) => {
          const questions = parseQuestions(paper.content);

          return (
            <div
              key={paper.id}
              className="bg-white p-6 mb-6 rounded-2xl shadow-lg"
            >
              {/* TOP BAR */}
              <div className="flex justify-between items-center mb-3">
                <span className="text-sm text-gray-500">
                  Paper ID: {paper.id}
                </span>

                <span
                  className={`px-3 py-1 text-sm rounded-full font-semibold ${getStatusStyle(
                    paper.status
                  )}`}
                >
                  {paper.status}
                </span>
              </div>

              {/* FACULTY */}
              <p className="mb-3 text-gray-700">
                <strong>Faculty ID:</strong> {paper.faculty_id}
              </p>

              {/* QUESTIONS */}
              <div className="bg-gray-100 p-4 rounded-lg mb-4 max-h-60 overflow-y-auto">
                <h3 className="font-semibold mb-2 text-gray-700">
                  Questions
                </h3>

                {questions.length === 0 ? (
                  <p className="text-sm text-gray-500">
                    No questions found ❌
                  </p>
                ) : (
                  questions.map((q, i) => (
                    <div key={i} className="mb-2">
                      {i + 1}. {q.question}
                    </div>
                  ))
                )}
              </div>

              {/* ACTION BUTTONS */}
              {paper.status === "pending" && (
                <div className="flex gap-3">
                  <button
                    onClick={() => updateStatus(paper.id, "approved")}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg transition"
                  >
                    Approve
                  </button>

                  <button
                    onClick={() => updateStatus(paper.id, "rejected")}
                    className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 rounded-lg transition"
                  >
                    Reject
                  </button>
                </div>
              )}
            </div>
          );
        })
      )}
    </div>
  );
}