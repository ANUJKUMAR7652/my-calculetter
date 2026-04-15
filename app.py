import streamlit as st
import sympy as sp
import time
import math
from functools import reduce

# YouTube Shorts Setup
st.set_page_config(layout="centered", page_title="Math AI Mega App")

# --- COMMON CSS FOR VIP UI & LARGE FONTS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1a2e 0%, #0f0f1a 100%); }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container { 
        max-width: 550px; 
        padding-top: 40px !important; 
        margin: auto; 
    }

    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 26, 0.95);
        border-right: 2px solid #ff00cc;
    }

    div[data-testid="stHorizontalBlock"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        align-items: center;
    }

    input {
        text-align: center !important;
        font-size: 35px !important;
        font-weight: bold !important;
        background-color: rgba(0,0,0,0.3) !important;
        border: 2px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    input:focus { border: 2px solid #00ffcc !important; }
    input::-webkit-outer-spin-button, input::-webkit-inner-spin-button {
        -webkit-appearance: none; margin: 0;
    }

    /* 🔥 PERFECTED MATH BOXES (No Empty Spaces) 🔥 */
    .stMath {
        background: rgba(10, 10, 20, 0.8) !important;
        border-left: 8px solid #00f2fe !important;
        border-radius: 20px !important;
        padding: 30px 20px !important; 
        margin-top: 10px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 5px 25px rgba(0, 242, 254, 0.15) !important;
        overflow-x: auto;
        text-align: center;
    }

    .stMath, .katex { font-size: 45px !important; color: #ffffff !important; }

    .calc-heading {
        font-size: 35px; font-weight: bold; color: #00f2fe;
        text-align: center; margin-bottom: 20px;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.4);
    }

    .step-explain {
        font-size: 24px; font-weight: bold; color: #00ffcc;
        margin-top: 25px; margin-bottom: 10px; padding-bottom: 5px;
        border-bottom: 1px dashed rgba(0, 255, 204, 0.3);
    }

    .stButton>button {
        width: 100% !important;
        background: linear-gradient(45deg, #ff00cc, #3333ff);
        color: white; border: none; border-radius: 15px; height: 70px;
        font-size: 26px; font-weight: 900; margin-top: 25px;
        box-shadow: 0 0 25px rgba(255, 0, 204, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# Helper Function for Smart Inputs
def parse_input(val_str, is_denominator=False):
    if val_str.strip() == "": return 1 if is_denominator else 0
    try: return int(val_str)
    except: return 1 if is_denominator else 0

def show_error(msg):
    st.markdown(f"""
    <div style='text-align:center; background: rgba(255,0,0,0.1); padding: 30px; border-radius: 20px; border: 2px solid #ff00cc; margin-top: 30px;'>
        <h1 style='color:#ff00cc; font-size:40px; margin-bottom:10px;'>⚠️ MATH ERROR</h1>
        <p style='color:white; font-size:22px;'>{msg}</p>
    </div>
    """, unsafe_allow_html=True)

def show_loading():
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        bar.progress(i + 1)

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("<h2 style='color:#00ffcc;'>🚀 Tools Menu</h2>", unsafe_allow_html=True)
app_mode = st.sidebar.radio("Choose Calculator:", 
    ["➕ Fraction Solver", "✨ Simplify Fraction", "🔢 LCM & HCF Pro"]
)

# ==========================================
# APP 1: FRACTION SOLVER
# ==========================================
if app_mode == "➕ Fraction Solver":
    st.markdown("<div class='calc-heading'>FRACTION SOLVER PRO</div>", unsafe_allow_html=True)
    
    c1, c_op, c2 = st.columns([2, 1, 2])
    with c1:
        n1_str = st.text_input("n1", value="2", label_visibility="collapsed")
        st.markdown("<hr style='margin:10px 0; border:3px solid #ff00cc;'>", unsafe_allow_html=True)
        d1_str = st.text_input("d1", value="7", label_visibility="collapsed")
    with c_op:
        st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)
        op = st.selectbox("op", ["+", "-", "×", "÷"], label_visibility="collapsed")
    with c2:
        n2_str = st.text_input("n2", value="3", label_visibility="collapsed")
        st.markdown("<hr style='margin:10px 0; border:3px solid #3333ff;'>", unsafe_allow_html=True)
        d2_str = st.text_input("d2", value="8", label_visibility="collapsed")

    if st.button("CALCULATE", use_container_width=True):
        n1, d1 = parse_input(n1_str, False), parse_input(d1_str, True)
        n2, d2 = parse_input(n2_str, False), parse_input(d2_str, True)

        if d1 == 0 or d2 == 0 or (op == "÷" and n2 == 0):
            show_error("Denominator (नीचे की संख्या) <b>Zero (0)</b> नहीं हो सकती।<br>यह Undefined है!")
        else:
            show_loading()
            st.markdown("<div class='calc-heading' style='font-size:28px;'>📝 Calculation Steps</div>", unsafe_allow_html=True)
            
            f1, f2 = sp.Rational(n1, d1), sp.Rational(n2, d2)

            if op in ["+", "-"]:
                lcm_v = sp.lcm(d1, d2)
                m1, m2 = lcm_v // d1, lcm_v // d2
                num1_new, num2_new = n1 * m1, n2 * m2
                res = f1 + f2 if op == "+" else f1 - f2
                op_sign = "+" if op == "+" else "-"
                final_ans = f"{res.p}" if res.q == 1 else rf"\frac{{{res.p}}}{{{res.q}}}"

                st.markdown("<div class='step-explain'>📌 Step 1: LCM निकालकर Base बराबर करें</div>", unsafe_allow_html=True)
                st.latex(rf"\text{{LCM of }} {d1} \text{{ and }} {d2} = {lcm_v}")
                
                st.markdown("<div class='step-explain'>📌 Step 2: Multiply & Solve</div>", unsafe_allow_html=True)
                latex_steps = rf"""
                \begin{{aligned}}
                &\frac{{{n1}}}{{{d1}}} {op_sign} \frac{{{n2}}}{{{d2}}} \\[15pt]
                &= \frac{{{n1} \times {m1}}}{{{d1} \times {m1}}} {op_sign} \frac{{{n2} \times {m2}}}{{{d2} \times {m2}}} \\[15pt]
                &= \frac{{{num1_new}}}{{{lcm_v}}} {op_sign} \frac{{{num2_new}}}{{{lcm_v}}} \\[15pt]
                &= \frac{{{num1_new} {op_sign} {num2_new}}}{{{lcm_v}}} \\[15pt]
                &= {final_ans}
                \end{{aligned}}
                """
                st.latex(latex_steps)

            elif op == "×":
                res = f1 * f2
                final_ans = f"{res.p}" if res.q == 1 else rf"\frac{{{res.p}}}{{{res.q}}}"
                st.markdown("<div class='step-explain'>📌 Step 1: आमने-सामने गुणा करें</div>", unsafe_allow_html=True)
                latex_steps = rf"""
                \begin{{aligned}}
                &\frac{{{n1}}}{{{d1}}} \times \frac{{{n2}}}{{{d2}}} \\[15pt]
                &= \frac{{{n1} \times {n2}}}{{{d1} \times {d2}}} \\[15pt]
                &= \frac{{{n1 * n2}}}{{{d1 * d2}}} \\[15pt]
                &= {final_ans}
                \end{{aligned}}
                """
                st.latex(latex_steps)

            elif op == "÷":
                res = f1 / f2
                final_ans = f"{res.p}" if res.q == 1 else rf"\frac{{{res.p}}}{{{res.q}}}"
                st.markdown("<div class='step-explain'>📌 Step 1: दूसरे Fraction को पलटें (Reciprocal)</div>", unsafe_allow_html=True)
                latex_steps = rf"""
                \begin{{aligned}}
                &\frac{{{n1}}}{{{d1}}} \div \frac{{{n2}}}{{{d2}}} \\[15pt]
                &= \frac{{{n1}}}{{{d1}}} \times \frac{{{d2}}}{{{n2}}} \\[15pt]
                &= \frac{{{n1} \times {d2}}}{{{d1} \times {n2}}} \\[15pt]
                &= \frac{{{n1 * d2}}}{{{d1 * n2}}} \\[15pt]
                &= {final_ans}
                \end{{aligned}}
                """
                st.latex(latex_steps)

# ==========================================
# APP 2: SIMPLIFY FRACTION
# ==========================================
elif app_mode == "✨ Simplify Fraction":
    st.markdown("<div class='calc-heading'>SIMPLIFY PRO</div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)
        w_str = st.text_input("Whole", value="2", label_visibility="collapsed")
    with c2:
        n_str = st.text_input("Num", value="21", label_visibility="collapsed")
        st.markdown("<hr style='margin:15px 0; border:4px solid #fff;'>", unsafe_allow_html=True)
        d_str = st.text_input("Den", value="98", label_visibility="collapsed")

    if st.button("SIMPLIFY", use_container_width=True):
        w, n, d = parse_input(w_str, False), parse_input(n_str, False), parse_input(d_str, True)
        
        if d == 0:
            show_error("Denominator <b>Zero (0)</b> नहीं हो सकता!")
        else:
            show_loading()
            st.markdown("<div class='calc-heading' style='font-size:28px;'>📝 Simplification Steps</div>", unsafe_allow_html=True)

            improper_num = (w * d) + n
            gcd_val = math.gcd(improper_num, d)
            s_num, s_den = improper_num // gcd_val, d // gcd_val

            if w > 0:
                st.markdown("<div class='step-explain'>📌 Step 1: Mixed से Improper में बदलें</div>", unsafe_allow_html=True)
                step1 = rf"""
                \begin{{aligned}}
                &{w} \frac{{{n}}}{{{d}}} \\[15pt]
                &= \frac{{{w} \times {d} + {n}}}{{{d}}} \\[15pt]
                &= \frac{{{improper_num}}}{{{d}}}
                \end{{aligned}}
                """
                st.latex(step1)
            else:
                st.markdown("<div class='step-explain'>📌 Original Fraction</div>", unsafe_allow_html=True)
                st.latex(rf"\frac{{{improper_num}}}{{{d}}}")

            if gcd_val > 1:
                st.markdown("<div class='step-explain'>📌 Step 2: HCF से भाग देकर सरल करें</div>", unsafe_allow_html=True)
                st.latex(rf"\text{{HCF of }} {improper_num} \text{{ and }} {d} = {gcd_val}")
                step2 = rf"""
                \begin{{aligned}}
                &= \frac{{{improper_num} \div {gcd_val}}}{{{d} \div {gcd_val}}} \\[15pt]
                &= \frac{{{s_num}}}{{{s_den}}}
                \end{{aligned}}
                """
                st.latex(step2)
            else:
                st.markdown("<div class='step-explain'>📌 Step 2: Fraction पहले से सरल है</div>", unsafe_allow_html=True)

            if s_num > s_den and s_den > 1:
                st.markdown("<div class='step-explain'>📌 Step 3: Final Mixed Answer</div>", unsafe_allow_html=True)
                st.latex(rf"= {s_num // s_den} \frac{{{s_num % s_den}}}{{{s_den}}}")
            elif s_den == 1:
                st.markdown("<div class='step-explain'>📌 Step 3: Final Whole Answer</div>", unsafe_allow_html=True)
                st.latex(rf"= {s_num}")

# ==========================================
# APP 3: LCM & HCF
# ==========================================
elif app_mode == "🔢 LCM & HCF Pro":
    st.markdown("<div class='calc-heading'>LCM & HCF CALCULATOR</div>", unsafe_allow_html=True)
    
    st.markdown("<p style='color:white; text-align:center;'>Enter Numbers (Comma separated):</p>", unsafe_allow_html=True)
    nums_str = st.text_input("Nums", value="12, 15, 75", label_visibility="collapsed")
    
    if st.button("FIND LCM & HCF", use_container_width=True):
        try:
            nums = [int(x.strip()) for x in nums_str.split(",")]
            def lcm(a, b): return abs(a*b) // math.gcd(a, b)
            lcm_res = reduce(lcm, nums)
            hcf_res = reduce(math.gcd, nums)
            
            show_loading()
            
            st.latex(rf"""
            \begin{{aligned}}
            \text{{LCM}} &= {lcm_res} \\[20pt]
            \text{{HCF}} &= {hcf_res}
            \end{{aligned}}
            """)

            st.markdown("<div class='calc-heading' style='font-size:28px; margin-top:30px;'>🧬 Prime Factorization</div>", unsafe_allow_html=True)
            
            # 🔥 THE "imes" BUG IS FIXED HERE 🔥
            times_symbol = r" \times "
            for n in nums:
                factors = []
                d = 2
                temp = n
                while d * d <= temp:
                    while temp % d == 0:
                        factors.append(str(d))
                        temp //= d
                    d += 1
                if temp > 1:
                    factors.append(str(temp))
                
                st.latex(rf"{n} = {times_symbol.join(factors)}")
                
        except:
            show_error("Please enter valid comma-separated numbers! (e.g. 12, 15)")
