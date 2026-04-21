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
        console.log("PAPERS DATA:", data); // 🔍 debug
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

  // ---------------- APPROVE / REJECT ----------------
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
        alert("Failed to update status ❌");
      }
    } catch (err) {
      console.error(err);
      alert("Server error ❌");
    }
  };

  // ---------------- SAFE PARSE ----------------
  const parseQuestions = (content) => {
    try {
      // Case 1: already array
      if (Array.isArray(content)) return content;

      // Case 2: JSON string
      if (typeof content === "string") return JSON.parse(content);

      return [];
    } catch (e) {
      console.error("Parse error:", e);
      return [];
    }
  };

  if (loading) return <p className="p-10">Loading...</p>;

  return (
    <div className="min-h-screen bg-gray-100 p-6">

      {/* HEADER */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">COE Dashboard</h1>

        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>

      {/* NO DATA */}
      {papers.length === 0 ? (
        <p>No question papers submitted yet</p>
      ) : (
        papers.map((paper) => {
          const questions = parseQuestions(paper.content);

          return (
            <div
              key={paper.id}
              className="bg-white p-5 mb-5 rounded-xl shadow"
            >
              {/* STATUS */}
              <p className="mb-2">
                <strong>Status:</strong>{" "}
                <span
                  className={
                    paper.status === "approved"
                      ? "text-green-600 font-semibold"
                      : paper.status === "rejected"
                      ? "text-red-600 font-semibold"
                      : "text-yellow-600 font-semibold"
                  }
                >
                  {paper.status}
                </span>
              </p>

              {/* FACULTY */}
              <p className="mb-3">
                <strong>Faculty ID:</strong> {paper.faculty_id}
              </p>

              {/* QUESTIONS */}
              <div className="bg-gray-100 p-3 rounded mb-3">
                <h3 className="font-semibold mb-2">Questions:</h3>

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
                    className="bg-green-600 text-white px-4 py-2 rounded"
                  >
                    Approve
                  </button>

                  <button
                    onClick={() => updateStatus(paper.id, "rejected")}
                    className="bg-red-600 text-white px-4 py-2 rounded"
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