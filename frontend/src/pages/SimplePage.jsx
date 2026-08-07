export default function SimplePage({ title, description }) {
  return (
    <section className="bg-white p-6 rounded-xl shadow">
      <h1 className="text-2xl font-bold mb-2">{title}</h1>
      <p className="text-slate-700">{description}</p>
    </section>
  )
}
