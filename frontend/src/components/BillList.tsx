import { type Bill } from "../api"

export default function BillList({ bills, loading }: { bills: Bill[], loading: boolean }) {
  if (loading) return <p className="text-gray-500">Loading...</p>
  if (bills.length === 0) return <p className="text-gray-500">No bills yet.</p>

  return (
    <table className="w-full text-left border-collapse">
      <thead>
        <tr className="border-b border-gray-200">
          <th className="py-2 pr-4 font-semibold text-gray-600">Biller</th>
          <th className="py-2 pr-4 font-semibold text-gray-600">Amount</th>
          <th className="py-2 pr-4 font-semibold text-gray-600">Due Date</th>
          <th className="py-2 pr-4 font-semibold text-gray-600">Status</th>
        </tr>
      </thead>
      <tbody>
        {bills.map(bill => (
          <tr key={bill.id} className="border-b border-gray-100">
            <td className="py-2 pr-4">{bill.biller}</td>
            <td className="py-2 pr-4">{bill.amount} {bill.currency}</td>
            <td className="py-2 pr-4">{bill.due_date ?? "—"}</td>
            <td className="py-2 pr-4">{bill.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
