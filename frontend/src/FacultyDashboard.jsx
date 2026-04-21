import { useState, useEffect } from "react";

const BASE_URL = "http://127.0.0.1:8000";

export default function FacultyDashboard({ handleLogout }) {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [notifications, setNotifications] = useState([]);

  const [inputMode, setInputMode] = useState("topic");
  const [topic, setTopic] = useState("");
  const [content, setContent] = useState("");

  // ---------------- FETCH NOTIFICATIONS ----------------
  useEffect(() => {
    const facultyId = localStorage.getItem("user_id");

    fetch(`${BASE_URL}/notifications/${facultyId}`)
      .then((res) => res.json())
      .then((data) => setNotifications(data))
      .catch((err) => console.error(err));
  }, []);

  // ---------------- GENERATE QUESTIONS ----------------
  const generateQuestions = async () => {
    if (!topic && !content) {
      alert("Please enter topic or content ❗");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${BASE_URL}/generate-questions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          topic,
          content,
          num_questions: 5,
          difficulty: "medium",
          question_type: "descriptive",
          include_images: false,
        }),
      });

      const data = await res.json();

      if (res.ok) {
        setQuestions(data.questions || []);
      } else {
        alert(data.detail || "Failed to generate ❌");
      }
    } catch (err) {
      console.error(err);
      alert("Server error ❌");
    }

    setLoading(false);
  };

  // ---------------- SEND TO COE ----------------
  const sendToCOE = async () => {
    if (questions.length === 0) {
      alert("No questions to send ❗");
      return;
    }

    try {
      const res = await fetch(`${BASE_URL}/papers/submit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          faculty_id: Number(localStorage.getItem("user_id")),
          institute_id: Number(localStorage.getItem("institute_id")),
          questions: questions,
        }),
      });

      if (res.ok) {
        alert("Paper submitted to COE ✅");
        setQuestions([]);
        setTopic("");
        setContent("");
      } else {
        alert("Failed to send ❌");
      }
    } catch (err) {
      console.error(err);
      alert("Server error ❌");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 to-purple-200 p-6">

      {/* HEADER */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">
          Faculty Dashboard
        </h1>

        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>

      {/* 🔔 NOTIFICATIONS */}
      {notifications.length > 0 && (
        <div className="max-w-3xl mx-auto mb-4">
          {notifications.map((n) => (
            <div
              key={n.id}
              className="bg-yellow-100 border-l-4 border-yellow-500 p-3 mb-2 rounded shadow"
            >
              🔔 {n.message}
            </div>
          ))}
        </div>
      )}

      {/* MAIN CARD */}
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-2xl shadow-xl">

        {/* INPUT MODE */}
        <div className="flex justify-center gap-4 mb-6">
          {["topic", "content"].map((mode) => (
            <button
              key={mode}
              onClick={() => setInputMode(mode)}
              className={`px-5 py-2 rounded-lg font-medium transition ${
                inputMode === mode
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 hover:bg-gray-300"
              }`}
            >
              {mode.toUpperCase()}
            </button>
          ))}
        </div>

        {/* INPUT */}
        {inputMode === "topic" ? (
          <input
            placeholder="Enter topic (e.g., Machine Learning)"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="w-full p-3 border rounded-lg mb-4 focus:ring-2 focus:ring-blue-400"
          />
        ) : (
          <textarea
            placeholder="Paste syllabus or content here..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={5}
            className="w-full p-3 border rounded-lg mb-4 focus:ring-2 focus:ring-blue-400"
          />
        )}

        {/* GENERATE */}
        <button
          onClick={generateQuestions}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg mb-4 transition"
        >
          Generate Questions
        </button>

        {/* LOADING */}
        {loading && (
          <p className="text-center text-gray-500">
            Generating questions...
          </p>
        )}

        {/* QUESTIONS */}
        {questions.length > 0 && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-700">
              Generated Questions
            </h3>

            {questions.map((q, i) => (
              <div key={i} className="mb-3 p-3 bg-gray-100 rounded-lg">
                {i + 1}. {q.question}
              </div>
            ))}

            <button
              onClick={sendToCOE}
              className="w-full mt-4 bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg transition"
            >
              Send to COE
            </button>
          </div>
        )}
      </div>
    </div>
  );
}