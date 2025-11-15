#!/usr/bin/env python
"""
Git仓库设置脚本 - 为彩票网站项目创建Git仓库
"""
import os
import subprocess
import sys

def run_command(command, description=""):
    """运行命令并显示结果"""
    print(f"执行: {command}")
    if description:
        print(f"说明: {description}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"[OK] 成功")
            if result.stdout.strip():
                print(f"输出: {result.stdout.strip()}")
        else:
            print(f"[FAIL] 失败")
            if result.stderr.strip():
                print(f"错误: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] 执行失败: {e}")
        return False

def setup_git_repository():
    """设置Git仓库"""
    print("彩票网站项目 - Git仓库设置")
    print("=" * 50)
    
    # 检查是否已经是Git仓库
    if os.path.exists('.git'):
        print("[INFO] 当前目录已经是Git仓库")
    else:
        # 初始化Git仓库
        if not run_command("git init", "初始化Git仓库"):
            return False
    
    # 检查Git配置
    print("\n检查Git配置...")
    run_command("git config user.name", "检查用户名配置")
    run_command("git config user.email", "检查邮箱配置")
    
    # 如果没有配置，提示用户配置
    result = subprocess.run("git config user.name", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("\n[INFO] 请配置Git用户信息:")
        print("git config --global user.name \"Your Name\"")
        print("git config --global user.email \"your.email@example.com\"")
        print("\n或者为此项目单独配置:")
        print("git config user.name \"AlexKaili\"")
        print("git config user.email \"alex@example.com\"")
    
    # 创建.gitignore文件（如果不存在）
    if not os.path.exists('.gitignore'):
        print("\n[INFO] .gitignore文件已存在")
    else:
        print("\n[OK] .gitignore文件已存在")
    
    # 添加所有文件到暂存区
    print("\n添加文件到Git...")
    if not run_command("git add .", "添加所有文件到暂存区"):
        return False
    
    # 检查状态
    run_command("git status", "检查Git状态")
    
    # 创建初始提交
    print("\n创建初始提交...")
    commit_message = "Initial commit: Django lottery website with Docker support"
    if not run_command(f'git commit -m "{commit_message}"', "创建初始提交"):
        print("[INFO] 可能没有新的更改需要提交")
    
    # 显示提交历史
    run_command("git log --oneline", "显示提交历史")
    
    print("\n" + "=" * 50)
    print("Git仓库设置完成！")
    print("=" * 50)
    print("下一步操作:")
    print("1. 在GitHub上创建新仓库 'lottery-website'")
    print("2. 添加远程仓库:")
    print("   git remote add origin https://github.com/AlexKaili/lottery-website.git")
    print("3. 推送代码到GitHub:")
    print("   git branch -M main")
    print("   git push -u origin main")
    print("\n项目GitHub地址: https://github.com/AlexKaili/lottery-website")
    
    return True

if __name__ == "__main__":
    setup_git_repository()
