import time
import frida

# 连接安卓机上的frida-server
device = frida.get_device('RST4AQAYS4AABEUK',1000)
# 启动`demo02`这个app
pid = device.spawn(["com.roysue.demo02"])
device.resume(pid)
time.sleep(1)
session = device.attach(pid)
# 加载s1.js脚本
with open("s1.js") as f:
    script = session.create_script(f.read())
script.load()

# 脚本会持续运行等待输入
raw_input()