import { Pie } from 'react-chartjs-2'
import { ArcElement, Chart as ChartJS, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

export default function SkillPieChart({ matched = 0, missing = 0 }) {
  return (
    <div className="bg-white rounded-xl shadow p-4">
      <p className="font-semibold mb-3">Skill Match</p>
      <Pie
        data={{
          labels: ['Matched', 'Missing'],
          datasets: [{ data: [matched, missing], backgroundColor: ['#10b981', '#ef4444'] }],
        }}
      />
    </div>
  )
}
