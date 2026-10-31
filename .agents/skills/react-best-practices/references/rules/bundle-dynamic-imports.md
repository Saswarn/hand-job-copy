---
title: Lazy-Load Heavy Components
impact: CRITICAL
impactDescription: smaller initial chunk, faster app start (FE-6)
tags: bundle, dynamic-import, code-splitting, react-lazy
---

## Lazy-Load Heavy Components

Use `React.lazy` + `Suspense` to load large components that are not needed on the first screen (e.g. the Settings / Debug page).

**Incorrect (Debug page bundles with the main chunk):**

```tsx
import { DebugPage } from './pages/DebugPage'

function App({ page }: { page: Page }) {
  return page === 'debug' ? <DebugPage /> : <VideoPage />
}
```

**Correct (Debug page loads on demand):**

```tsx
import { lazy, Suspense } from 'react'

const DebugPage = lazy(() => import('./pages/DebugPage').then(m => ({ default: m.DebugPage })))

function App({ page }: { page: Page }) {
  return (
    <Suspense fallback={null}>
      {page === 'debug' ? <DebugPage /> : <VideoPage />}
    </Suspense>
  )
}
```
