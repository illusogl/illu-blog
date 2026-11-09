# 答案不唯一时用这个（diff 会误报），例如"输出任意一个重心/任意一组解"
# 用法: python checker.py   （自动编译 gen 和 sol，循环验证 sol 输出的合法性）
import subprocess, os

EX = ".exe" if os.name == "nt" else ""   # Windows 下自动加 .exe

def check(inp, out):
    """验证 out 是不是 inp 的合法输出。返回 None = 通过，返回字符串 = 错误原因"""
    tok = iter(inp.split())
    res = out.split()
    # ===== 每道题只改这里：读入格式 + 逐条合法性判定 =====
    n = int(next(tok))
    if len(res) != n:
        return "输出个数不对"
    # 例：算出参考答案后逐条比对/验证 res 每一项是否合法
    # for i, x in enumerate(res):
    #     if not 合法(x): return f"第{i}条非法"
    return None
    # ===== 改到这里为止 =====

subprocess.run(f"g++ -O2 sol.cpp -o sol{EX} && g++ -O2 gen.cpp -o gen{EX}",
               shell=True, check=True)
for i in range(1, 100001):
    inp = subprocess.run([f"./gen{EX}", str(i)], capture_output=True).stdout
    r = subprocess.run([f"./sol{EX}"], input=inp, capture_output=True)
    if r.returncode != 0:
        print(f"RE! seed={i}")
        open("in.txt", "wb").write(inp)
        break
    msg = check(inp.decode(), r.stdout.decode())
    if msg:
        print(f"WA! seed={i}: {msg}")
        open("in.txt", "wb").write(inp)
        print(inp.decode())
        break
else:
    print("OK: 100000 tests passed")
