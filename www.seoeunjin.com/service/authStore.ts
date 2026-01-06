import { create } from 'zustand';

/**
 * ✅ Access Token 저장 원칙
 * - access_token은 절대 localStorage/sessionStorage/cookie에 저장하지 않음
 * - 브라우저 메모리(= zustand store)에서만 보관 (5~15분 단기)
 * - 새로고침/탭 종료 시 토큰이 사라지는 것이 정상 동작
 */
type AuthState = {
    accessToken: string | null;
};

type AuthActions = {
    setAccessToken: (token: string) => void;
    clearAccessToken: () => void;
};

export const useAuthStore = create<AuthState & AuthActions>((set) => ({
    accessToken: null,
    setAccessToken: (token) => set({ accessToken: token }),
    clearAccessToken: () => set({ accessToken: null }),
}));


