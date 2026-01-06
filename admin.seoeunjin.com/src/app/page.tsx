"use client";

import { useState, useEffect } from "react";
import { LandingPage } from "./pages/LandingPage";
import { HomePage } from "./pages/HomePage";
import { useStore } from "../store";
import { useAuthStore } from "../store/authStore";

export default function Home() {
  const isLoggedIn = useStore((state) => state.user?.isLoggedIn);
  const [showLanding, setShowLanding] = useState(!isLoggedIn);
  const login = useStore((state) => state.user?.login);

  // ✅ access_token은 메모리(zustand)에서만 관리 (새로고침 시 사라지는 것이 정상)
  useEffect(() => {
    const token = useAuthStore.getState().accessToken;
    if (!token) {
      setShowLanding(true);
      return;
    }

    // 토큰이 있고 아직 로그인되지 않은 경우에만 (메모리 토큰 기반) 복원 시도
    if (!isLoggedIn && login) {
      try {
        const tokenParts = token.split('.');
        if (tokenParts.length === 3) {
          const payload = JSON.parse(atob(tokenParts[1]));
          const userId = payload.sub || payload.userId;
          const email = payload.email;
          const nickname = payload.nickname || payload.name || '사용자';

          login({
            id: userId ? parseInt(userId) : undefined,
            name: nickname,
            email: email || 'user@example.com',
          });
          setShowLanding(false);
        }
      } catch (error) {
        console.error('[page.tsx] 토큰 파싱 실패:', error);
        useAuthStore.getState().clearAccessToken();
        setShowLanding(true);
      }
    }
  }, []); // 최초 1회만 실행

  // isLoggedIn 상태가 변경되면 showLanding도 업데이트
  useEffect(() => {
    console.log('[page.tsx] isLoggedIn 상태 변경:', isLoggedIn);
    // 토큰도 함께 확인하여 확실하게 처리
    const token = useAuthStore.getState().accessToken;
    if (!isLoggedIn || !token) {
      setShowLanding(true);
    } else {
      setShowLanding(false);
    }
  }, [isLoggedIn]);

  const handleLogin = () => {
    console.log('[page.tsx] handleLogin 호출됨, isLoggedIn:', isLoggedIn);
    // 강제로 메인 화면으로 이동
    setShowLanding(false);

    // 로그인 상태가 아직 설정되지 않았다면 설정
    if (!isLoggedIn && login) {
      console.log('[page.tsx] 로그인 상태가 없어서 설정');
      login({
        name: 'Guest',
        email: 'guest@aiion.com',
      });
    }
  };

  if (showLanding) {
    return <LandingPage onLogin={handleLogin} />;
  }

  return <HomePage />;
}
