import LiveView from '../components/LiveView'

// Scan countdown and result overlay come with the scan messages (HAN-13); idle return with HAN-11.
export default function AiDetectionPage(): React.JSX.Element {
  return (
    <main className="h-full w-full">
      <LiveView />
    </main>
  )
}
