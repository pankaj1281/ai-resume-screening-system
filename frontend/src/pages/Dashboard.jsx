import ScoreGauge from '../components/ScoreGauge'
import SkillPieChart from '../components/SkillPieChart'

export default function Dashboard() {
  return (
    <div className="grid md:grid-cols-2 gap-4">
      <ScoreGauge score={78} />
      <SkillPieChart matched={18} missing={6} />
      <div className="bg-white rounded-xl shadow p-4">
        <h2 className="font-semibold">Experience Timeline</h2>
        <p className="text-sm text-slate-600 mt-2">Visualized from parsed resume data in production API response.</p>
      </div>
      <div className="bg-white rounded-xl shadow p-4">
        <h2 className="font-semibold">Education Timeline</h2>
        <p className="text-sm text-slate-600 mt-2">Visualized from parsed education milestones.</p>
      </div>
    </div>
  )
}
