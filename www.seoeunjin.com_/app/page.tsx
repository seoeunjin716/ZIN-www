'use client';

import { Suspense, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { handleGoogleLogin, handleKakaoLogin, handleNaverLogin, saveAccessToken } from '@/service/mainservice';
import { useAuthStore } from '@/store/auth.store';

function HomeInner() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const accessToken = useAuthStore((state) => state.accessToken);

  useEffect(() => {
    // OAuth 로그인 콜백 처리 (백엔드에서 토큰과 함께 리다이렉트)
    const token = searchParams.get('token');
    const providerParam = searchParams.get('provider');
    const error = searchParams.get('error');
    const errorDescription = searchParams.get('error_description');
    const errorMessage = searchParams.get('message');

    if (token) {
      // ✅ access_token은 메모리(zustand)에만 저장
      saveAccessToken(token);

      console.log('OAuth 로그인 성공, 토큰 저장 완료');

      // 대시보드로 리다이렉트
      router.push(`/dashboard/${providerParam || 'google'}`);
      return;
    } else if (error) {
      // 에러 처리
      const errorMsg = errorMessage 
        ? decodeURIComponent(errorMessage) 
        : errorDescription 
        ? decodeURIComponent(errorDescription) 
        : error;
      
      console.error('OAuth 로그인 에러:', error, errorMsg);
      
      // 에러 타입에 따른 메시지 표시
      let displayMessage = '';
      if (error.includes('google')) {
        displayMessage = `구글 로그인 실패: ${errorMsg}`;
      } else if (error.includes('kakao')) {
        displayMessage = `카카오 로그인 실패: ${errorMsg}`;
      } else if (error.includes('naver')) {
        displayMessage = `네이버 로그인 실패: ${errorMsg}`;
      } else {
        displayMessage = `로그인 실패: ${errorMsg}`;
      }
      
      alert(displayMessage);
      return;
    }

    // 로그아웃 파라미터가 있으면 리다이렉트하지 않음
    const logout = searchParams.get('logout');
    if (logout === 'true') {
      // 로그아웃 처리 완료 후 URL 정리
      router.replace('/');
      return;
    }

    // 이미 로그인된 사용자는 대시보드로 리다이렉트
    if (accessToken) {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        try {
          const user = JSON.parse(storedUser);
          const provider = user.provider || 'google';
          router.push(`/dashboard/${provider}`);
          return;
        } catch (err) {
          console.error('사용자 정보 파싱 실패:', err);
        }
      }
    }
  }, [searchParams, router, accessToken]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-white font-sans">
      <main className="flex w-full max-w-md flex-col items-center gap-8 px-8 py-16">
        <h1 className="text-3xl font-bold text-gray-900">로그인</h1>
        <div className="flex w-full flex-col gap-4">
          <button
            onClick={handleGoogleLogin}
            className="flex h-14 w-full items-center justify-center gap-3 rounded-lg border border-gray-300 bg-white px-6 text-base font-medium text-gray-700 transition-colors hover:bg-gray-50"
          >
            <svg
              className="h-5 w-5"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                fill="#4285F4"
              />
              <path
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                fill="#34A853"
              />
              <path
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                fill="#FBBC05"
              />
              <path
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                fill="#EA4335"
              />
            </svg>
            구글 로그인
          </button>
          <button
            onClick={handleKakaoLogin}
            className="flex h-14 w-full items-center justify-center gap-3 rounded-lg bg-[#FEE500] px-6 text-base font-medium text-gray-900 transition-colors hover:bg-[#FDD835] cursor-pointer"
          >
            <svg
              className="h-5 w-5"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 3C6.48 3 2 6.48 2 11c0 2.4 1.06 4.57 2.75 6.04L3 21l4.28-1.35C8.5 20.5 10.17 21 12 21c5.52 0 10-3.48 10-8s-4.48-10-10-10z"
                fill="#000000"
              />
            </svg>
            카카오 로그인
          </button>
          <button
            onClick={handleNaverLogin}
            className="flex h-14 w-full items-center justify-center gap-3 rounded-lg bg-[#03C75A] px-6 text-base font-medium text-white transition-colors hover:bg-[#02B350]"
          >
            <svg
              className="h-5 w-5"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M16.273 12.845L7.376 0H0v24h7.726V11.156L16.624 24H24V0h-7.727v12.845z"
                fill="#FFFFFF"
              />
            </svg>
            네이버 로그인
          </button>
        </div>
      </main>
    </div>
  );
}

export default function Home() {
  // Next 16: useSearchParams() 사용 컴포넌트는 Suspense로 감싸야 prerender 에러가 나지 않음
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center bg-white font-sans">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-transparent"></div>
        </div>
      }
    >
      <HomeInner />
    </Suspense>
  );
}
