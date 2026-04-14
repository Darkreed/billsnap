import { useRef, useState } from "react"
import { uploadBill, type Bill } from "../api"

export default function UploadForm({ onUploaded }: { onUploaded: (bill: Bill) => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    setError(null)
    try {
      const bill = await uploadBill(file)
      onUploaded(bill)
      setFile(null)
      if (inputRef.current) inputRef.current.value = ""
    } catch {
      setError("Upload failed. Make sure the server is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 mb-8 w-full max-w-md">
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={e => setFile(e.target.files?.[0] ?? null)}
      />
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        className="w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-blue-400 hover:text-blue-500 transition-colors"
      >
        {file ? file.name : "Tap to select a bill image"}
      </button>
      <button
        type="submit"
        disabled={!file || loading}
        className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg font-medium disabled:opacity-40"
      >
        {loading ? "Uploading..." : "Upload Bill"}
      </button>
      {error && <p className="text-red-500 text-sm">{error}</p>}
    </form>
  )
}
