import { useState } from "react";

function App() {
  const [inputMode, setInputMode] = useState("topic");
  const [topic, setTopic] = useState("");
  const [content, setContent] = useState("");
  const [pdfFile, setPdfFile] = useState(null);
  const [difficulty, setDifficulty] = useState("medium");
  const [questionType, setQuestionType] = useState("descriptive");
  const [numQuestions, setNumQuestions] = useState(5);
  const [keywords, setKeywords] = useState("");
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const generateQuestions = async () => {
    setLoading(true);

    try {
      let response;

      if (inputMode === "pdf") {
        const formData = new FormData();
        formData.append("file", pdfFile);
        formData.append("num_questions", numQuestions);
        formData.append("difficulty", difficulty);
        formData.append("question_type", questionType);

        console.log("This is the question type", questionType)
        console.log("This is the PDF file ", pdfFile)
        response = await fetch(
          "http://127.0.0.1:8000/generate-questions-from-pdf",
          {
            method: "POST",
            body: formData,
          }
        );
      } else {
        console.log("This is the question type ",questionType)
        response = await fetch(
          "http://127.0.0.1:8000/generate-questions",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              topic: inputMode === "topic" ? topic : null,
              content: inputMode === "content" ? content : null,
              difficulty,
              question_type: questionType,
              num_questions: numQuestions,
              keywords: keywords
                ? keywords.split(",").map((k) => k.trim())
                : null,
            }),
          }
        );
      }

      const data = await response.json();
      setQuestions(data.questions);
    } catch (error) {
      console.error("Error:", error);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 to-purple-200 p-10">
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl shadow-2xl">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">
          Intelligent Question Generator
        </h1>

        {/* INPUT MODE TOGGLE */}
        <div className="mb-6">
          <label className="block mb-2 font-semibold text-gray-700">
            Input Mode
          </label>

          <div className="flex gap-3">
            {["topic", "content", "pdf"].map((mode) => (
              <button
                key={mode}
                onClick={() => setInputMode(mode)}
                className={`px-4 py-2 rounded-lg border transition-all duration-200 ${
                  inputMode === mode
                    ? "bg-indigo-600 text-white border-indigo-600 shadow-md"
                    : "bg-white text-gray-700 border-gray-300 hover:bg-gray-100"
                }`}
              >
                {mode.toUpperCase()}
              </button>
            ))}
          </div>
        </div>

        {/* TOPIC MODE */}
        {inputMode === "topic" && (
          <input
            type="text"
            placeholder="Enter topic"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="w-full p-3 border rounded-lg mb-4 focus:ring-2 focus:ring-indigo-400"
          />
        )}

        {/* CONTENT MODE */}
        {inputMode === "content" && (
          <textarea
            placeholder="Paste study material..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full p-3 border rounded-lg mb-4 h-40 focus:ring-2 focus:ring-indigo-400"
          />
        )}

        {/* PDF MODE */}
        {inputMode === "pdf" && (
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setPdfFile(e.target.files[0])}
            className="w-full p-3 border rounded-lg mb-4"
          />
        )}

        {/* DIFFICULTY */}
        <div className="mb-4">
          <label className="block mb-1 font-semibold">Difficulty</label>
          <div className="flex gap-2">
            {["easy", "medium", "hard"].map((level) => (
              <button
                key={level}
                onClick={() => setDifficulty(level)}
                className={`px-4 py-2 rounded-lg border ${
                  difficulty === level
                    ? "bg-purple-600 text-white border-purple-600"
                    : "bg-white text-gray-700 border-gray-300"
                }`}
              >
                {level.toUpperCase()}
              </button>
            ))}
          </div>
        </div>

        {/* QUESTION TYPE */}
        <div className="mb-4">
          <label className="block mb-1 font-semibold">Question Type</label>
          <div className="flex gap-2">
            {["descriptive", "mcq"].map((type) => (
              <button
                key={type}
                onClick={() => setQuestionType(type)}
                className={`px-4 py-2 rounded-lg border ${
                  questionType === type
                    ? "bg-indigo-600 text-white border-indigo-600"
                    : "bg-white text-gray-700 border-gray-300"
                }`}
              >
                {type.toUpperCase()}
              </button>
            ))}
          </div>
        </div>

        {/* NUMBER OF QUESTIONS */}
        <div className="mb-4">
          <label className="block mb-1 font-semibold">
            Number of Questions
          </label>
          <input
            type="number"
            value={numQuestions}
            onChange={(e) => setNumQuestions(Number(e.target.value))}
            className="w-full p-3 border rounded-lg"
          />
        </div>

        {/* KEYWORDS */}
        {inputMode !== "pdf" && (
          <input
            type="text"
            placeholder="Keywords (comma separated)"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            className="w-full p-3 border rounded-lg mb-4"
          />
        )}

        {/* GENERATE BUTTON */}
        <button
          onClick={generateQuestions}
          className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-xl shadow-lg hover:scale-105 transition-all duration-200"
        >
          Generate Questions
        </button>

        {loading && (
          <p className="mt-4 text-indigo-600 font-semibold text-center">
            Generating...
          </p>
        )}
      </div>

      {/* RESULTS */}
      <div className="max-w-3xl mx-auto mt-10">
        {questions.map((q, index) => (
          <div
            key={index}
            className="bg-white p-6 rounded-2xl shadow-md mb-4"
          >
            {questionType === "mcq" ? (
              <>
                <strong className="block mb-2">
                  Q{index + 1}. {q.question}
                </strong>
                {q.options?.map((opt, i) => (
                  <div key={i} className="ml-4">
                    {String.fromCharCode(65 + i)}. {opt}
                  </div>
                ))}
              </>
            ) : (
              <strong>
                Q{index + 1}. {q.question}
              </strong>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;