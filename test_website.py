#!/usr/bin/env python
"""
복권 사이트 기능 테스트 스크립트
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_page(url, expected_status=200, description=""):
    """페이지가 정상적으로 접근되는지 테스트합니다"""
    try:
        response = requests.get(f"{BASE_URL}{url}")
        status = "[OK]" if response.status_code == expected_status else "[FAIL]"
        print(f"{status} {description or url}: {response.status_code}")
        return response.status_code == expected_status
    except Exception as e:
        print(f"[FAIL] {description or url}: 연결 실패 - {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("복권 사이트 기능 테스트")
    print("=" * 50)
    
    # 주요 페이지 테스트
    tests = [
        ("/", "홈페이지"),
        ("/lottery/", "복권 로비"),
        ("/lottery/1/", "복권 상세 페이지"),
        ("/draw-results/", "당첨 결과"),
        ("/accounts/login/", "로그인 페이지"),
        ("/accounts/register/", "회원가입 페이지"),
    ]
    
    passed = 0
    total = len(tests)
    
    for url, desc in tests:
        if test_page(url, description=desc):
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"테스트 결과: {passed}/{total} 통과")
    
    if passed == total:
        print("모든 기본 기능 테스트 통과!")
        print("\n테스트 계정 정보:")
        print("관리자: admin / admin123")
        print("테스트 유저: testuser / test123")
        print("\n접속 주소: http://127.0.0.1:8000")
    else:
        print("일부 기능에 문제가 있을 수 있습니다. 서버 로그를 확인하세요.")

if __name__ == "__main__":
    main()
