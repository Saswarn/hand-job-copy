import { useNavigate } from 'react-router'
import { ROUTES } from '../common/routes'

// ponytail: placeholder until the tutorial video lands (HAN-11)
export default function TutorialPage(): React.JSX.Element {
  const navigate = useNavigate()

  return (
    <main
      className="flex h-full w-full flex-col items-center justify-center gap-6 bg-black text-white"
      onClick={() => navigate(ROUTES.detection)}
    >
      <h1 className="text-5xl font-bold">วิดีโอสอนใช้งาน</h1>
      <p className="text-4xl">แตะที่ใดก็ได้เพื่อเริ่ม</p>
    </main>
  )
}
