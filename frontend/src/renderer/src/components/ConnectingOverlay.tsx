export default function ConnectingOverlay(): React.JSX.Element {
  return (
    <div className="absolute inset-0 flex items-center justify-center bg-black/80">
      <p className="text-5xl font-bold text-white">กำลังเชื่อมต่อ…</p>
    </div>
  )
}
