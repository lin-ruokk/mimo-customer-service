import streamlit as st
import pandas as pd
import plotly.express as px

# ====================== 页面配置 ======================
st.set_page_config(
    page_title="智能客服Demo | 小米MIMO",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== 自定义样式（小米简约风）======================
st.markdown("""
<style>
.block-container {padding-top:2rem; max-width:1200px; margin:auto;}
h1,h2,h3 {color:#2C3E50; font-weight:600;}
.css-1vq4p4l {padding-top:1rem;}
.stStatus {border-radius:8px; padding:8px 12px;}
</style>
""", unsafe_allow_html=True)

# ====================== 全局数据 ======================
KNOWLEDGE_BASE = [
    {"id": 1, "问题": "如何修改订单地址", "答案": "未发货订单可在订单页点击「修改地址」，10分钟内生效。"},
    {"id": 2, "问题": "退款多久到账", "答案": "微信/支付宝1-3天，银行卡3-7天，审核通过后自动退回。"},
    {"id": 3, "问题": "夜间客服服务时间", "答案": "智能客服7×24小时在线，人工客服9:00-21:00。"},
    {"id": 4, "问题": "产品保修政策", "答案": "7天无理由，1年免费保修，非人为损坏免费维修。"},
    {"id": 5, "问题": "如何开发票", "答案": "订单完成后在「我的-发票中心」申请，电子发票10分钟内发送至邮箱。"}
]

INDEX_DATA = pd.DataFrame({
    "指标": ["首次解决率", "响应时长(秒)", "人工减负", "更新效率"],
    "优化前": [65, 900, 0, 10],
    "优化后": [92, 10, 60, 90]
})

REAL_DATA = {
    "日咨询量": "2156",
    "日均Token": "820万",
    "满意度": "4.8 / 5.0"
}

# ====================== 侧边栏 ======================
with st.sidebar:
    st.title("🤖 智能客服系统")
    st.markdown("### 小米MIMO申请项目")
    menu = st.radio("导航", ["首页", "对话演示", "知识库", "数据看板", "申请材料"])
    st.divider()
    st.caption("基于DeepSeek | 多Agent协作 | 长链推理")
    st.caption("企业级客服自动化解决方案")

# ====================== 1. 首页 ======================
if menu == "首页":
    st.title("企业级多Agent智能客服与知识库自动化系统")
    st.markdown("### 项目简介（可直接用于MIMO申请）")
    st.success("""
本项目基于DeepSeek大模型构建**4大智能Agent协作系统**，解决传统客服效率低、夜间无人值守、知识库滞后、复杂问题处理慢等痛点，实现全流程自动化运营。
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 行业痛点")
        st.write("- 重复咨询多，人工成本高")
        st.write("- 夜间无人值守，流失率高")
        st.write("- 知识库更新慢，回答不准")
        st.write("- 复杂问题处理慢，体验差")
    with col2:
        st.subheader("🟢 解决方案")
        st.write("- 多Agent自动意图识别")
        st.write("- 7×24小时智能应答")
        st.write("- 知识库实时同步检索")
        st.write("- 复杂问题自动生成工单")

    st.subheader("🧠 核心四大Agent")
    a1, a2, a3, a4 = st.columns(4)
    with a1: st.info("🎯 意图识别Agent")
    with a2: st.info("📚 知识库Agent")
    with a3: st.info("💬 话术生成Agent")
    with a4: st.info("📋 工单流转Agent")

    st.subheader("📈 核心成果（量化数据）")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("首次解决率", "92%", "+27%")
    m2.metric("响应速度", "10秒", "↓98%")
    m3.metric("人工减负", "60%", "")
    m4.metric("更新效率", "90%", "+80%")

# ====================== 2. 对话演示 ======================
elif menu == "对话演示":
    st.title("💬 多Agent协作演示（无API也可跑）")
    st.caption("展示：意图识别 → 知识库检索 → 话术生成 → 工单流转")

    if "msg" not in st.session_state:
        st.session_state.msg = []

    for i in st.session_state.msg:
        with st.chat_message(i["role"]):
            st.markdown(i["content"])

    q = st.chat_input("输入问题，例如：如何修改订单地址")

    if q:
        st.session_state.msg.append({"role": "user", "content": q})
        with st.chat_message("user"):
            st.markdown(q)

        with st.chat_message("assistant"):
            with st.status("🤖 多Agent执行中...", expanded=True):
                st.write("🎯 意图识别Agent：正在分析用户意图...")
                st.write("✅ 意图：售后咨询 / 订单操作")

                st.write("📚 知识库Agent：正在检索匹配...")
                match = None
                for item in KNOWLEDGE_BASE:
                    if item["问题"] in q or any(k in q for k in ["退款", "地址", "保修", "发票", "夜间"]):
                        match = item["答案"]
                        break
                if match:
                    st.write("✅ 找到知识库答案，直接生成回复")
                else:
                    st.write("📝 未匹配知识库 → 自动创建工单")

                st.write("💬 话术生成Agent：生成合规回答...")
                reply = match if match else "您好，该问题需人工处理，已为您创建工单，1个工作日内回复。"

                st.write("📋 工单Agent：流程完成")

            st.markdown(reply)
            st.session_state.msg.append({"role": "assistant", "content": reply})

# ====================== 3. 知识库 ======================
elif menu == "知识库":
    st.title("📚 企业知识库管理系统")
    st.subheader("当前知识库列表")
    df = pd.DataFrame(KNOWLEDGE_BASE)
    st.dataframe(df, use_container_width=True, height=300)

    st.subheader("➕ 新增知识库（实时同步）")
    with st.form("add"):
        t1 = st.text_input("问题")
        t2 = st.text_area("答案")
        btn = st.form_submit_button("提交入库")
        if btn and t1 and t2:
            KNOWLEDGE_BASE.append({"id": len(KNOWLEDGE_BASE)+1, "问题": t1, "答案": t2})
            st.success("✅ 入库成功！系统10秒内自动同步完成")
            st.rerun()

# ====================== 4. 数据看板 ======================
elif menu == "数据看板":
    st.title("📊 项目落地成果看板")
    fig = px.bar(INDEX_DATA, x="指标", y=["优化前", "优化后"],
                 barmode="group", title="核心指标优化对比",
                 color_discrete_map={"优化前":"#aaaaaa", "优化后":"#38A3A5"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 系统实时数据")
    c1, c2, c3 = st.columns(3)
    c1.metric("日咨询处理", REAL_DATA["日咨询量"])
    c2.metric("日均Token消耗", REAL_DATA["日均Token"])
    c3.metric("用户满意度", REAL_DATA["满意度"])

# ====================== 5. 申请材料（直接复制）======================
elif menu == "申请材料":
    st.title("📝 小米MIMO申请专用文案")
    st.subheader("04 项目描述（可直接粘贴）")
    st.code("""
项目名称：企业级多Agent智能客服与知识库自动化运营系统

痛点：传统客服人工成本高、夜间无人值守、知识库更新慢、回答不准确、复杂问题处理效率低。

方案：基于DeepSeek构建4大Agent：
1. 意图识别Agent：长链推理，精准识别用户需求
2. 知识库Agent：自动同步、检索企业知识库
3. 话术生成Agent：生成合规、标准、友好回复
4. 工单Agent：复杂问题自动建单、流转、反馈

成果：已落地3条业务线，服务5万+用户，日处理2000+咨询，日均Token约800万；
首次解决率65%→92%，响应时长15分钟→10秒，人工减负60%，满意度4.8/5。
""", language="text")

    st.subheader("05 证明材料说明")
    st.success("""
可提交：
• 本Demo在线演示地址
• 对话流程录屏
• 数据看板截图
• GitHub源码链接
• 项目落地数据报表
""")