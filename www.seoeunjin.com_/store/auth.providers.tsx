'use client';

import { AuthStoreProvider } from '@/store/auth.store';

export default function Providers({ children }: { children: React.ReactNode }) {
  return <AuthStoreProvider>{children}</AuthStoreProvider>;
}


