
import os
import time
import requests
import streamlit as st

st.set_page_config(page_title="2024디딤돌R&D", layout="wide")

# ----------------------
# 설정
# ----------------------
N8N_BASE = st.secrets.get("N8N_BASE_URL")
# 토큰 기반 인증을 쓰고 있다면 secrets에 N8N_TOKEN을 넣고, 헤더에 추가하세요.
N8N_TOKEN = st.secrets.get("N8N_TOKEN")

def post_form(url: str, form: dict):
    headers = {}
    if N8N_TOKEN:
        headers["Authorization"] = f"Bearer {N8N_TOKEN}"
    started = time.time()
    try:
        # n8n webhook은 보통 form-data/x-www-form-urlencoded 모두 허용됩니다.
        # 기본은 application/x-www-form-urlencoded로 전송합니다.
        resp = requests.post(url, data=form, headers=headers, timeout=30)
        took = int((time.time() - started) * 1000)
        ok = resp.status_code >= 200 and resp.status_code < 300
        return {
            "ok": ok,
            "status_code": resp.status_code,
            "elapsed_ms": took,
            "url": url,
            "request_form": form,
            "response_text": resp.text,
            "response_json": try_json(resp)
        }
    except Exception as e:
        return {
            "ok": False,
            "status_code": None,
            "elapsed_ms": int((time.time() - started) * 1000),
            "url": url,
            "request_form": form,
            "error": str(e),
        }

def try_json(resp):
    try:
        return resp.json()
    except Exception:
        return None

# ----------------------
# UI
# ----------------------
st.title("2024디딤돌R&D")
st.caption("사이드 바에서 서비스를 선택하세요. 각 서비스는 워크플로우를 호출합니다.")
# 사이드바에서 서비스 선택 (페이지네이션 방식)
with st.sidebar:
  st.header("🚀 서비스 메뉴")
  
  # 서비스 목록
  services = [
    ("📬", "gmail", "Gmail"),
    ("📄", "gdocs", "Google Docs"),
    ("📆", "gcalendar", "Google Calendar"),
    ("🌐", "translate", "Google Translate"),
    ("⏱️", "time", "Time"),
    ("📰", "rss", "RSS"),
    ("💬", "slack", "Slack"),
    ("🧠", "ai", "AI"),
  ]
  
  # 세션 상태에서 현재 선택된 서비스 저장
  if "selected_service" not in st.session_state:
    st.session_state.selected_service = "gmail"
  
  # 각 서비스를 버튼으로 표시
  for emoji, service_id, service_name in services:
    if st.button(
      f"{emoji} {service_name}",
      key=f"nav_{service_id}",
      use_container_width=True,
      type="primary" if st.session_state.selected_service == service_id else "secondary"
    ):
      st.session_state.selected_service = service_id
      st.rerun()
  
  # 현재 선택된 서비스 변수에 할당
  service = st.session_state.selected_service
  
  st.divider()
  st.caption(f"현재 선택: **{service}**")

# ----------------------
# 서비스별 폼
# ----------------------

def ui_gmail():
    st.subheader("📬 Gmail")
    tab1, tab2, tab3, tab4 = st.tabs(["get_many", "get", "send", "reply"])

    with tab1:
        st.markdown("**메일 목록 가져오기**")
        if st.button("실행", key="gmail_get_many_btn"):
            out = post_form(f"{N8N_BASE}/gmail/get_many", {})
            st.json(out)

    with tab2:
        st.markdown("**메일 단건 조회**")
        id_ = st.text_input("id", placeholder="예: 1929ej3115a3beb", key="gmail_get_id")
        if st.button("실행", key="gmail_get_btn"):
            out = post_form(f"{N8N_BASE}/gmail/get", {"id": id_})
            st.json(out)

    with tab3:
        st.markdown("**메일 발송**")
        email = st.text_input("email", placeholder="수신자 이메일")
        title = st.text_input("title", placeholder="제목")
        text = st.text_area("text", placeholder="본문 내용")
        if st.button("실행", key="gmail_send_btn"):
            out = post_form(f"{N8N_BASE}/gmail/send", {"email": email, "title": title, "text": text})
            st.json(out)

    with tab4:
        st.markdown("**답장**")
        id_ = st.text_input("id", placeholder="원본 메일 id", key="gmail_reply_id")
        text = st.text_area("text", placeholder="답장 내용")
        if st.button("실행", key="gmail_reply_btn"):
            out = post_form(f"{N8N_BASE}/gmail/reply", {"id": id_, "text": text})
            st.json(out)

def ui_gdocs():
    st.subheader("📄 Google Docs")
    tab1, tab2, tab3 = st.tabs(["create", "get", "update"])

    with tab1:
        st.markdown("**문서 생성**")
        title = st.text_input("title", placeholder="문서 제목")
        if st.button("실행", key="gdocs_create_btn"):
            out = post_form(f"{N8N_BASE}/gdocs/create", {"title": title})
            st.json(out)

    with tab2:
        st.markdown("**문서 조회**")
        id_ = st.text_input("id", placeholder="문서 ID", key="gdocs_get_id")
        if st.button("실행", key="gdocs_get_btn"):
            out = post_form(f"{N8N_BASE}/gdocs/get", {"id": id_})
            st.json(out)

    with tab3:
        st.markdown("**문서 업데이트(본문 추가/치환 등)**")
        id_ = st.text_input("id", placeholder="문서 ID", key="gdocs_update_id")
        text = st.text_area("text", placeholder="추가/치환할 내용")
        if st.button("실행", key="gdocs_update_btn"):
            out = post_form(f"{N8N_BASE}/gdocs/update", {"id": id_, "text": text})
            st.json(out)

def ui_gcalendar():
    st.subheader("📆 Google Calendar")
    tab1, tab2, tab3, tab4 = st.tabs(["get_many", "get", "create", "delete"])

    with tab1:
        st.markdown("**이벤트 목록 조회**")
        if st.button("실행", key="gc_get_many_btn"):
            out = post_form(f"{N8N_BASE}/gc/get_many", {})
            st.json(out)

    with tab2:
        st.markdown("**이벤트 단건 조회**")
        event_id = st.text_input("event_id", placeholder="이벤트 ID")
        if st.button("실행", key="gc_get_btn"):
            out = post_form(f"{N8N_BASE}/gc/get", {"event_id": event_id})
            st.json(out)

    with tab3:
        st.markdown("**이벤트 생성**")
        start = st.text_input("start (ISO8601)", placeholder="예: 2025-08-14T22:00:00+09:00")
        end = st.text_input("end (ISO8601)", placeholder="예: 2025-08-14T23:00:00+09:00")
        text = st.text_input("text", placeholder="이벤트 제목/내용")
        if st.button("실행", key="gc_create_btn"):
            out = post_form(f"{N8N_BASE}/gc/create", {"start": start, "end": end, "text": text})
            st.json(out)

    with tab4:
        st.markdown("**이벤트 삭제**")
        event_id = st.text_input("event_id", placeholder="이벤트 ID", key="gc_delete_id")
        if st.button("실행", key="gc_delete_btn"):
            out = post_form(f"{N8N_BASE}/gc/delete", {"event_id": event_id})
            st.json(out)

def ui_translate():
    st.subheader("🌐 Translate")
    tab1, tab2, tab3, tab4 = st.tabs(["kr", "en", "cn", "jp"])
    text = st.text_area("text", placeholder="번역할 텍스트", key="tr_text")

    with tab1:
        if st.button("한국어로 번역", key="tr_kr_btn"):
            out = post_form(f"{N8N_BASE}/translate/kr", {"text": text})
            st.json(out)

    with tab2:
        if st.button("영어로 번역", key="tr_en_btn"):
            out = post_form(f"{N8N_BASE}/translate/en", {"text": text})
            st.json(out)

    with tab3:
        if st.button("중국어로 번역", key="tr_cn_btn"):
            out = post_form(f"{N8N_BASE}/translate/cn", {"text": text})
            st.json(out)

    with tab4:
        if st.button("일본어로 번역", key="tr_jp_btn"):
            out = post_form(f"{N8N_BASE}/translate/jp", {"text": text})
            st.json(out)

def ui_time():
    st.subheader("⏱️ Time")
    tab1, tab2, tab3 = st.tabs(["now", "between", "add"])

    with tab1:
        st.markdown("**현재 시간(now)**")
        if st.button("실행", key="time_now_btn"):
            out = post_form(f"{N8N_BASE}/time/now", {})
            st.json(out)

    with tab2:
        st.markdown("**두 날짜 사이(between)**")
        start = st.text_input("start", placeholder="예: 2019.01.01")
        end = st.text_input("end", placeholder="예: 2020.01.01")
        if st.button("실행", key="time_between_btn"):
            out = post_form(f"{N8N_BASE}/time/between", {"start": start, "end": end})
            st.json(out)

    with tab3:
        st.markdown("**날짜에 일수 더하기(add)**")
        date = st.text_input("date", placeholder="예: 2019.01.01")
        add_days = st.text_input("add_days", placeholder="예: 200")
        if st.button("실행", key="time_add_btn"):
            out = post_form(f"{N8N_BASE}/time/add", {"date": date, "add_days": add_days})
            st.json(out)

def ui_rss():
    st.subheader("📰 RSS")
    tab1, tab2, tab3, tab4 = st.tabs(["jtbc", "sbs", "yh", "read"])

    with tab1:
        if st.button("JTBC", key="rss_jtbc_btn"):
            out = post_form(f"{N8N_BASE}/rss/jtbc", {})
            st.json(out)

    with tab2:
        if st.button("SBS", key="rss_sbs_btn"):
            out = post_form(f"{N8N_BASE}/rss/sbs", {})
            st.json(out)

    with tab3:
        if st.button("연합뉴스", key="rss_yh_btn"):
            out = post_form(f"{N8N_BASE}/rss/yh", {})
            st.json(out)

    with tab4:
        url = st.text_input("RSS URL", placeholder="예: https://news-ex.jtbc.co.kr/v1/get/rss/newsflesh")
        # https://news-ex.jtbc.co.kr/v1/get/rss/newsflesh 그대로 사용하는 버튼 
        button_label = "읽기 (기본 URL)"
        if st.button(button_label, key="rss_read_btn"):
            out = post_form(f"{N8N_BASE}/rss/read", {"url": url if url else "https://news-ex.jtbc.co.kr/v1/get/rss/newsflesh"})
            st.json(out)

def ui_slack():
    st.subheader("💬 Slack")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["send", "remove", "get", "reaction", "remove_reaction", "user_list",])

    with tab1:
      channel_id = st.text_input("channel_id", value="", placeholder="예: C099U6GK6DR", key="slack_send_channel")
      text = st.text_input("text", value="", placeholder="예: 안녕하세요", key="slack_send_text")
      if st.button("실행", key="slack_send_btn"):
          out = post_form(f"{N8N_BASE}/slack/send", {"channel_id": channel_id, "text": text})
          st.json(out)


    with tab2:
        channel_id = st.text_input("channel_id", value="", placeholder="예: C099U6GK6DR", key="slack_remove_msg_channel")
        message_timestamp = st.text_input("message_timestamp", value="", placeholder="예: 1755020881.314499", key="slack_remove_msg_ts")
        if st.button("실행", key="slack_remove_msg_btn"):
            out = post_form(f"{N8N_BASE}/slack/remove_message", {
                "channel_id": channel_id,
                "message_timestamp": message_timestamp
            })
            st.json(out)


    with tab3:
        channel_id = st.text_input("channel_id", value="", placeholder="예: C099U6GK6DR", key="slack_get_channel")
        if st.button("실행", key="slack_get_btn"):
            out = post_form(f"{N8N_BASE}/slack/get", {"channel_id": channel_id})
            st.json(out)

    with tab4:
        channel_id = st.text_input("channel_id", value="", placeholder="예: C099U6GK6DR", key="slack_react_channel")
        message_timestamp = st.text_input("message_timestamp", value="", placeholder="예: 1755020881.314499")
        if st.button("실행", key="slack_react_btn"):
            out = post_form(f"{N8N_BASE}/slack/reaction", {
                "channel_id": channel_id,
                "message_timestamp": message_timestamp
            })
            st.json(out)

    with tab5:
        channel_id = st.text_input("channel_id", value="", placeholder="예: C099U6GK6DR", key="slack_remove_channel")
        message_timestamp = st.text_input("message_timestamp", value="", placeholder="예: 1755020881.314499", key="slack_remove_ts")
        if st.button("실행", key="slack_remove_btn"):
            out = post_form(f"{N8N_BASE}/slack/remove_reaction", {
                "channel_id": channel_id,
                "message_timestamp": message_timestamp
            })
            st.json(out)

    with tab6:
        if st.button("사용자 목록 가져오기", key="slack_user_list_btn"):
            out = post_form(f"{N8N_BASE}/slack/user_list", {})
            st.json(out)


def ui_ai():
    st.subheader("🧠 AI")
    tab1, tab2 = st.tabs(["summary", "check"])

    with tab1:
        text = st.text_area("text", placeholder="요약할 텍스트")
        if st.button("실행", key="ai_summary_btn"):
            out = post_form(f"{N8N_BASE}/ai/summary", {"text": text})
            st.json(out)

    with tab2:
        text = st.text_area("text", placeholder="사실 검증/체크할 텍스트")
        if st.button("실행", key="ai_check_btn"):
            out = post_form(f"{N8N_BASE}/ai/check", {"text": text})
            st.json(out)

# 라우팅
if service == "gmail":
    ui_gmail()
elif service == "gdocs":
    ui_gdocs()
elif service == "gcalendar":
    ui_gcalendar()
elif service == "translate":
    ui_translate()
elif service == "time":
    ui_time()
elif service == "rss":
    ui_rss()
elif service == "slack":
    ui_slack()
elif service == "ai":
    ui_ai()

# with st.expander("⚙️ 설정/도움말", expanded=False):
#     st.markdown(
#         """
#         **환경변수/시크릿**
#         - `.streamlit/secrets.toml` 에 다음 값을 넣어주세요:
#         ```toml
#         N8N_BASE_URL = "https://example.com/webhook"
#         # 필요 시
#         # N8N_TOKEN = "YOUR_EXAMPLE_TOKEN"
#         ```
#         - 인증이 필요한 경우, n8n Webhook에 토큰 검증 로직을 추가하고 본 앱에서 `Authorization: Bearer <TOKEN>` 헤더로 보냅니다.

#         **요청 전송 형식**
#         - 기본적으로 `application/x-www-form-urlencoded` 로 전송합니다.
#         - n8n에서 반드시 `multipart/form-data`가 필요하다면 `requests.post(..., files=...)` 방식으로 전환하세요.
#         """
#     )
