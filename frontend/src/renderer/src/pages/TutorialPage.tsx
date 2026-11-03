import { useNavigate } from 'react-router'
import { ROUTES } from '../common/routes'

// TODO(frontend): replace the text with <video autoPlay loop muted> of one local .mp4 (path in one place).
export default function TutorialPage(): React.JSX.Element {
  const navigate = useNavigate()

  return (
    <main
      className="flex h-full w-full flex-col items-center justify-center gap-6"
      onClick={() => navigate(ROUTES.detection)}
    >
      <h1 className="text-title font-bold">วิดีโอสอนใช้งาน</h1>
      <p className="text-body text-muted">แตะที่ใดก็ได้เพื่อเริ่ม</p>
    </main>
  )
}
