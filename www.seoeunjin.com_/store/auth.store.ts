/* eslint-disable @typescript-eslint/consistent-type-definitions */
'use client';

import React, { createContext, useContext, useEffect } from 'react';
import { useStore } from 'zustand';
import { createStore } from 'zustand/vanilla';

/**
 * ✅ 토큰 저장 정책
 * - accessToken: 브라우저 메모리(Zustand)에서만 보관
 * - refreshToken: HttpOnly Cookie (프론트에서 접근/저장 로직 작성 금지)
 *
 * 결과적으로 새로고침/탭 종료 시 accessToken이 사라지는 것이 정상 동작입니다.
 */

// ---------------------------------------------------------------------------
// Ducks: types / actionTypes / actions / reducer / selectors
// ---------------------------------------------------------------------------

export type AuthState = {
  accessToken: string | null;
};

export const authActionTypes = {
  SET_ACCESS_TOKEN: 'auth/SET_ACCESS_TOKEN',
  CLEAR_ACCESS_TOKEN: 'auth/CLEAR_ACCESS_TOKEN',
} as const;

export type AuthAction =
  | { type: typeof authActionTypes.SET_ACCESS_TOKEN; payload: string | null }
  | { type: typeof authActionTypes.CLEAR_ACCESS_TOKEN };

export const authActions = {
  setAccessToken: (token: string | null): AuthAction => ({
    type: authActionTypes.SET_ACCESS_TOKEN,
    payload: token,
  }),
  clearAccessToken: (): AuthAction => ({
    type: authActionTypes.CLEAR_ACCESS_TOKEN,
  }),
};

export const authInitialState: AuthState = {
  accessToken: null,
};

export function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case authActionTypes.SET_ACCESS_TOKEN:
      return { ...state, accessToken: action.payload };
    case authActionTypes.CLEAR_ACCESS_TOKEN:
      return { ...state, accessToken: null };
    default:
      return state;
  }
}

export const authSelectors = {
  selectAccessToken: (s: AuthState) => s.accessToken,
  selectIsAuthenticated: (s: AuthState) => Boolean(s.accessToken),
} as const;

// ---------------------------------------------------------------------------
// Zustand store (Provider 기반)
// ---------------------------------------------------------------------------

export type AuthActionsApi = {
  setAccessToken: (token: string) => void;
  clearAccessToken: () => void;
  dispatch: (action: AuthAction) => void;
};

export type AuthStore = AuthState & AuthActionsApi;

export const createAuthStore = (preloadedState?: Partial<AuthState>) =>
  createStore<AuthStore>()((set) => ({
    ...authInitialState,
    ...preloadedState,

    dispatch: (action) => set((state) => authReducer(state, action)),

    setAccessToken: (token) => set((state) => authReducer(state, authActions.setAccessToken(token))),
    clearAccessToken: () => set((state) => authReducer(state, authActions.clearAccessToken())),
  }));

export type AuthStoreApi = ReturnType<typeof createAuthStore>;

const AuthStoreContext = createContext<AuthStoreApi | null>(null);

/**
 * ✅ 싱글톤 스토어
 * - Provider 내부/외부(유틸 함수) 모두에서 같은 store 인스턴스를 사용
 * - mainservice.ts 같은 non-React 모듈에서도 accessToken 저장 가능
 */
export const authStore: AuthStoreApi = createAuthStore();

export const authStoreActions = {
  setAccessToken: (token: string) => authStore.getState().setAccessToken(token),
  clearAccessToken: () => authStore.getState().clearAccessToken(),
} as const;

export type AuthStoreProviderProps = {
  children: React.ReactNode;
  initialAccessToken?: string | null;
};

export function AuthStoreProvider({ children, initialAccessToken = null }: AuthStoreProviderProps) {
  // 초기 토큰이 필요한 케이스가 있다면(예: 서버에서 hydrate) 한 번만 반영
  useEffect(() => {
    if (initialAccessToken && !authStore.getState().accessToken) {
      authStore.getState().setAccessToken(initialAccessToken);
    }
  }, [initialAccessToken]);

  return React.createElement(AuthStoreContext.Provider, { value: authStore }, children);
}

export function useAuthStore<T>(selector: (state: AuthStore) => T): T {
  const store = useContext(AuthStoreContext);
  if (!store) {
    throw new Error('useAuthStore must be used within <AuthStoreProvider>.');
  }
  return useStore(store, selector);
}

export function useAuthStoreApi(): AuthStoreApi {
  const store = useContext(AuthStoreContext);
  if (!store) {
    throw new Error('useAuthStoreApi must be used within <AuthStoreProvider>.');
  }
  return store;
}


