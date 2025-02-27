import sys
sys.path.append('/workspace/packages')  # Cloud Build のパッケージパスを追加

import requests
import pandas as pd
from IPython.display import display  # これが必要ならそのまま

print("✅ Successfully imported requests and pandas!")


# ✅ API のエンドポイント
BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

# ✅ 正しいフィールドリスト（コメントアウトで簡単に制御）
fields_list = [
    "NCTId",
    "BriefTitle",
    "OfficialTitle",  # 基本情報
    "OverallStatus",
    "Phase",  # 試験の状態
    "StartDate",
    "PrimaryCompletionDate",
    "CompletionDate",  # 期間情報
    "EnrollmentCount",
    "EligibilityCriteria",
    "Gender",
    "MinimumAge",
    "MaximumAge",  # 参加条件
    "StudyType",
    "InterventionType",
    "InterventionName",  # 研究タイプ & 介入情報
    "LocationCountry",
    "LocationCity",
    "LocationFacility",  # 実施場所情報
    "HasResults",
    "ResultsFirstPostDate",  # 試験結果情報
    "LeadSponsorName",
    "Collaborator"  # スポンサー情報
]

params = {
    "query.term": "heart disease",
    "pageSize": 10,  # まずは 10 件取得
    "fields": ",".join(fields_list)
}

response = requests.get(BASE_URL, params=params, headers={"Accept": "application/json"})

if response.status_code == 200:
    data = response.json()

    print("📌 APIレスポンスの一部を確認:")
    print(data)  # レスポンスデータ全体を確認

    studies = data.get("studies", [])

    if not studies:
        print("⚠️ 取得データが空です！検索条件を変えて試してください。")
    else:
        extracted_data = []
        for study in studies:
            extracted_data.append({
                "NCTId": study["protocolSection"]["identificationModule"].get("nctId", "N/A"),
                "BriefTitle": study["protocolSection"]["identificationModule"].get("briefTitle", "N/A"),
                "OverallStatus": study["protocolSection"]["statusModule"].get("overallStatus", "N/A"),
                "Phase": study["protocolSection"]["designModule"].get("phases", ["N/A"])[0],  # フェーズはリスト
                "StartDate": study["protocolSection"]["statusModule"].get("startDateStruct", {}).get("date", "N/A"),
                "CompletionDate": study["protocolSection"]["statusModule"].get("completionDateStruct", {}).get("date", "N/A"),
                "EnrollmentCount": study["protocolSection"]["designModule"].get("enrollmentInfo", {}).get("count", "N/A"),
                "LeadSponsorName": study["protocolSection"]["sponsorCollaboratorsModule"]["leadSponsor"].get("name", "N/A"),
            })

        df = pd.DataFrame(extracted_data)
        display(df)

else:
    print(f"❌ APIリクエストエラー: {response.status_code}")
    print(response.text)

print(df.head)  # 取得したデータをそのまま確認

import matplotlib.pyplot as plt

# ステータスごとのカウント
status_counts = df["OverallStatus"].value_counts()

# グラフ作成
plt.figure(figsize=(8, 5))
status_counts.plot(kind="bar")
plt.title("Clinical Trials Status Distribution")
plt.xlabel("Status")
plt.ylabel("Number of Trials")
plt.xticks(rotation=45)
plt.show()


GET /api/query/full_studies


