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
     * 백엔드 GET /api/auth/google/auth-url 엔드포인트로 연결
     * 백엔드 구조: 인증 URL 받기 → 구글 로그인 → 백엔드 콜백 처리 → 프론트엔드로 JWT 토큰 전달
     */
    async function handleGoogleLogin() {
        try {
            // ✅ 백엔드 실제 엔드포인트: POST /google/login -> { success, authUrl }
            const googleLoginUrl = `${baseUrl}/google/login`;

            console.log("구글 로그인 요청 시작");
            console.log('구글 로그인 요청 URL:', googleLoginUrl);

            // POST 요청 (백엔드 @PostMapping("/login")에 맞춤)
            const response = await fetch(googleLoginUrl, {
                method: 'POST',
                // refreshToken 쿠키가 Set-Cookie로 내려오는 구조라면 저장되도록 설정
                credentials: 'include',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}),
            });

            // HTTP 응답 상태 확인
            if (!response.ok) {
                const errorText = await response.text().catch(() => '');
                console.error('HTTP 에러:', response.status, response.statusText, errorText);
                alert(`서버 오류가 발생했습니다 (${response.status}). 백엔드 서버가 실행 중인지 확인해주세요.`);
                return;
            }

            const data = await response.json();
            console.log('구글 인증 URL 응답:', data);

            if (data.success && data.authUrl) {
                // 구글 인가 페이지로 리다이렉트
                // 백엔드가 콜백 처리 후 프론트엔드 메인 페이지(/)로 JWT 토큰과 함께 리다이렉트
                window.location.href = data.authUrl;
            } else {
                const errorMessage = data.message || '알 수 없는 오류';
                console.error('인증 URL 가져오기 실패:', errorMessage, '전체 응답:', data);
                alert('구글 로그인을 시작할 수 없습니다: ' + errorMessage);
            }
        } catch (error) {
            console.error("구글 로그인 실패:", error);

            // 네트워크 에러인 경우
            if (error instanceof TypeError && error.message.includes('fetch')) {
                alert(`백엔드 서버(${baseUrl})에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.`);
            } else {
                alert('구글 로그인 중 오류가 발생했습니다: ' + (error instanceof Error ? error.message : String(error)));
            }
        }
    }

    /**
     * 카카오 로그인 핸들러 (이너 함수)
     */
    async function handleKakaoLogin() {
        // 카카오 로그인 시작: 인증 URL 가져오기
        try {
            // ✅ 백엔드 실제 엔드포인트: POST /kakao/login -> { success, authUrl }
            const response = await fetch(`${baseUrl}/kakao/login`, {
                method: 'POST',
                // refreshToken 쿠키가 Set-Cookie로 내려오는 구조라면 저장되도록 설정
                credentials: 'include',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}),
            });

            // HTTP 응답 상태 확인
            if (!response.ok) {
                const errorText = await response.text().catch(() => '');
                console.error('HTTP 에러:', response.status, response.statusText, errorText);
                alert(`서버 오류가 발생했습니다 (${response.status}). 백엔드 서버가 실행 중인지 확인해주세요.`);
                return;
            }

            const data = await response.json();
            console.log('API 응답:', data);

            if (data.success && data.authUrl) {
                // 카카오 인가 페이지로 리다이렉트
                window.location.href = data.authUrl;
            } else {
                const errorMessage = data.message || '알 수 없는 오류';
                console.error('인증 URL 가져오기 실패:', errorMessage, '전체 응답:', data);
                alert('카카오 로그인을 시작할 수 없습니다: ' + errorMessage);
            }
        } catch (error) {
            console.error("카카오 로그인 실패:", error);

            // 네트워크 에러인 경우
            if (error instanceof TypeError && error.message.includes('fetch')) {
                alert(`백엔드 서버(${baseUrl})에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.`);
            } else {
                alert('카카오 로그인 중 오류가 발생했습니다: ' + (error instanceof Error ? error.message : String(error)));
            }
        }
    }

    /**
     * 네이버 로그인 핸들러 (이너 함수)
     */
    function handleNaverLogin() {
        // ✅ 가장 단순/안정: 백엔드 엔드포인트로 이동 (리다이렉트 기반)
        window.location.href = `${baseUrl}/naver/login`;
    }

    // 클로저를 통해 이너 함수들을 반환
    return {
        handleGoogleLogin,
        handleKakaoLogin,
        handleNaverLogin,
    };
})();

