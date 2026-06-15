def build_vip_system_prompt() -> str:
    return """
你是渡假村 VIP 專屬推薦助理。

你的任務是根據客戶入住資訊、住宿資訊，以及渡假村知識庫候選資料，產生個人化 VIP 行程推薦。

重要規則：
- 不得捏造知識庫中不存在的設施、服務、餐廳或景點。
- 行程只能使用「渡假村知識庫候選資料」中的 recommendations。
- 每一天都要依照入住日期產生行程。
- 每個時段只能從該時段 recommendations 中選出最適合的一筆。
- 同一天不要重複安排相同景點或餐廳。
- 若客戶沒有停車需求，不要主動推薦停車、接駁、代客泊車或行李服務。
- 語氣需符合高級渡假村服務風格，親切但正式。

請輸出 JSON，不要輸出 Markdown。
""".strip()

def build_vip_user_prompt(
    data: dict,
    stay_notes: list,
    knowledge_context: str,
) -> str:
    notes_text = "、".join(
        f"{note['NoteType']}：{note['NoteContent']}"
        for note in stay_notes
    )
    return f"""
請根據以下客戶資料與渡假村知識庫候選資料，產生 VIP 個人化入住行程。

客戶入住資訊：
- 姓名：{data["full_name"]}
- 性別：{data["gender_name"]}
- 年齡：{data["age"]} 歲
- 國籍：{data["country_name"]}

住宿資訊：
- 入住日期：{data["check_in_date"]}
- 入住天數：{data["stay_days"]} 天
- 房型：{data["room_type_name"]}
- 總人數：{data["total_count"]} 人
- 是否有停車：{data["has_parking"]}

特殊備註：
{notes_text}

渡假村知識庫候選資料：
{knowledge_context}

請產生以下 JSON 格式：

{{
  "summary": "請用高級渡假村服務語氣，簡短說明本次推薦重點",
  "itinerary": [
    {{
      "date": "YYYY-MM-DD",
      "schedules": [
        {{
          "time": "09:00",
          "title": "從該時段 recommendations 選出的名稱",
          "content": "說明為什麼適合這位客戶",
          "preference": "分類",
          "source_type": "knowledge_base"
        }}
      ]
    }}
  ],
  "vip_services": [
    {{
      "title": "VIP服務名稱",
      "content": "服務說明"
    }}
  ],
  "notes": [
    "注意事項"
  ]
}}

限制：
- itinerary 的 date 必須來自知識庫候選資料中的 date。
- schedules 的 time 必須來自知識庫候選資料中的 time。
- title 必須來自該時段 recommendations 裡的 title。
- preference 必須來自該筆 recommendations 裡的 preference。
- 如果某個時段 recommendations 是空陣列，該時段可以略過。
- 不要新增知識庫沒有提供的景點、餐廳或設施。
""".strip()