import { useNavigate } from 'react-router'
import tutorialVideo from '../assets/tutorial-placeholder.mp4'
import { ROUTES } from '../common/routes'

export default function TutorialPage(): React.JSX.Element {
  const navigate = useNavigate()

  return (
    <main className="relative h-full w-full bg-surface">
      <video
        className="h-full w-full object-contain"
        src={tutorialVideo}
        autoPlay
        loop
        muted
        playsInline
      />
      <button
        type="button"
        className="absolute inset-0 flex w-full items-end justify-center p-8 focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-ink"
        onClick={() => navigate(ROUTES.detection)}
      >
        <span className="bg-surface px-6 py-2 text-body text-ink">แตะที่ใดก็ได้เพื่อเริ่ม</span>
      </button>
    </main>
  )
}
