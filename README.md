# ISO/IEC 27001知識能力自我挑戰：ISMS Auditor知識測驗

以 `ISO-IEC-27001-Lead-Auditor-CN V15.35.pdf`（368 題）與 `IRCA 模擬試題.pdf`（40 題，排除 3 題重複後收錄 37 題）為題庫的互動練習網站，純靜態 HTML，不需後端。

## 功能

- **練習模式**：依序（記住上次位置）、隨機、未練習、錯題複習、標記題目、配對／排序題專練、情境題專練
- **模擬考試**：自訂題數／時間／及格分數（預設 80 題、180 分鐘、70%），倒數計時、交卷評分、逐題檢討
- **查題**：關鍵字搜尋題幹、選項與解析，或輸入題號直接跳題
- 單選 237 題、複選 132 題（須全對才給分）、配對／排序 36 題（看參考答案後自評）
- **阿拉蕾助教**：首頁問候、每題作答提示（複選題數、否定題型、情境題技巧）、答對／答錯反應、模擬考倒數提醒與成績鼓勵
- **Allan Lo 顧問講解**：每題作答後顯示中文專業講解（引用 ISO/IEC 27001:2022、27002:2022、ISO 19011:2018、ISO/IEC 17021-1 等），模擬考後提供成績檢討；講解資料在 `tools/allan_explanations.json`
- **答案疑義題**：講解時發現題庫答案可能有誤的 43 題，另列練習模式並整理於 `答案疑義清單.md`
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

## 角色素材

`docs/img/chars/` 為由角色設定圖裁切的阿拉蕾與 Allan Lo 表情頭像。顧問講解與助教台詞由 AI 協助撰寫初稿，建議由顧問本人審閱。
