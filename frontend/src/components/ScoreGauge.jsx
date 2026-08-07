export default function ScoreGauge({ score }) {
  const color = score >= 75 ? 'bg-green-500' : score >= 50 ? 'bg-yellow-500' : 'bg-red-500'
  return (
    <div className="bg-white rounded-xl shadow p-4">
      <p className="font-semibold">ATS Score</p>
      <div className="w-full bg-slate-200 h-4 rounded mt-3 overflow-hidden">
        <div className={`${color} h-4`} style={{ width: `${score}%` }} />
      </div>
      <p className="mt-2 text-sm">{score}/100</p>
    </div>
  )
}
