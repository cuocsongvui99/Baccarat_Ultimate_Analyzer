
import streamlit as st
from collections import Counter

st.set_page_config(page_title="Ultimate Baccarat Analyzer", layout="centered")
st.title("🎯 Ultimate Baccarat Analyzer - Đánh Giá Bàn & Dự Đoán Thông Minh")

st.write("Nhập chuỗi kết quả ván Baccarat (B = Banker, P = Player). Ví dụ: BBPPBPBBP")

input_data = st.text_input("🔤 Kết quả các ván:", "")

# ----------------------------------
def detect_cau_types(results):
    types = []
    streak = 1
    for i in range(1, len(results)):
        if results[i] == results[i - 1]:
            streak += 1
        else:
            if streak >= 3:
                types.append(("Cầu Bệt", results[i - 1], streak))
            streak = 1

    if len(results) >= 4:
        if all(results[-i] != results[-i - 1] for i in range(1, 4)):
            types.append(("Cầu 1-1", "-", 2))

    if len(results) >= 6:
        last6 = results[-6:]
        if last6[0] == last6[1] and last6[2] == last6[3] and last6[4] == last6[5]:
            types.append(("Cầu Dính Kép", "-", 3))

    b = results.count('B')
    p = results.count('P')
    if b / len(results) >= 0.7:
        types.append(("Cầu Nghiêng B", "B", b))
    elif p / len(results) >= 0.7:
        types.append(("Cầu Nghiêng P", "P", p))

    return types

# ----------------------------------
def predict_next(results):
    if len(results) < 4:
        return "Không đủ dữ liệu để dự đoán"

    last = results[-1]
    streak = 1
    for i in range(len(results) - 2, -1, -1):
        if results[i] == last:
            streak += 1
        else:
            break

    if streak >= 3:
        return f"🟢 Dự đoán: tiếp tục {last} (Cầu Bệt)"

    if len(results) >= 4 and results[-1] != results[-2] and results[-2] != results[-3]:
        return f"🟡 Dự đoán: đảo chiều → chọn {'B' if last == 'P' else 'P'} (Cầu 1-1)"

    if results.count('B') / len(results) >= 0.7:
        return "🟡 Dự đoán: Cầu nghiêng B → chọn B"
    elif results.count('P') / len(results) >= 0.7:
        return "🟡 Dự đoán: Cầu nghiêng P → chọn P"

    return "🔴 Không rõ xu hướng, nên chờ thêm"

# ----------------------------------
def score_board(types):
    score = 0
    detail = []
    for t in types:
        if t[0] == "Cầu Bệt":
            score += 3
            detail.append("✅ Cầu Bệt: +3")
        elif t[0] == "Cầu 1-1":
            score += 2
            detail.append("✅ Cầu 1-1: +2")
        elif t[0] == "Cầu Dính Kép":
            score += 2
            detail.append("✅ Cầu Dính Kép: +2")
        elif "Cầu Nghiêng" in t[0]:
            score += 1
            detail.append(f"✅ {t[0]}: +1")

    if score == 0:
        score -= 2
        detail.append("⚠️ Không rõ cầu: -2")

    return score, detail

def classify_score(score):
    if score >= 7:
        return "🟢 BÀN RẤT TỐT - NÊN VÀO TIỀN"
    elif score >= 4:
        return "🟡 BÀN TẠM ỔN - CÂN NHẮC"
    else:
        return "🔴 BÀN RỦI RO - TRÁNH XA"

# ----------------------------------
if input_data:
    results = list(input_data.upper())
    results = [r for r in results if r in ['B', 'P']]

    if len(results) < 6:
        st.warning("⛔ Cần ít nhất 6 kết quả để phân tích.")
    else:
        st.subheader("📊 Phân tích Cầu:")
        types = detect_cau_types(results)
        if types:
            for t in types:
                st.write(f"• {t[0]} ({t[1]}) - {t[2]} lần")
        else:
            st.write("⚠️ Không phát hiện cầu rõ ràng.")

        st.subheader("📈 Thống kê xác suất:")
        counts = Counter(results)
        total = len(results)
        for k in ['B', 'P']:
            pct = counts[k] / total * 100 if k in counts else 0
            st.write(f"{k}: {pct:.2f}%")

        st.subheader("🔮 Dự đoán ván tiếp theo:")
        st.success(predict_next(results))

        st.subheader("🎯 Chấm điểm & Khuyến nghị bàn:")
        score, detail = score_board(types)
        for d in detail:
            st.write(d)
        st.success(f"✅ Tổng điểm: {score} điểm")
        st.markdown(f"### {classify_score(score)}")
