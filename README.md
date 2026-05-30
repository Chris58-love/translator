# 实时同声传译工具

这是一个本地运行的个人实时同声传译工具。浏览器负责英语语音识别和字幕展示，FastAPI 后端负责调用 DeepSeek API 翻译，支持 partial 增量翻译、final 最终校正、术语表、翻译风格、网络模式切换和字幕导出。

## 功能概览

- 英语实时语音识别。
- 英文 interim / final 字幕展示。
- DeepSeek API 中文翻译。
- WebSocket `/ws/translate` 实时通信。
- HTTP `/translate` fallback。
- partial 增量翻译和 final 最终校正。
- partial 翻译保留机制，减少长句字幕闪烁。
- 上下文缓存、断句、防抖、翻译队列。
- DeepSeek direct / proxy / auto 网络模式。
- DeepSeek 健康检测和网络异常冷却。
- 术语表和翻译风格配置。
- 字幕记录 `subtitleRecords`。
- JSON / TXT / SRT / Markdown 导出。
- Windows 双击启动脚本。
- 可选 PyInstaller exe 启动器。

## 运行环境

- Windows 10 / 11
- Python 3.9+
- Chrome 或 Edge 浏览器
- DeepSeek API Key

## 推荐目录结构

```text
realtime-interpreter/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── translate_service.py
│   ├── websocket_manager.py
│   ├── context_manager.py
│   ├── deepseek_state.py
│   ├── deepseek_network.py
│   └── schemas.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── main.js
├── scripts/
│   ├── build_windows_exe.py
│   └── clean_build.py
├── .env
├── .env.template
├── .gitignore
├── requirements.txt
├── one_click_start_auto.py
├── start_windows.bat
├── stop_windows.bat
├── build_windows.bat
├── README.md
└── RELEASE_NOTES.md
```

## Windows 快速启动

1. 复制 `.env.template` 为 `.env`。
2. 打开 `.env`，填写 `DEEPSEEK_API_KEY`。
3. 双击 `start_windows.bat`。
4. 浏览器会自动打开：

```text
http://127.0.0.1:5500/
```

后端地址：

```text
http://127.0.0.1:8000/
```

## 停止服务

优先方式：

- 在启动窗口按 `Ctrl+C`。

如果端口残留：

- 双击 `stop_windows.bat`，它会尝试关闭占用 8000 和 5500 端口的本地服务。

## .env 配置

`.env` 是你的本地真实配置文件，不要提交到 Git，不要发给别人。

模板：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

DEEPSEEK_NETWORK_MODE=auto
DEEPSEEK_PROXY=
DEEPSEEK_STREAM_ENABLED=false

DEEPSEEK_CONNECT_TIMEOUT=15
DEEPSEEK_TIMEOUT=45
DEEPSEEK_MAX_RETRIES=2
DEEPSEEK_COOLDOWN_SECONDS=30
```

## DeepSeek 网络模式

`DEEPSEEK_NETWORK_MODE` 支持三种模式：

- `direct`：强制直连 DeepSeek，不使用代理。
- `proxy`：强制使用 `DEEPSEEK_PROXY`。
- `auto`：优先直连，失败后尝试代理，并缓存最近成功链路。

国外 / 香港直连推荐：

```env
DEEPSEEK_NETWORK_MODE=direct
DEEPSEEK_PROXY=
DEEPSEEK_STREAM_ENABLED=false
```

国内使用 Clash / Mihomo 推荐：

```env
DEEPSEEK_NETWORK_MODE=proxy
DEEPSEEK_PROXY=http://127.0.0.1:7897
DEEPSEEK_STREAM_ENABLED=false
```

自动模式：

```env
DEEPSEEK_NETWORK_MODE=auto
DEEPSEEK_PROXY=http://127.0.0.1:7897
DEEPSEEK_STREAM_ENABLED=false
```

Clash / Mihomo 常见混合代理端口是 `7890`、`7897` 或用户自定义端口，请以本机客户端配置为准。

## DeepSeek 健康检测

浏览器页面顶部可以点击“检测 DeepSeek 连接”。

也可以直接打开：

```text
http://127.0.0.1:8000/deepseek-health?refresh=true
```

`selected_mode` 表示当前实际使用链路：`direct`、`proxy` 或 `unknown`。

注意：WebSocket 已连接只代表浏览器连到了本地后端，不代表后端一定能访问 DeepSeek。

## 增量同传说明

系统支持 partial 增量翻译：

- 英文 interim 达到阈值后触发 `partial_translate`。
- 第一次 partial 会显示“正在临时翻译...”。
- 同一句后续 partial 更新时，会保留上一版临时中文，不再反复覆盖。
- 新 partial 返回后才更新中文。
- final 翻译回来后会覆盖 partial。
- 如果 final 翻译失败但已有 partial，会保留 partial 并显示重试按钮。

partial 翻译只用于实时显示，不写入正式上下文缓存。final 翻译成功后才更新上下文和导出记录。

## 术语表和翻译风格

页面提供“翻译配置”区域。

术语表格式：

```text
procurement = 采购
inventory planning = 库存计划
supply chain visibility = 供应链可视化
```

翻译风格：

- 默认准确
- 简洁字幕
- 商务会议
- 学术课堂
- 日常口语
- 偏直译

配置保存在浏览器 `localStorage` 中，不会上传到服务器。

## 字幕导出

支持导出：

- JSON
- TXT
- SRT
- Markdown

JSON 会保留 `partialChinese`、`finalChinese`、`hasPartial`、`correctionApplied` 等字段。TXT / SRT / Markdown 默认使用最终中文。

## 可选 exe 启动器

源码版 `start_windows.bat` 是推荐方案。也可以生成 exe 启动器：

1. 双击 `build_windows.bat`。
2. 等待生成：

```text
dist/RealtimeInterpreterLauncher.exe
```

说明：

- exe 只是启动器。
- exe 不包含 `.env`。
- exe 不包含 API Key。
- exe 仍需与 `backend/`、`frontend/`、`requirements.txt`、`.env` 放在同一项目目录中。

清理打包文件：

```powershell
python scripts/clean_build.py
```

## 常见问题

### Python 未安装

安装 Python 3.9+，并勾选 `Add Python to PATH`。

### 8000 / 5500 端口占用

双击 `stop_windows.bat`，或手动关闭占用端口的命令行窗口。

### 麦克风无权限

请在 Chrome / Edge 中允许当前页面访问麦克风，并检查系统麦克风权限。

### 浏览器不支持语音识别

建议使用最新版 Chrome。Web Speech API 在部分浏览器中不可用。

### DeepSeek ConnectError

通常是后端访问 DeepSeek 的网络链路异常。可配置：

```env
DEEPSEEK_NETWORK_MODE=proxy
DEEPSEEK_PROXY=http://127.0.0.1:7897
```

然后打开 `/deepseek-health?refresh=true` 检查。

### API Key 异常

确认 `.env` 中 `DEEPSEEK_API_KEY` 是真实 Key，不是占位符。

### Clash 代理端口不对

查看 Clash / Mihomo 的混合代理端口，常见是 `7890` 或 `7897`。配置必须和本机一致。

### WebSocket 已连接但 DeepSeek 失败

WebSocket 只表示浏览器连接到本地后端。DeepSeek 是否可用要看 `/deepseek-health`。

### 临时翻译和最终翻译不一致

这是正常现象。partial 面对的是不完整英文，final 会根据完整英文重新校正。

## 安全说明

- 不要提交 `.env`。
- 不要把 API Key 发给别人。
- 不要把 API Key 写入前端代码。
- 不要把 `.env` 打包进 exe。

## 后续扩展方向

- 多语言识别和翻译。
- Electron / Tauri 桌面客户端。
- 云端备份。
- 字幕导入。
- 术语表导入导出。
- 本地 Whisper 或其他 ASR 后端。
