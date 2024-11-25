import streamlit as st
import pandas as pd

# 航司列表
airlines = [
    "海南航空", "大新华航空", "乌鲁木齐航空", "首都航空",
    "北部湾航空", "桂林航空", "祥鹏航空", "福州航空",
    "天津航空", "金鹏航空", "长安航空", "西部航空"
]

# 定义需要统计的公司列表
target_companies = [
    "海航航空技术有限公司",
    "海航航空技术有限公司（福州）",
    "海航航空技术有限公司（天津）",
    "海航航空技术有限公司（云南）"
]

st.title("航司费用计算器")

# 在侧边栏上传文件
st.sidebar.title("上传文件")
uploaded_files = {}

for airline in airlines:
    uploaded_files[airline] = st.sidebar.file_uploader(f"上传{airline}表格", type=["xlsx", "xls"], key=airline)

# 计算费用按钮
if st.sidebar.button("计算所有费用"):
    results = []
    for airline, file in uploaded_files.items():
        if file is not None:
            try:
                # 读取Excel文件
                excel_file = pd.ExcelFile(file)
                
                # 检查是否存在“应收操作版”子表
                if '应收操作版' in excel_file.sheet_names:
                    df = pd.read_excel(excel_file, sheet_name='应收操作版')
                    
                    # 分别计算每个目标公司的“结算金额”总和
                    for company in target_companies:
                        company_df = df[df['申请人所在公司'] == company]
                        total_cost = company_df['结算金额'].sum()
                        
                        # 添加结果到列表
                        results.append((airline, company, total_cost))
                else:
                    st.warning(f"{airline}的表格中不存在‘应收操作版’子表，跳过计算")
            except Exception as e:
                st.error(f"{airline}的文件读取错误：{str(e)}")
        else:
            st.info(f"{airline}未上传文件，跳过计算")
    
    # 显示结果
    if results:
        results_df = pd.DataFrame(results, columns=["航空公司", "申请人所在公司", "结算金额"])
        st.write(results_df)
    else:
        st.info("没有可显示的结果")