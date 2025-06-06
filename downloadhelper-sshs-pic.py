import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3
import tkinter as tk
from tkinter import messagebox
import threading


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import time

import concurrent.futures

def download_images_from_page(url, output_folder=None, progress_callback=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Referer': url
    }
    for attempt in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=10, verify=False)
            res.raise_for_status()
            break
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2)
    res = requests.get(url, headers=headers, timeout=10, verify=False)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    title_tag = soup.find('span', class_='post-info-text')
    if title_tag:
        folder_name = title_tag.get_text(strip=True)
    else:
        folder_name = 'images'
    if output_folder is None:
        output_folder = folder_name
    os.makedirs(output_folder, exist_ok=True)
    img_tags = soup.find_all('img')
    total = len(img_tags)
    count = 0
    if progress_callback:
        progress_callback(f"共找到 {total} 张图片。")

    def download_one(idx, img):
        img_url = img.get('data-original') or img.get('src')
        if not img_url:
            return False
        full_url = urljoin(url, img_url)
        if progress_callback:
            progress_callback(f"正在下载 {idx}/{total} ...")
        try:
            img_data = requests.get(full_url, headers=headers, timeout=10, verify=False).content
            ext = os.path.splitext(full_url)[-1]
            if not ext or len(ext) > 5:
                ext = '.jpg'
            with open(os.path.join(output_folder, f'image_{idx}{ext}'), 'wb') as f:
                f.write(img_data)
            return True
        except Exception:
            return False

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda args: download_one(*args), enumerate(img_tags, 1)))
    count = sum(results)
    return count, output_folder

def paste_from_clipboard():
    try:
        url = root.clipboard_get()
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)
    except Exception as e:
        messagebox.showerror("错误", f"无法从剪贴板获取内容：{e}")

def start_download():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("提示", "请输入网址")
        return
    download_button.config(state=tk.DISABLED)
    status_label.config(text="正在下载，请稍候...")

    def update_status(msg):
        status_label.config(text=msg)

    def task():
        try:
            count, folder = download_images_from_page(url, progress_callback=update_status)
            status_label.config(text=f"下载完成！\n共下载 {count} 张图片\n保存在文件夹: ß{folder}")
            # 移除弹窗
            # messagebox.showinfo("完成", f"下载完成，共下载 {count} 张图片，保存在文件夹：{folder}")
        except Exception as e:
            status_label.config(text="下载失败")
            messagebox.showerror("错误", f"下载失败：{e}")
        finally:
            download_button.config(state=tk.NORMAL)
    threading.Thread(target=task).start()

root = tk.Tk()
root.title("图片批量下载器｜绅士会所特化版")
root.geometry("400x400")

tk.Label(root, text="请输入网址：").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack()
paste_button = tk.Button(root, text="粘贴网址", command=paste_from_clipboard)
paste_button.pack(pady=2)
download_button = tk.Button(root, text="下载", command=start_download)
download_button.pack(pady=10)
status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()