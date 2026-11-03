import { useNavigate } from 'react-router'
import { ROUTES } from '../common/routes'

// ponytail: placeholder; Debug camera / UV / scan params land in later tickets
export default function SettingsPage(): React.JSX.Element {
  const navigate = useNavigate()

  return (
    <main className="flex h-full w-full flex-col items-center justify-center gap-8 bg-black text-white">
      <h1 className="text-5xl font-bold">Settings / Debug</h1>
      <button
        type="button"
        className="rounded-2xl border-2 border-white px-10 py-5 text-4xl"
        onClick={() => navigate(ROUTES.tutorial)}
      >
        กลับ
      </button>
    </main>
  )
}
