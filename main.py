import webbrowser
import pyautogui
import time
import tkinter as tk
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from tqdm import tqdm


# region 其他函数
# 发送邮件
def send_email(title, content):
    # 发送邮件
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = '27****83@qq.com'
    password = 'nlt*****jid'
    # 收信方邮箱
    to_addr = '31****15@qq.com'
    # 发信服务器
    smtp_server = 'smtp.qq.com'
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(content, 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header(from_addr)  # 发送者
    msg['To'] = Header(to_addr)  # 接收者
    msg['Subject'] = Header(title, 'utf-8')  # 邮件标题

    try:
        smtpobj = smtplib.SMTP_SSL(smtp_server)
        # 建立连接--qq邮箱服务和端口号（可百度查询）
        smtpobj.connect(smtp_server, 465)
        # 登录--发送者账号和口令
        smtpobj.login(from_addr, password)
        # 发送邮件
        smtpobj.sendmail(from_addr, to_addr, msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")
        return True
    finally:
        # 关闭服务器
        smtpobj.quit()
        return False


# 用来判断 是否有网络连接
def web_is_connect(id):
    try:
        response = requests.get(f'http://fwqnetwork.coolfaka.com/test_net.php?id={id}')
    except Exception:
        return False
    if response.status_code == 200 and response.text == 'ok':
        return True
    return False


# 消息框
def alert(message, timeout=3000):
    def close_window(window):
        window.destroy()
        window.quit()

    window = tk.Tk()
    window.withdraw()  # 隐藏主窗口，只显示提示框

    # 创建提示框
    message_box = tk.Toplevel()
    message_box.title("提示")

    # 获取屏幕尺寸
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 计算消息框位置
    message_width = 300
    message_height = 80
    x = (screen_width - message_width) // 2
    y = (screen_height - message_height) // 2

    # 设置消息框位置和大小
    message_box.geometry(f"{message_width}x{message_height}+{x}+{y}")

    message_label = tk.Label(message_box, text=message)
    message_label.pack(pady=20)

    # 让提示框在3秒后自动关闭
    message_box.after(timeout, lambda: close_window(message_box))

    window.mainloop()


# 找图 return_type='true/position'
def find_image(img, times=0, return_type='position'):
    if times == 5:
        print('找图失败，停止运行！')
        dao_ji_shi(1200)
        return False

    time.sleep(1)
    p = pyautogui.locateOnScreen(img, confidence=0.9)
    if p != None:
        if return_type == 'position':
            return pyautogui.center(p)
        else:
            return True
    else:
        if return_type == 'position':
            print(f'{img} 第{times + 1}次找图，没找到图，重新查找！')
            return find_image(img, times + 1, return_type)
        else:
            return False


# 输入账号密码
def press_key(strings):
    time.sleep(1)
    for s in strings:
        pyautogui.press(s)
        time.sleep(0.5)
    pyautogui.press('Esc')
    time.sleep(0.5)


# 点击屏幕
def click(x, y, c=None):
    time.sleep(1)
    if c != None:
        pyautogui.moveTo(c, duration=0.5)
    else:
        pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.click()


# 倒计时
def dao_ji_shi(time_long=3600):
    for i in tqdm(range(time_long)):
        time.sleep(1)


def write_log():
    with open('log.txt', 'r') as f:
        log = f.read()
    if log == '':
        rt = 0
    else:
        rt = log.split('[')[-1]
        rt = rt.split(']')[0]
        rt = int(rt)
    rt += 1
    log += f'[{rt}]    {time.strftime("%Y-%m-%d %H:%M:%S")}\n'
    with open('log.txt', 'w') as f:
        f.write(log)

# endregion

# 连接网络主程序
def main(username='', password=''):
    # 屏幕的宽度和高度
    width, height = pyautogui.size()
    d_width, d_height = 1920, 1080
    scale_height = height / d_height

    time.sleep(1)

    # 打开浏览器
    url = "http://2.2.2.2"
    webbrowser.open(url)
    time.sleep(1)

    # 找图
    # 查找第一个图
    p = find_image('./image/s1.png')
    if p==False:
        return False
    click(0, 0, p)
    # 判断是否已经链接网络
    is_connect = find_image('./image/ok.png', return_type='true')
    if is_connect:
        print('已经快速连接')
        time.sleep(1)
        pyautogui.hotkey("ctrl", "w")
        return True
    # 没有链接继续第二张图输入密码登录
    p = find_image('./image/s2.png')
    if p==False:
        return False
    click(p.x, p.y - 52 * 2 * scale_height)
    press_key(username)
    click(p.x, p.y - 55 * scale_height)
    press_key(password)
    click(0, 0, p)
    time.sleep(3)
    pyautogui.hotkey("ctrl", "w")
    print('操作完成')
    # 写入日志
    write_log()
    return True


if __name__ == '__main__':

    device = '16G'
    username = '12*****7'
    password = 'L*****44'

    while True:

        r = False
        while not r:
            r = web_is_connect('16')
            if not r:
                print('============ 网络断开，自动重新链接! ============', end='')
                main(username, password)
            time.sleep(3)
        print('============ 网络已连接! ============')
        # dao_ji_shi(5)
        dao_ji_shi(3600)

    # ========== 获取鼠标位置 ==========
    # for i in range(5000):
    #     mouse = pyautogui.position()
    #     print(mouse)
    #     print(mouse.x)
    #     time.sleep(2)
