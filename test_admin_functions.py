#!/usr/bin/env python
"""
管理员功能测试脚本
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_admin_page(url, expected_status=200, description=""):
    """测试管理员页面是否正常访问"""
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
    print("管理员功能测试")
    print("=" * 50)
    
    # 测试管理员页面
    admin_tests = [
        ("/management/", "管理仪表板"),
        ("/management/sales-report/", "销售报告"),
        ("/management/draw-management/", "开奖管理"),
        ("/management/create-draw/", "创建期次"),
        ("/management/user-management/", "用户管理"),
        ("/management/lottery-type-management/", "彩票类型管理"),
        ("/admin/", "Django后台"),
    ]
    
    passed = 0
    total = len(admin_tests)
    
    print("测试管理员功能页面...")
    for url, desc in admin_tests:
        if test_admin_page(url, description=desc):
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"管理员功能测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("所有管理员功能正常！")
        print("\n管理员登录信息:")
        print("Django后台: http://127.0.0.1:8000/admin/")
        print("自定义后台: http://127.0.0.1:8000/management/")
        print("用户名: admin")
        print("密码: admin123")
    else:
        print("部分管理员功能可能存在问题")
    
    # 测试普通用户页面
    print("\n" + "=" * 50)
    print("测试普通用户功能页面...")
    
    user_tests = [
        ("/", "首页"),
        ("/lottery/", "彩票大厅"),
        ("/lottery/1/", "彩票详情"),
        ("/draw-results/", "开奖结果"),
        ("/accounts/login/", "登录页面"),
        ("/accounts/register/", "注册页面"),
    ]
    
    user_passed = 0
    user_total = len(user_tests)
    
    for url, desc in user_tests:
        if test_admin_page(url, description=desc):
            user_passed += 1
    
    print(f"用户功能测试结果: {user_passed}/{user_total} 通过")
    
    total_passed = passed + user_passed
    total_tests = total + user_total
    
    print("\n" + "=" * 50)
    print(f"整体测试结果: {total_passed}/{total_tests} 通过")
    
    if total_passed == total_tests:
        print("彩票网站所有功能正常运行！")
    else:
        print("部分功能需要检查")

if __name__ == "__main__":
    main()
