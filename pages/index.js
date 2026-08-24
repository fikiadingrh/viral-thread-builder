import { useState } from 'react'

export default function Home() {
  const [topic, setTopic] = useState('')
  const [template, setTemplate] = useState('listicle')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [copied, setCopied] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    
    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, template }),
      })
      
      const data = await res.json()
      
      if (!res.ok) {
        throw new Error(data.error || 'Request failed')
      }
      
      setResult(data.data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    if (result && result.thread) {
      navigator.clipboard.writeText(result.thread.join('\n\n'))
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-indigo-50">
      <div className="max-w-3xl mx-auto py-12 px-4">
        
        {/* HEADER */}
        <div className="text-center mb-10">
          <div className="text-6xl mb-4">🔥</div>
          <h1 className="text-4xl sm:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-indigo-600 mb-3">
            Viral Thread Builder
          </h1>
          <p className="text-gray-600 text-base sm:text-lg">
            Buat konten viral siap posting di Threads dalam hitungan detik
          </p>
        </div>

        {/* FORM CARD */}
        <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8 mb-8 border border-purple-100">
          <form onSubmit={handleSubmit}>
            <div className="mb-5">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                ✨ Topik / Niche
              </label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Contoh: skincare under 100k"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition"
                required
              />
            </div>

            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                🎯 Template
              </label>
              <select
                value={template}
                onChange={(e) => setTemplate(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none"
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
                  ? 'bg-purple-300 cursor-not-allowed text-white' 
                  : 'bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white shadow-lg'
              }`}
            >
              {loading ? 'Generating...' : '✨ Generate Viral Thread'}
            </button>
          </form>
        </div>

        {/* ERROR */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-8">
            ⚠️ {error}
          </div>
        )}

        {/* RESULT */}
        {result && (
          <div className="space-y-6">
            
            {/* SCORE CARD */}
            <div className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-6 rounded-xl shadow-lg">
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-purple-100 text-sm">Score</p>
                  <p className="text-4xl font-bold">{result.analysis.score}/100</p>
                </div>
                <div className="text-right">
                  <p className="text-purple-100 text-sm">Status</p>
                  <p className="text-xl font-semibold">
                    {result.analysis.score >= 80 ? '✅ Ready' : result.analysis.score >= 60 ? '⚠️ OK' : '🔧 Fix'}
                  </p>
                </div>
              </div>
            </div>

            {/* THREAD PREVIEW */}
            <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-100">
              <div className="bg-gradient-to-r from-purple-50 to-indigo-50 px-6 py-4 border-b flex justify-between items-center">
                <h3 className="font-bold text-gray-800">🧵 Preview Thread</h3>
                <button
                  onClick={handleCopy}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm"
                >
                  {copied ? '✓ Copied!' : '📋 Copy'}
                </button>
              </div>
              
              <div className="p-6 space-y-4">
                {result.thread.map((post, idx) => (
                  <div key={idx} className="pl-8 border-l-2 border-purple-300 pb-4">
                    <span className="absolute left-0 text-purple-600 font-bold">
                      {idx + 1}
                    </span>
                    <p className="text-gray-800 whitespace-pre-wrap">
                      {post}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* HOOKS */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="font-bold text-gray-800 mb-4">🪝 Hook Variants</h3>
              <div className="space-y-2">
                {result.hooks.map((hook, idx) => (
                  <div key={idx} className="bg-purple-50 border border-purple-100 rounded-lg p-3">
                    <p className="text-gray-700 text-sm">{hook}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* TIPS */}
            {result.analysis.suggestions.length > 0 && (
              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-xl">
                <h3 className="font-bold text-yellow-800 mb-3">💡 Tips</h3>
                <ul className="space-y-2">
                  {result.analysis.suggestions.map((s, idx) => (
                    <li key={idx} className="text-yellow-700 text-sm">• {s}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* TIMES */}
            <div className="bg-blue-50 border-l-4 border-blue-400 p-6 rounded-xl">
              <h3 className="font-bold text-blue-800 mb-3">⏰ Best Times</h3>
              <div className="flex flex-wrap gap-3">
                {result.optimal_times.map((t, idx) => (
                  <span key={idx} className="bg-white px-3 py-2 rounded-full text-blue-600 text-sm font-medium">
                    {t}
                  </span>
                ))}
              </div>
            </div>

          </div>
        )}

        {/* FOOTER */}
        <footer className="mt-12 text-center text-gray-400 text-sm">
          <p>Made with ❤️ for Viral Content Creators</p>
          <p className="mt-1">Powered by Next.js + Python on Vercel</p>
        </footer>

      </div>
    </div>
  )
}
