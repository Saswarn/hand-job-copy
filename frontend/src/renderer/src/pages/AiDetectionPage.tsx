import LiveView from '../components/LiveView'

/**
 * Live view full screen; the scan UI sits on top of it on this same page (no separate result page).
 * TODO(frontend): on enter send { type: 'scan_start' }, show countdown from useBackend().scan.remaining_s,
 * then the result ("สะอาด" text-clean / "ยังมีคราบ" text-dirt) from scan.result. Idle 60 s -> back to tutorial.
 */
export default function AiDetectionPage(): React.JSX.Element {
  return (
    <main className="relative h-full w-full">
      <LiveView />
      <section
        aria-label="สถานะการสแกน"
        className="pointer-events-none absolute inset-x-0 bottom-0 flex justify-center p-8"
      >
        {/* scan countdown / result goes here */}
      </section>
    </main>
  )
}
