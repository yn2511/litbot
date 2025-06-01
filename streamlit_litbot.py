import streamlit as st
import docx
from datetime import datetime
import os
import re
import uuid

# 박서련 「나, 나, 마들렌」 원문 불러오기
with open("나, 나, 마들렌_박서련.txt", "r", encoding="utf-8") as f:
    novel_text = f.read()

# Claude API 응답 더미

def dummy_claude_response(prompt):
    return "(예시 답변) 그 장면에 집중한 게 흥미롭네! 왜 그렇게 생각했는지 궁금해."

# 안전한 파일명 생성 함수
def sanitize_filename(filename):
    name, ext = os.path.splitext(filename)
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    return f"{safe_name}_{uuid.uuid4().hex[:6]}{ext}"

# 텍스트 추출 함수 (인코딩 대응 포함)
def extract_text(file):
    if file.name.endswith(".txt"):
        try:
            return file.getvalue().decode("utf-8")
        except UnicodeDecodeError:
            return file.getvalue().decode("cp949")
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

# 대화 로그 저장
def save_log(user_input, bot_response, log_file="chat_log.txt"):
    with open(log_file, "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}]\nYou: {user_input}\nClaude: {bot_response}\n\n")

# UI
st.title("📚 문학 챗봇 \n - 박서련 『나, 나, 마들렌』을 읽고 챗 봇과 대화해보아요!")

st.markdown("---")
st.markdown("### 1. 감상문 업로드 (.txt, .docx)")
st.markdown("⚠️ **파일명은 반드시 영문과 숫자로만 구성해주세요.** 한글, 공백, 특수문자는 오류를 유발할 수 있습니다.")
review_file = st.file_uploader("감상문을 업로드해주세요", type=["txt", "docx"])

review_text = ""
if review_file is not None:
    safe_name = sanitize_filename(review_file.name)
    review_text = extract_text(review_file)
    st.success(f"감상문 업로드 완료! (저장명: {safe_name})")
    st.text_area("📄 감상문 미리보기", review_text, height=150)

st.markdown("---")
st.markdown("### 2. Claude와 문학 토론")

if review_text:
    user_input = st.text_input("💬 Claude에게 질문해보세요")

    if user_input:
        # 프롬프트 구성
        prompt = f"소설 원문:\n{novel_text}\n\n감상문:\n{review_text}\n\n사용자 질문:\n{user_input}"
        response = dummy_claude_response(prompt)

        st.markdown(f"**🧑 You:** {user_input}")
        st.markdown(f"**🤖 Claude:** {response}")
        save_log(user_input, response)
else:
    st.info("먼저 감상문을 업로드해주세요.")

st.markdown("---")
st.markdown("### 3. 성찰일지 업로드 (.txt, .docx)")
st.markdown("⚠️ **파일명은 반드시 영문과 숫자로만 구성해주세요.** 한글, 공백, 특수문자는 오류를 유발할 수 있습니다.")
reflection_file = st.file_uploader("성찰일지를 업로드해주세요", type=["txt", "docx"], key="reflection")

if reflection_file is not None:
    reflection_text = extract_text(reflection_file)
    safe_reflection_name = sanitize_filename(reflection_file.name)
    st.success(f"성찰일지 업로드 완료! (저장명: {safe_reflection_name})")
    with open("reflection.txt", "w", encoding="utf-8") as f:
        f.write(reflection_text)
    st.text_area("📔 성찰일지 미리보기", reflection_text, height=150)
