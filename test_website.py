#!/usr/bin/env python
"""
彩票网站功能测试脚本
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_page(url, expected_status=200, description=""):
    """测试页面是否正常访问"""
    try:
        response = requests.get(f"{BASE_URL}{url}")
        status = "[OK]" if response.status_code == expected_status else "[FAIL]"
        print(f"{status} {description or url}: {response.status_code}")
        return response.status_code == expected_status
    except Exception as e:
        print(f"[FAIL] {description or url}: 连接失败 - {e}")
        return False

def main():
    """主测试函数"""
    print("彩票网站功能测试")
    print("=" * 50)
    
    # 测试主要页面
    tests = [
        ("/", "首页"),
        ("/lottery/", "彩票大厅"),
        ("/lottery/1/", "彩票详情页"),
        ("/draw-results/", "开奖结果"),
        ("/accounts/login/", "登录页面"),
        ("/accounts/register/", "注册页面"),
    ]
    
    passed = 0
    total = len(tests)
    
    for url, desc in tests:
        if test_page(url, description=desc):
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("所有基础功能测试通过！")
        print("\n测试账户信息:")
        print("管理员: admin / admin123")
        print("测试用户: testuser / test123")
        print("\n访问地址: http://127.0.0.1:8000")
    else:
        print("部分功能可能存在问题，请检查服务器日志")

if __name__ == "__main__":
    main()
