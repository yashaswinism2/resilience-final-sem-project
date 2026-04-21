export default function Landing({ setSelectedRole }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-300 via-purple-200 to-pink-200 flex items-center justify-center px-4">

      <div className="bg-white/80 backdrop-blur-xl shadow-2xl rounded-3xl p-10 w-full max-w-4xl text-center">

        <h1 className="text-4xl font-extrabold text-gray-800 mb-2">
          Intelligent Question Paper Generator
        </h1>

        <p className="text-gray-600 mb-10 text-lg">
          Select your role to continue
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          {/* Super Admin */}
          <div
            onClick={() => setSelectedRole("superadmin")}
            className="group cursor-pointer p-6 rounded-2xl bg-white shadow-md hover:shadow-2xl hover:scale-105 transition-all duration-300 border border-transparent hover:border-purple-400"
          >
            <div className="text-5xl mb-3 group-hover:scale-110 transition">👑</div>
            <h2 className="font-semibold text-lg text-purple-700">
              Super Admin
            </h2>
            <p className="text-sm text-gray-500 mt-2">
              Manage system & users
            </p>
          </div>

          {/* COE */}
          <div
            onClick={() => setSelectedRole("coe")}
            className="group cursor-pointer p-6 rounded-2xl bg-white shadow-md hover:shadow-2xl hover:scale-105 transition-all duration-300 border border-transparent hover:border-blue-400"
          >
            <div className="text-5xl mb-3 group-hover:scale-110 transition">🏫</div>
            <h2 className="font-semibold text-lg text-blue-700">
              COE
            </h2>
            <p className="text-sm text-gray-500 mt-2">
              Review & approve question papers
            </p>
          </div>

          {/* Faculty */}
          <div
            onClick={() => setSelectedRole("faculty")}
            className="group cursor-pointer p-6 rounded-2xl bg-white shadow-md hover:shadow-2xl hover:scale-105 transition-all duration-300 border border-transparent hover:border-green-400"
          >
            <div className="text-5xl mb-3 group-hover:scale-110 transition">👩‍🏫</div>
            <h2 className="font-semibold text-lg text-green-700">
              Faculty
            </h2>
            <p className="text-sm text-gray-500 mt-2">
              Generate & submit question papers
            </p>
          </div>

        </div>

        <p className="text-xs text-gray-500 mt-10">
          Powered by AI • NLP • Machine Learning
        </p>

      </div>
    </div>
  );
}