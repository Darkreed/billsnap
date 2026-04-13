const BASE_URL = "http://localhost:8000/api/v1"

export interface Bill {
  id: string
  biller: string
  amount: number
  currency: string | null
  status: "unpaid" | "paid" | "overdue"
  due_date: string | null
  billing_month: string | null
  recipient: string | null
  language: string | null
  created_at: string
}

export async function fetchBills(): Promise<Bill[]> {
  const response = await fetch(`${BASE_URL}/bills/`)
  const data = await response.json()
  return data
}

export async function uploadBill(file: File): Promise<Bill> {
  const form = new FormData()
  form.append("file", file)
  const response = await fetch(`${BASE_URL}/bills/upload`, {
    method: "POST",
    body: form
  })
  return response.json()
}
