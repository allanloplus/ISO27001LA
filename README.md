# ISO/IEC 27001 Lead Auditor 學習測驗網站

以 `ISO-IEC-27001-Lead-Auditor-CN V15.35.pdf`（368 題）為題庫的互動練習網站，純靜態 HTML，不需後端。

## 功能

- **練習模式**：依序（記住上次位置）、隨機、未練習、錯題複習、標記題目、情境題專練
- **模擬考試**：自訂題數／時間／及格分數（預設 80 題、180 分鐘、70%），倒數計時、交卷評分、逐題檢討
- **查題**：關鍵字搜尋題幹、選項與解析，或輸入題號直接跳題
- 單選 229 題、複選 106 題（須全對才給分）、拖曳配對 33 題（以原始圖片呈現，看參考答案後自評）
- 作答紀錄、錯題本與標記存在瀏覽器 localStorage
- 鍵盤操作：`A`–`H` 選擇、`Enter` 確認／下一題、`←` `→` 切換
- 支援手機版面與深色模式

## 使用方式

- 本機：直接用瀏覽器開啟 `docs/index.html`
- GitHub Pages：Settings → Pages → Source 選 `Deploy from a branch`，Branch 選 `main`、資料夾 `/docs`

## 重新產生題庫

```bash
pip install pymupdf
python3 tools/parse_pdf.py "ISO-IEC-27001-Lead-Auditor-CN V15.35.pdf" docs
```

產出 `docs/questions.json`、`docs/questions.js` 與 `docs/img/`（題目圖片）。
