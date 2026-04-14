import { useState, useEffect } from "react"
import BillList from "./components/BillList"
import UploadForm from "./components/UploadForm"
import { fetchBills, type Bill } from "./api"

function App() {
  const [bills, setBills] = useState<Bill[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchBills()
      .then(data => setBills(data))
      .finally(() => setLoading(false))
  }, [])

  function handleUploaded(bill: Bill) {
    setBills(prev => [bill, ...prev])
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">BillSnap</h1>
      <UploadForm onUploaded={handleUploaded} />
      <BillList bills={bills} loading={loading} />
    </div>
  )
}

export default App
