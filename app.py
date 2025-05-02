import streamlit as st
import black # code formatter
import isort # arranged the code
import subprocess
import tempfile # stored tempory data file
import base64  
import re
import random
import plotly.express as px
import ast
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title='Code Formatter and Optimaizer', page_icon='📊', layout='wide')
# @st.cache_data
# def load_lottie_url(url:str):
#     res = requests.get(url)
#     if res.status_code != 200 :
#         return None
#     return res.json
@st.cache_data
def load_lottie_url(url: str):
    res = requests.get(url)
    if res.status_code != 200:
        return None
    return res.json()  # <- Add the parentheses to call the function

animation = load_lottie_url('https://assets10.lottiefiles.com/packages/lf20_j1adxtyb.json')

# st.markdown("""
#           <style>
#             .big-title { text-align: center; font-size: 3em; color:#2575fc; font-weight:bold}
            
#             .subtitle { text-align: center; font-size: 20px; color: #444; font-style:italic;}
            
#             .feature-box {background: linear-gradient(to right, #6a11cb, #2575fc); padding: 15px; border-radius: 8px; color:white; text-align:centre; margin-bottom:20px;}
            
#             .doc-box {background: linear-gradient (to right, #34d399, #10b981); padding: 15px; border-radius:8px; color:black; text-align:center;}
            
#             .score-box {background: linear-gradient (to right, #34d399, #10b981); padding: 10px; border-radius:8px; color:white; text-align:center; font-size: 24px; font-weight:bold;}
            
#             .footer { text-align:center; font-size:14px; color: #aaa; margin-top:40px; }

#             .social-icon img {height:50px;width:25px; margin: 0 5px; vertical-align: middle;}
#             </style>
# """, unsafe_allow_html=True)

st.markdown("""
    <style>
        .big-title {
            text-align: center;
            font-size: 3em;
            color: #2575fc;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #444;
            font-style: italic;
        }
        .feature-box {
            background: linear-gradient(to right, #6a11cb, #2575fc);
            padding: 15px;
            border-radius: 8px;
            color: white;
            text-align: center;
            margin-bottom: 20px;
        }
        .doc-box {
            background: linear-gradient(to right, #34d399, #10b981);
            padding: 15px;
            border-radius: 8px;
            color: black;
            text-align: center;
        }
        .social-icon {
               text-align: center;
                margin-top: 10px;
                  }
        .social-icon a img {
               height:30px;
               width:30px;
               margin: 0 10px;
               transition: transform 0.2s ease-in-out;
}
         .social-icon a img:hover {
                    transform: scale(1.2);
}
        .footer {
            text-align: center;
            font-size: 14px;
            color: #aaa;
            margin-top: 40px;
        }
        .social-icon img {
            height: 50px;
            width: 25px;
            margin: 0 5px;
            vertical-align: middle;
        }
    </style>
""", unsafe_allow_html=True)


col1,col2 = st.columns([2,1])
with col1:
    st.markdown('<div class="big-title">AI-Powered Python Code Formatter & Optimizer 🚀</div>', unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Empower your Python code with AI-Driven formatting, optimization and analyazer</div>", unsafe_allow_html=True)
with col2:
    if animation:
        st_lottie(animation, height=200, speed=1, loop=True)
    else:
        st.warning("⚠️ Failed to load animation")

with st.container():
    st.markdown('<div class ="feature-box"><h2>🔧Feature </h2>   <p> Refactor, Analyzer code , Optimized your give code</p></div>',unsafe_allow_html=True)
    st.markdown('<div class= "doc-box"> <h3> 📕Documentation </h3> <p>Get Stared with AI-driven optimization</p></div>', unsafe_allow_html=True)

    if st.button('🗑️ Clear Code', help='Reset your code: '):
        st.session_state.code_input = ''
    
if 'code_input' not in st.session_state:
    st.session_state.code_input = ''

tabs = st.tabs(['📝Code Input','⚙️ Refactored Output','🎯 Socre Card','📊 Module Graph','✨ Code Optimization Suggestion'])

with tabs[0]:
    code_input = st.text_area('Paste your code here: ', value=st.session_state.code_input, height=200, key='input_code')

def refactored_code(code):
    sorted_code = isort.code(code)
    formatted_code = black.format_file_contents(sorted_code, fast= False, mode=black.Mode())
    with tempfile.NamedTemporaryFile(delete=False, suffix='python', mode='w') as tmp_file:
         tmp_file.write(formatted_code)
         tmp_path = tmp_file.name
    result = subprocess.run(['flake8',tmp_path], capture_output=True, text=True)
    return formatted_code, result.stdout

def count_issues(output):
    return {
        'Unused Imports': len(re.findall(r'unuse-import',output)),
        'Unused Variables': len(re.findall(r'unuse-variable',output)),
        'Undefined Variables': len(re.findall(r'undefined-variable',output)),
    }
def quality_score(issue_count):
    total = sum(issue_count.values())
    return  max(0,100-total*10)

def extract_import(code):
    tree =  ast.parse(code)
    imports = [node.name[0].name for node in tree.body if isinstance(node, ast.Import)]
    return imports

def plot_import_usage(imports):
    import_counts = {imp:imports.count(imp) for imp in set(imports)}
    colors = [f'rgb({random.randint(50,255)}, {random.randint(50,255)})' for _ in import_counts]
    fig = px.bar( x =list(import_counts.keys()), y=list(import_counts.values()),
                 labels = {'x': 'Used Modules', 'y':'Usage Counts'},
                 title = 'Modules Usage', color = list(import_counts.keys()),color_discrete_sequence = colors)
    fig.update_layout(bargrph = 0.3)
    st.plotly_chart(fig, use_container_width=True)

def download_button (code):
    b64 = base64.b64encode(code.encode()).decode()
#     return f"""
#       <div class ='download-btn' style='text-align: center; padding: 10px;'>
#       <a href='data:file/txt;based64{b64}' download = 'refactored.py' style= 'background:linear-gradient(to right, #6a11cb,#2575fc); padding: 12px 20px; border-radius: 8px; color: white; text-align: center; font-weight: bold font-size:18px; text-decoration:none;'>📅 Download Refactored Code </a>
#       </div>
# """
    return f"""
        <div class='download-btn' style='text-align: center; padding: 10px;'>
            <a href='data:file/txt;base64,{b64}' download='refactored.py'
               style='background:linear-gradient(to right, #6a11cb, #2575fc);
                      padding: 12px 20px; border-radius: 8px; color: white;
                      text-align: center; font-weight: bold;
                      font-size:18px; text-decoration:none;'>
                📅 Download Refactored Code
            </a>
        </div>
    """

def optimized_code(code):
    suggestions = []
    if 'for in in range(len(list))' in code:
        suggestions.append('Use "for item in list" instead for "for i in range(len(list))" for better readability.')
    if "== None" in code:
        suggestions.append("Use 'is None' instead of '== None' for better performance and readability.")
    if len(re.findall(r"print\(", code)) > 3:
        suggestions.append("Avoid excessive 'print' statements. Consider logging or using a debugger for better performance.")
    if "for i in range(len(" in code:
        suggestions.append("Consider using 'enumerate()' for cleaner loops, e.g., 'for i, item in enumerate(list):'")
    if "list1 + list2" in code:
        suggestions.append("Avoid concatenating lists inside loops, as it's inefficient. Use 'list.extend()' or 'append()'.")
    if "list.remove(" in code:
        suggestions.append("If you're removing duplicates, consider using 'set()' instead of repeatedly removing elements from a list.")
    if "global " in code:
        suggestions.append("Avoid using 'global' variables. It's better to pass variables as function arguments or return values.")
    if len(re.findall(r"\b[a-z]{1,2}\b", code)) > 5: 
        suggestions.append("Use descriptive variable names instead of single-letter variables (e.g., 'x', 'y').")
    if "open(" in code and "close()" in code:
        suggestions.append("Use 'with open(...) as file' to automatically handle file closing and exceptions.")
    if "if x == None:" in code:
        suggestions.append("Use default arguments instead of manual 'None' checks in function definitions, e.g., 'def func(x=None):'")
    if "lambda " in code and len(re.findall(r"lambda", code)) > 3:
        suggestions.append("Consider replacing redundant lambda functions with regular function definitions.")
    if "list(map(" in code:
        suggestions.append("Consider using list comprehensions instead of 'map()' for better readability and performance.")

    return suggestions

if st.button('⚙️ Refactor Now'):
    if not code_input.strip():
        st.warning('Please paste the code to analyze')
    else:
        cleaned_code, analysis = refactored_code(code_input)

        issues = count_issues(analysis)
        score = quality_score(issues)
        used_imports = extract_import(code_input)

        with tabs[1]:
            st.markdown('### Cleaned And Refactores Code')
            st.code(cleaned_code, language='python')
            st.markdown(download_button(cleaned_code), unsafe_allow_html=True)
        with tabs[2]:
            st.markdown(f'<div class="score-box">📊 Code Quality Score:{score}</div>', unsafe_allow_html=True)
            st.progress(score)
            st.json(issues)
        with tabs[3]:
            if used_imports:
                plot_import_usage(used_imports)
            else:
                st.info('❌ No Module is found in your code.')
        with tabs[4]:
            suggestions = optimized_code(code_input)
            if suggestions:
                st.markdown("### 💡 Code Optimization Suggestions")
                for suggestion in suggestions:
                    st.markdown(f'- {suggestion}')
            else:
                st.info('No optimization suggestion available')

    
# footer
st.markdown("""
<div class = 'footer'>
                RefactorPro &copy; 2025 &mdash; Built with ❤️ by Qirat Saeed <br>
            <br>
            Senior Student
        <div class='social-icons'>
            <a href="https://github.com/qiratsumra"><i class="icon-github">Github</i></a>
            <a href="https://www.linkedin.com/in/qirat-saeed-8048662b7/"></a>
        </div>
            </div>
""", unsafe_allow_html=True)













 # .score-box {
        #     background: linear-gradient(to right, #34d399, #10b981);
        #     padding: 10px;
        #     border-radius: 8px;
        #     color: white;
        #     text-align: center;
        #     font-size: 24px;
        #     font-weight: bold;
        # }
