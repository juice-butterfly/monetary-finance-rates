# -*- coding: utf-8 -*-
"""生成「利率传导诊断台」扫码展板：大二维码 + 演示三步指引。
配色沿用应用自身的米白设计令牌。"""
import io
import os
import re

import segno

URL = "https://juice-butterfly.github.io/monetary-finance-rates/"
OUT_DIR = r"C:\Users\Lenovo\Desktop"
HTML_OUT = os.path.join(OUT_DIR, "利率传导诊断台-扫码展板.html")
PNG_QR = os.path.join(OUT_DIR, "利率传导诊断台-二维码.png")

# ---- 二维码 ----
# border=4 是 QR 规范要求的静音区（四周至少 4 个模块宽的白边），少了会扫不出来
qr = segno.make(URL, error="h")
BORDER = 4
svg_inner = qr.svg_inline(scale=1, border=BORDER, dark="#1F2328", light="#FFFFFF")
# segno 输出的 <svg> 没有 viewBox，宽高被写死 → CSS 拉伸会失效。
# 用符号尺寸补一个 viewBox，才能等比缩放到任意大小。
_side = qr.symbol_size(scale=1, border=BORDER)[0]
svg_inner = re.sub(
    r'<svg width="\d+" height="\d+"',
    '<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet"' % (_side, _side),
    svg_inner, count=1)
assert "viewBox" in svg_inner, "viewBox 注入失败"

# 同时导出一张独立的高清二维码 PNG（备用）
qr.save(PNG_QR, scale=16, border=4, dark="#1F2328", light="#FFFFFF")

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>扫码展板 · 利率传导诊断台</title>
<style>
:root{
  --bg:#F6F4F0;--surface:#FFFFFF;--surface2:#FBFAF7;
  --line:#E5E0D8;--line2:#D3CDC2;
  --ink:#1F2328;--ink2:#5A616B;--ink3:#8D949E;
  --amber:#A9762F;--amber2:#C08F3E;--amber-bg:#FAF3E4;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1480px;overflow:hidden}
body{
  background:radial-gradient(1000px 380px at 16% -14%,#FFFFFF,transparent 72%),var(--bg);
  color:var(--ink);
  font:15px/1.6 "Microsoft YaHei","PingFang SC",system-ui,sans-serif;
  padding:56px 64px 44px;display:flex;flex-direction:column;
}
.eyebrow{font-size:13.5px;color:var(--ink3);letter-spacing:.6px}
h1{font-size:46px;font-weight:600;letter-spacing:1px;margin:12px 0 0}
h1 .sub{font-size:19px;font-weight:400;color:var(--ink3);letter-spacing:0;margin-left:14px}
.rule{height:1px;background:var(--line);margin:26px 0 0}
.lede{font-size:17px;color:var(--ink2);margin-top:22px;line-height:1.85;max-width:900px}
.lede b{color:var(--ink);font-weight:600}
.qrwrap{
  margin:34px auto 0;background:var(--surface);border:1px solid var(--line);
  border-radius:20px;padding:30px 30px 24px;display:flex;flex-direction:column;align-items:center;
  box-shadow:0 2px 22px rgba(31,35,40,.05);
}
.qrbox{width:560px;height:560px}
.qrbox svg{width:100%;height:100%;display:block;shape-rendering:crispEdges}
.qrcap{margin-top:20px;font-size:22px;font-weight:600;letter-spacing:.4px}
.qrurl{margin-top:9px;font-size:14.5px;color:var(--ink3);letter-spacing:.2px;
  font-family:ui-monospace,Consolas,monospace;word-break:break-all;text-align:center}
.steps{margin-top:34px;display:flex;gap:16px}
.step{flex:1;background:var(--surface2);border:1px solid var(--line);border-radius:12px;padding:16px 17px}
.step .n{
  display:inline-flex;align-items:center;justify-content:center;
  width:26px;height:26px;border-radius:50%;background:var(--amber);color:#fff;
  font-size:14px;font-weight:600;margin-bottom:10px;
}
.step .t{font-size:15.5px;font-weight:600;margin-bottom:6px}
.step .d{font-size:13px;color:var(--ink2);line-height:1.68}
.foot{margin-top:auto;padding-top:22px;font-size:12.5px;color:var(--ink3);line-height:1.7;border-top:1px solid var(--line)}
.foot b{color:var(--ink2);font-weight:600}
</style>
</head>
<body>

<div class="eyebrow">中南财经政法大学 · 货币金融学 · 利率部分 · 小组展示</div>
<h1>利率传导诊断台<span class="sub">今天中国的利率，卡在哪一环</span></h1>
<div class="rule"></div>

<p class="lede">
把课程知识做成一台<b>可推导</b>的诊断台：参数随便拖，传导链当场变色；
AI 只负责组织语言，<b>每个数字都能回查到出处</b>，编不出来的会被当场标红。
</p>

<div class="qrwrap">
  <div class="qrbox">__QR_SVG__</div>
  <div class="qrcap">扫码打开 · 手机也能用</div>
  <div class="qrurl">__URL__</div>
</div>

<div class="steps">
  <div class="step">
    <div class="n">1</div>
    <div class="t">拖参数</div>
    <div class="d">左侧九个参数可直接拖、也可填数字。看「传导链」哪一环被点亮变琥珀色。</div>
  </div>
  <div class="step">
    <div class="n">2</div>
    <div class="t">切图表</div>
    <div class="d">利率走廊、中美对照、收益率曲线、久期敏感性 —— 都是真算出来的。</div>
  </div>
  <div class="step">
    <div class="n">3</div>
    <div class="t">点生成解读</div>
    <div class="d">AI 按课程框架输出五段：现象 · 理论 · 机制 · 含义 · 局限，底部校验条核验数字。</div>
  </div>
</div>

<div class="foot">
<b>口径来源优先级：</b>陈思翀老师课件（第三讲）＞《中国金融学》（西南财经大学编写组）＞ 朱新蓉《货币金融学》第五版（仅作章节骨架）。
利率走廊上下限为示意口径。
</div>

</body>
</html>
"""

HTML = HTML.replace("__QR_SVG__", svg_inner).replace("__URL__", URL)

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(HTML)

print("展板 HTML :", HTML_OUT, os.path.getsize(HTML_OUT), "bytes")
print("独立二维码:", PNG_QR, os.path.getsize(PNG_QR), "bytes")
print("URL       :", URL)
