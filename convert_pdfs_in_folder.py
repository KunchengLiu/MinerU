import os
import sys
import tkinter as tk
from tkinter import filedialog
import requests

# --- 根据您的 API 文档配置的变量 ---

# 1. API 基础 URL
API_BASE_URL = "http://127.0.0.1:8000"

# 2. API 端点 (根据您提供的文档)
API_ENDPOINT = "/file_parse"  # <--- 已更新

# 3. 输出子文件夹的名称
OUTPUT_SUBDIR = "md_output"

# ------------------------------------

def select_folder():
    """使用 Tkinter 弹出一个对话框让用户选择文件夹。"""
    print("正在打开文件夹选择对话框...")
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    folder_path = filedialog.askdirectory(title="请选择包含 PDF 的文件夹")
    
    if not folder_path:
        print("没有选择文件夹，程序即将退出。")
        sys.exit()
        
    print(f"已选择文件夹: {folder_path}")
    return folder_path

def call_conversion_api(pdf_path, api_url):
    """
    调用 Mineru API (/file_parse) 将单个 PDF 文件转换为 Markdown。
    
    :param pdf_path: 要转换的 PDF 文件的完整路径。
    :param api_url: 完整的 API 端点 URL。
    :return: 转换后的 Markdown 文本，如果失败则返回 None。
    """
    try:
        with open(pdf_path, 'rb') as f:
            files_payload = [
                ('files', (os.path.basename(pdf_path), f, 'application/pdf'))
            ]
            
            data_payload = {
                'return_md': True
            }
            
            # 发送 POST 请求，同时包含 files 和 data
            response = requests.post(api_url, files=files_payload, data=data_payload)
            
            # 检查响应
            if response.status_code == 200:
                
                # --- [!! 关键修改 !!] ---
                # API 返回的是 JSON，而不是原始字符串。
                try:
                    data = response.json()
                    
                    # 根据您的示例，结构为:
                    # {"results": {"FILENAME": {"md_content": "..."}}}
                    
                    # 1. 获取 'results' 字典
                    results_dict = data.get('results')
                    if not results_dict:
                        print(f"  [错误] API 响应中未找到 'results' 键。")
                        return None
                        
                    # 2. 'results' 里面似乎只有一个键（文件名）
                    #    我们获取 'results' 字典中第一个条目的值
                    first_file_key = next(iter(results_dict))
                    file_results = results_dict[first_file_key]
                    
                    # 3. 从中提取 'md_content'
                    md_content = file_results.get('md_content')
                    
                    if md_content is not None:
                        return md_content # 成功！返回真正的 Markdown
                    else:
                        print(f"  [错误] 在 API 响应的 'results' 中未找到 'md_content' 键。")
                        return None
                        
                except requests.exceptions.JSONDecodeError:
                    print(f"  [错误] API 响应不是有效的 JSON。 响应内容: {response.text[:150]}...")
                    return None
                except Exception as e:
                    print(f"  [错误] 解析 API 响应时出错: {e}")
                    return None
                # --- [!! 修改结束 !!] ---
                
            else:
                print(f"  [错误] API 返回状态码 {response.status_code}: {response.text[:100]}...")
                return None
                
    except requests.exceptions.ConnectionError:
        print(f"  [错误] 无法连接到 API 服务器: {api_url}")
        print("  请确保您的 Mineru API 服务 (mineru-api) 正在运行。")
        return None
    except Exception as e:
        print(f"  [错误] 调用 API 时发生未知错误: {e}")
        return None

def main():
    source_folder = select_folder()
    
    # 1. 定义并创建输出文件夹
    output_folder = os.path.join(source_folder, OUTPUT_SUBDIR)
    os.makedirs(output_folder, exist_ok=True)
    
    # 2. 准备 API URL
    full_api_url = API_BASE_URL + API_ENDPOINT
    print(f"将使用 API 端点: {full_api_url}")
    print(f"文件将保存在: {output_folder}\n")
    
    # 3. 遍历源文件夹中的所有文件
    success_count = 0
    fail_count = 0
    
    for filename in os.listdir(source_folder):
        # 确保只处理非隐藏的 PDF 文件
        if filename.lower().endswith('.pdf') and not filename.startswith('.'):
            pdf_path = os.path.join(source_folder, filename)
            
            # 4. 定义输出 MD 文件的路径
            md_filename = os.path.splitext(filename)[0] + ".md"
            md_path = os.path.join(output_folder, md_filename)
            
            print(f"--- 开始转换: {filename} ---")
            
            # 5. 调用 API 进行转换
            md_content = call_conversion_api(pdf_path, full_api_url)
            
            # 6. 保存结果
            if md_content:
                try:
                    with open(md_path, 'w', encoding='utf-8') as f:
                        f.write(md_content)
                    print(f"  [成功] 已保存为: {md_filename}")
                    success_count += 1
                except IOError as e:
                    print(f"  [错误] 无法写入文件 {md_path}: {e}")
                    fail_count += 1
            else:
                print(f"  [失败] 无法转换: {filename}")
                fail_count += 1
            
            print("-" * (len(filename) + 16)) # 打印分隔线
            
    print("\n======================")
    print("转换完成！")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {fail_count} 个文件")
    print("======================")

if __name__ == "__main__":
    # 确保 tkinter 窗口在 macOS 或某些 Linux 上能正常弹出
    try:
        main()
    except Exception as e:
        print(f"发生严重错误: {e}")
    finally:
        # 确保程序在结束后能退出，防止 tkinter 挂起
        if 'tk' in locals() or 'tk' in sys.modules:
            try:
                tk.Tk().destroy()
            except:
                pass
        os._exit(0) # 强制退出