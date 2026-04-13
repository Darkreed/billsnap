import { useState } from "react"
import { uploadBill, type Bill } from "../api"

export default function UploadForm({ onUploaded }: { onUploaded: (bill: Bill) => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    setError(null)
    try {
      const bill = await uploadBill(file)
      onUploaded(bill)
      setFile(null)
    } catch {
      setError("Upload failed. Make sure the server is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-4 items-center mb-8">
      <input
        type="file"
        accept="image/*"
        onChange={e => setFile(e.target.files?.[0] ?? null)}
        className="text-sm text-gray-600"
      />
      <button
        type="submit"
        disabled={!file || loading}
        className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
      >
        {loading ? "Uploading..." : "Upload Bill"}
      </button>
      {error && <p className="text-red-500 text-sm">{error}</p>}
    </form>
  )
}
