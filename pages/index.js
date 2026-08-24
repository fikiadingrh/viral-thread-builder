import { useState } from "react";

export default function Home() {
  const [topic, setTopic] = useState("");
  const [template, setTemplate] = useState("listicle");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    setCopied(false);

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, template }),
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.error || "Terjadi kesalahan");

      setResult(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (result && result.thread) {
      navigator.clipboard.writeText(result.thread.join("\n\n"));
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-indigo-50">
      <div className="max-w-3xl mx-auto py-12 px-4">
        {/* ===== HEADER ===== */}
        <div className="text-center mb-10">
          <div className="inline-block text-6xl mb-4">🔥</div>
          <h1 className="text-4xl sm:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-indigo-600 mb-3">
            Viral Thread Builder
          </h1>
          <p className="text-gray-600 text-base sm:text-lg max-w-xl mx-auto">
            Buat konten viral siap posting di Threads dalam hitungan detik.
            Optimasi engagement maksimal.
          </p>
        </div>

        {/* ===== INPUT FORM ===== */}
        <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8 mb-8 border border-purple-100">
          <form onSubmit={handleSubmit}>
            <div className="mb-5">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                📌 Topik / Niche
              </label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Contoh: skincare under 100k"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition"
                required
                maxLength={100}
              />
            </div>

            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                🎯 Template
              </label>
              <select
                value={template}
                onChange={(e) => setTemplate(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition"
              >
                <option value="listicle">📋 Listicle (Review Produk)</option>
                <option value="how_to">📖 How-To Tutorial</option>
                <option value="hot_take">🔥 Hot Take / Opini</option>
                <option value="personal_story">💭 Personal Story</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className={`w-full py-4 rounded-xl font-bold text-lg transition-all ${
                loading
                  ? "bg-purple-300 cursor-not-allowed text-white"
                  : "bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white shadow-lg hover:shadow-xl"
              }`}
            >
              {loading ? "Generating..." : "✨ Generate Viral Thread"}
            </button>
          </form>
        </div>

        {/* ===== ERROR ===== */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-8">
            ⚠️ {error}
          </div>
        )}

        {/* ===== RESULTS ===== */}
        {result && (
          <div className="space-y-6">
            {/* Score Card */}
            <div className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-6 rounded-xl shadow-lg">
              <div className="flex flex-wrap justify-between items-center gap-4">
                <div>
                  <p className="text-purple-100 text-sm">Optimization Score</p>
                  <p className="text-4xl font-bold">{result.analysis.score}/100</p>
                </div>
                <div className="text-right">
                  <p className="text-purple-100 text-sm">Status</p>
                  <p className="text-lg font-semibold">
                    {result.analysis.score >= 80
                      ? "✅ Ready to Post"
                      : result.analysis.score >= 60
                      ? "⚠️ Needs Tweaks"
                      : "🔧 Needs Work"}
                  </p>
                </div>
                <div>
                  <p className="text-purple-100 text-sm">Total Posts</p>
                  <p className="text-2xl font-semibold">{result.analysis.total_posts}</p>
                </div>
              </div>
            </div>

            {/* Thread Preview */}
            <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-100">
              <div className="bg-gradient-to-r from-purple-50 to-indigo-50 px-6 py-4 border-b border-purple-100 flex justify-between items-center">
                <h3 className="font-bold text-gray-800 text-lg">🧵 Preview Thread</h3>
                <button
                  onClick={handleCopy}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition text-sm font-medium"
                >
                  {copied ? "✓ Copied!" : "📋 Copy All"}
                </button>
              </div>

              <div className="p-6 space-y-4">
                {result.thread.map((post, idx) => (
                  <div
                    key={idx}
                    className="relative pl-8 border-l-2 border-purple-300 pb-4 last:border-l-0"
                  >
                    <span className="absolute -left-3 top-0 w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-xs font-bold">
                      {idx + 1}
                    </span>
                    <p className="text-gray-800 whitespace-pre-wrap leading-relaxed">
                      {post}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Hook Variants */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
              <h3 className="font-bold text-gray-800 mb-4">🪝 Hook Variants (A/B Test)</h3>
              <div className="space-y-2">
                {result.hooks.map((hook, idx) => (
                  <div
                    key={idx}
                    className="bg-purple-50 border border-purple-100 rounded-lg p-3 flex items-start gap-3"
                  >
                    <span className="bg-purple-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold flex-shrink-0">
                      {idx + 1}
                    </span>
                    <p className="text-gray-700 text-sm">{hook}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Suggestions */}
            {result.analysis.suggestions.length > 0 && (
              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-xl">
                <h3 className="font-bold text-yellow-800 mb-3">
                  💡 Optimization Tips
                </h3>
                <ul className="space-y-2">
                  {result.analysis.suggestions.map((s, idx) => (
                    <li
                      key={idx}
                      className="text-yellow-700 text-sm flex items-start gap-2"
                    >
                      <span>•</span>
                      <span>{s}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Best Times */}
            <div className="bg-blue-50 border-l-4 border-blue-400 p-6 rounded-xl">
              <h3 className="font-bold text-blue-800 mb-3">
                ⏰ Best Posting Times (WIB)
              </h3>
              <div className="flex flex-wrap gap-3">
                {result.optimal_times.map((time, idx) => (
                  <span
                    key={idx}
                    className="bg-white px-4 py-2 rounded-full text-blue-600 text-sm font-medium border border-blue-200"
                  >
                    {time}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ===== FOOTER ===== */}
        <footer className="mt-16 text-center text-gray-400 text-sm pb-8">
          <p>Made with ❤️ for Viral Content Creators</p>
          <p className="mt-1">Powered by Next.js + Python on Vercel</p>
        </footer>
      </div>
    </div>
  );
}
