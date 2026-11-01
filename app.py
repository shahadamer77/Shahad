import streamlit as st
import hashlib
import urllib.request
import re

st.set_page_config(page_title="فاحص أمان كلمات المرور", page_icon="🔒", layout="centered")

st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🔒 فاحص أمان كلمات المرور</h2>", unsafe_allow_html=True)
st.write("---")

password = st.text_input("أدخل كلمة المرور للفحص:", type="password")

if password:
    score = 0
    feedback = []
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ الطول قصير جداً (يُفضل 8 أحرف أو أكثر).")
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ يجب أن تحتوي على حروف كبيرة وصغيرة مختلطة.")
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ يجب أن تحتوي على أرقام.")
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("❌ يجب أن تحتوي على رموز خاصة.")

    st.write(f"**تقييم القوة:** {score} / 4")
    for note in feedback:
        st.write(note)
    if not feedback:
        st.success("كلمة المرور قوية جداً ومعقدة! ✅")

    st.write("---")
    
    sha1_pwd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_pwd[:5]
    suffix = sha1_pwd[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Python-Security-Tool'})
        with urllib.request.urlopen(req) as response:
            res_text = response.read().decode('utf-8')
            found = False
            for line in res_text.splitlines():
                hash_suffix, count = line.split(':')
                if hash_suffix == suffix:
                    st.error(f"⚠️ تحذير خطير! ظهرت كلمة المرور في التسريبات العالمية **{count}** مرة!")
                    found = True
                    break
            if not found:
                st.success("🎉 ممتاز! كلمة المرور نظيفة ولم تسرب أبداً في أي قاعدة بيانات مخترقة.")
    except Exception as e:
        st.error(f"خطأ في الاتصال بالإنترنت: {e}")
