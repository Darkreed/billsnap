import { useState } from "react"
import { markAsPaid, type Bill } from "../api"

type SortKey = "biller" | "amount" | "due_date" | "status"

export default function BillList({ bills, loading, onPaid }: {
  bills: Bill[]
  loading: boolean
  onPaid: (bill: Bill) => void
}) {
  const [filter, setFilter] = useState("")
  const [sortKey, setSortKey] = useState<SortKey>("due_date")
  const [sortAsc, setSortAsc] = useState(true)

  if (loading) return <p className="text-gray-500">Loading...</p>
  if (bills.length === 0) return <p className="text-gray-500">No bills yet.</p>

  function handleSort(key: SortKey) {
    if (key === sortKey) setSortAsc(prev => !prev)
    else { setSortKey(key); setSortAsc(true) }
  }

  const displayed = bills
    .filter(b => b.biller.toLowerCase().includes(filter.toLowerCase()))
    .sort((a, b) => {
      const av = a[sortKey] ?? ""
      const bv = b[sortKey] ?? ""
      return sortAsc ? (av > bv ? 1 : -1) : (av < bv ? 1 : -1)
    })

  async function handlePaid(bill: Bill) {
    if (bill.status === "paid") return
    const updated = await markAsPaid(bill.id)
    onPaid(updated)
  }

  function arrow(key: SortKey) {
    if (sortKey !== key) return " ↕"
    return sortAsc ? " ↑" : " ↓"
  }

  return (
    <div>
      <input
        type="text"
        placeholder="Filter by biller..."
        value={filter}
        onChange={e => setFilter(e.target.value)}
        className="mb-4 w-full max-w-sm px-3 py-2 border border-gray-300 rounded-lg text-sm"
      />
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="border-b border-gray-200">
            <th className="py-2 pr-4 font-semibold text-gray-600">Paid</th>
            {(["biller", "amount", "due_date", "status"] as SortKey[]).map(key => (
              <th key={key} onClick={() => handleSort(key)}
                className="py-2 pr-4 font-semibold text-gray-600 cursor-pointer select-none hover:text-gray-900">
                {key.replace("_", " ")}{arrow(key)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {displayed.map(bill => (
            <tr key={bill.id} className="border-b border-gray-100">
              <td className="py-2 pr-4">
                <input type="checkbox" checked={bill.status === "paid"}
                  onChange={() => handlePaid(bill)} className="w-4 h-4 cursor-pointer" />
              </td>
              <td className="py-2 pr-4">{bill.biller}</td>
              <td className="py-2 pr-4">{bill.amount} {bill.currency}</td>
              <td className="py-2 pr-4">{bill.due_date ?? "—"}</td>
              <td className="py-2 pr-4">{bill.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
