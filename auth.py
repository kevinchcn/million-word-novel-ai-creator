"""
API认证模块
"""

import streamlit as st
import requests
import os
from typing import Optional

class Authentication:
    def __init__(self):
        self.api_base = "https://api.deepseek.com"
    
    def authenticate(self, api_key: str) -> bool:
        """验证DeepSeek API密钥"""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # 简单的API调用测试
            test_payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 5
            }
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=test_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return True
            else:
                print(f"API返回错误: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"API验证异常: {str(e)}")
            return False
    
    def get_api_key(self) -> Optional[str]:
        """获取API密钥"""
        return st.session_state.get('api_key')

def check_api_key(api_key: str) -> bool:
    """检查API密钥有效性"""
    auth = Authentication()
    return auth.authenticate(api_key)

def save_api_key_to_env(api_key: str):
    """保存API密钥到环境文件"""
    env_file = ".env"
    
    # 读取现有文件
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    else:
        lines = []
    
    # 更新或添加API密钥
    found = False
    for i, line in enumerate(lines):
        if line.startswith("DEEPSEEK_API_KEY="):
            lines[i] = f"DEEPSEEK_API_KEY={api_key}\n"
            found = True
            break
    
    if not found:
        lines.append(f"DEEPSEEK_API_KEY={api_key}\n")
    
    # 写入文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    # 更新当前环境
    os.environ["DEEPSEEK_API_KEY"] = api_key
    
    return True

if __name__ == "__main__":
    # 测试验证功能
    import sys
    
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        if check_api_key(api_key):
            print("✅ API密钥有效")
            if input("是否保存到.env文件? (y/n): ").lower() == 'y':
                save_api_key_to_env(api_key)
                print("✅ API密钥已保存到.env文件")
        else:
            print("❌ API密钥无效")
    else:
        print("用法: python auth.py <api_key>")