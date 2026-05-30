# Release Notes

## v1.0.0-local

本版本是个人本地实时同声传译工具的首个完整本地封装版本。

### 核心功能

- 浏览器 Web Speech API 英语实时识别。
- 英文 interim / final 字幕展示。
- DeepSeek API 中文翻译。
- WebSocket 实时通信与 HTTP `/translate` fallback。
- partial 增量翻译与 final 最终校正。
- partial 翻译保留机制，避免长句翻译时中文区域闪烁。
- 上下文缓存、断句、防抖和翻译队列。
- DeepSeek direct / proxy / auto 网络模式。
- DeepSeek 健康检测与网络异常冷却。
- 术语表和翻译风格配置。
- 字幕记录 `subtitleRecords`。
- JSON / TXT / SRT / Markdown 导出。
- Windows 双击启动脚本。
- 可选 PyInstaller 启动器打包。

### 当前限制

- 语音识别依赖 Chrome / Edge 浏览器的 Web Speech API。
- 当前只做英语语音识别到中文翻译。
- DeepSeek API Key 由用户自行申请并配置。
- 本版本不包含数据库、用户账户、云端同步或音频文件上传。
- PyInstaller 方案只打包启动器，不把后端、前端和 `.env` 合并进 exe。

### 已知问题

- Web Speech API 在部分浏览器或网络环境下可用性不稳定。
- 长句 partial 翻译可能与 final 翻译不一致，这是增量同传的正常现象。
- 如果 Clash / Mihomo 端口配置错误，DeepSeek 健康检测会失败。
- 如果 8000 或 5500 端口被占用，需要运行 `stop_windows.bat` 或手动关闭占用进程。

### 后续可扩展方向

- 多语言识别和多语言翻译。
- 桌面客户端封装，例如 Electron 或 Tauri。
- 云端备份和历史记录管理。
- 字幕导入、术语表导入导出。
- 本地 Whisper / 云端 ASR 可选后端。
- 更细粒度的专业领域提示词和术语管理。
