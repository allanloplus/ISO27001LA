# ISO/IEC 27001 Lead Auditor 學習測驗網站

以 `ISO-IEC-27001-Lead-Auditor-CN V15.35.pdf`（368 題）與 `IRCA 模擬試題.pdf`（40 題，排除 3 題重複後收錄 37 題）為題庫的互動練習網站，純靜態 HTML，不需後端。

## 功能

- **練習模式**：依序（記住上次位置）、隨機、未練習、錯題複習、標記題目、情境題專練
- **模擬考試**：自訂題數／時間／及格分數（預設 80 題、180 分鐘、70%），倒數計時、交卷評分、逐題檢討
- **查題**：關鍵字搜尋題幹、選項與解析，或輸入題號直接跳題
- 單選 237 題、複選 132 題（須全對才給分）、配對／排序 36 題（看參考答案後自評）
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

`IRCA 模擬試題.pdf` 為投影片截圖，無法直接擷取文字，題目已人工轉錄於 `tools/irca_questions.json`，
原始投影片圖片為 `docs/img/irca_XX.jpg`。標記 `duplicateOf` 的題目與 V15.35 重複，建置時會略過：

| IRCA 題號 | 重複的 V15.35 題號 |
|---|---|
| 11（稽核資訊收集流程排序） | 189 |
| 12（稽核員個人特質配對） | 261 |
| 28（外部議題，選四項） | 212 |
