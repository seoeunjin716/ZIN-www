/**
 * 메인 서비스 - 로그인 핸들러 함수들
 * 클로저 패턴을 사용하여 공통 설정을 외부 스코프에 유지하고 이너 함수로 핸들러를 정의
 */
import { authStoreActions } from '@/store/auth.store';

/**
 * ✅ 로그인 성공 처리
 * - accessToken: 프론트 메모리(Zustand store)에만 저장
 * - refreshToken: HttpOnly Cookie 로 저장되어야 하며, 이는 **백엔드(Set-Cookie)** 가 담당
 *
 * ⚠️ 프론트(JS)에서는 HttpOnly 쿠키를 저장/수정할 수 없습니다.
 *    대신, 백엔드 응답의 Set-Cookie가 브라우저에 저장되도록 fetch에 credentials:'include'를 설정합니다.
 */
export function saveAccessToken(accessToken: string) {
  authStoreActions.setAccessToken(accessToken);
}

export function clearAccessToken() {
  authStoreActions.clearAccessToken();
}

export const { handleGoogleLogin, handleKakaoLogin, handleNaverLogin } = (() => {
  // 외부 스코프 - 공통 설정 및 변수
  const baseUrl = process.env.NEXT_PUBLIC_GATEWAY_URL || 'http://localhost:8080';

  /**
   * 구글 로그인 핸들러 (이너 함수)
   * 백엔드 POST /google/login -> { success, authUrl }
   */
  async function handleGoogleLogin() {
    try {
      const googleLoginUrl = `${baseUrl}/google/login`;

      const response = await fetch(googleLoginUrl, {
        method: 'POST',
        // refreshToken 쿠키가 Set-Cookie로 내려오는 구조라면 저장되도록 설정
        credentials: 'include',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });

      if (!response.ok) {
        const errorText = await response.text().catch(() => '');
        console.error('HTTP 에러:', response.status, response.statusText, errorText);
        alert(`서버 오류가 발생했습니다 (${response.status}). 백엔드 서버가 실행 중인지 확인해주세요.`);
        return;
      }

      const data = await response.json();

      if (data.success && data.authUrl) {
        window.location.href = data.authUrl;
      } else {
        const errorMessage = data.message || '알 수 없는 오류';
        console.error('인증 URL 가져오기 실패:', errorMessage, '전체 응답:', data);
        alert('구글 로그인을 시작할 수 없습니다: ' + errorMessage);
      }
    } catch (error) {
      console.error('구글 로그인 실패:', error);

      if (error instanceof TypeError && error.message.includes('fetch')) {
        alert(`백엔드 서버(${baseUrl})에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.`);
      } else {
        alert('구글 로그인 중 오류가 발생했습니다: ' + (error instanceof Error ? error.message : String(error)));
      }
    }
  }

  /**
   * 카카오 로그인 핸들러 (이너 함수)
   * 백엔드 POST /kakao/login -> { success, authUrl }
   */
  async function handleKakaoLogin() {
    try {
      const response = await fetch(`${baseUrl}/kakao/login`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });

      if (!response.ok) {
        const errorText = await response.text().catch(() => '');
        console.error('HTTP 에러:', response.status, response.statusText, errorText);
        alert(`서버 오류가 발생했습니다 (${response.status}). 백엔드 서버가 실행 중인지 확인해주세요.`);
        return;
      }

      const data = await response.json();

      if (data.success && data.authUrl) {
        window.location.href = data.authUrl;
      } else {
        const errorMessage = data.message || '알 수 없는 오류';
        console.error('인증 URL 가져오기 실패:', errorMessage, '전체 응답:', data);
        alert('카카오 로그인을 시작할 수 없습니다: ' + errorMessage);
      }
    } catch (error) {
      console.error('카카오 로그인 실패:', error);

      if (error instanceof TypeError && error.message.includes('fetch')) {
        alert(`백엔드 서버(${baseUrl})에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.`);
      } else {
        alert('카카오 로그인 중 오류가 발생했습니다: ' + (error instanceof Error ? error.message : String(error)));
      }
    }
  }

  /**
   * 네이버 로그인 핸들러
   * ✅ 가장 단순/안정: 백엔드 엔드포인트로 이동 (리다이렉트 기반)
   */
  function handleNaverLogin() {
    window.location.href = `${baseUrl}/naver/login`;
  }

  return {
    handleGoogleLogin,
    handleKakaoLogin,
    handleNaverLogin,
  };
})();


