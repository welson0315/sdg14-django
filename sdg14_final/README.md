# SDGs 14 海洋保育教育網站 (Ocean Conservation Education Platform)

本專案是一款專為 **聯合國永續發展目標 SDGs 14：水下生物 (Life Below Water)** 設計的網頁教育平台。系統結合 Python Django 後端框架與自動化爬蟲技術，提供即時海洋保育快訊、互動式物種圖鑑、會員收藏及知識測驗等功能。

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&style=for-the-badge)
![Django](https://img.shields.io/badge/Django-5.0-green?logo=django&style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?logo=sqlite&style=for-the-badge)

---

## 🌟 核心功能
* **即時海洋保育快訊**：透過 `BeautifulSoup` 自動擷取海保署官網最新公告，並具備異常連線防護機制。
* **最新海洋圖鑑**：響應式 CSS Grid 排版，動態呈現保育物種詳細資料。
* **互動式會員系統**：支援文章收藏、個人化追蹤與留言互動。
* **海洋知識測驗**：內建題庫與即時評分機制，提升學習互動性。

## 🛠️ 技術架構
* **前端**：Django Templates, HTML5, CSS3 (Flexbox/Grid)
* **後端**：Django Framework
* **爬蟲**：Requests, BeautifulSoup4
* **資料庫**：SQLite 3

## 💻 快速安裝指南 (給展示評分用)
若需在全新電腦（如學校展示機）執行本專案，請打開終端機 (CMD) 並執行以下步驟：

### 1. 建立並啟動環境
```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境 (Windows)
.venv\Scripts\activate

### 2. 安裝依賴套件
安裝 `requirements.txt` 中紀錄的所有必要套件（包含 Django, Pillow, BeautifulSoup4 等）：
```bash
pip install -r requirements.txt

### 2. 更新 🌟 核心功能 (加入通報系統)

```markdown
* **海洋觀測與污染通報**：提供前端表單與圖片上傳功能 (`Pillow`)，讓使用者能即時通報污染事件，並於後台/紀錄頁面動態渲染。
