import { HashRouter, Navigate, Route, Routes } from 'react-router'
import { ROUTES } from './common/routes'
import LongPressCorner from './components/LongPressCorner'
import AiDetectionPage from './pages/AiDetectionPage'
import SettingsPage from './pages/SettingsPage'
import TutorialPage from './pages/TutorialPage'

function App(): React.JSX.Element {
  return (
    <HashRouter>
      <Routes>
        <Route path={ROUTES.tutorial} element={<TutorialPage />} />
        <Route path={ROUTES.detection} element={<AiDetectionPage />} />
        <Route path={ROUTES.settings} element={<SettingsPage />} />
        <Route path="*" element={<Navigate to={ROUTES.tutorial} replace />} />
      </Routes>
      <LongPressCorner />
    </HashRouter>
  )
}

export default App
