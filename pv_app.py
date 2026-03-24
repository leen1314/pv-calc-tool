#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光伏收益测算网页版 - Streamlit App
"""

import streamlit as st
import sys
import os

# 自动查找 pv_smart_calc.py
script_dir = os.path.dirname(os.path.abspath(__file__))
possible_paths = [
    script_dir,
    '/home/admin123/.openclaw/workspace/scripts',
    os.path.join(os.path.expanduser('~'), 'Desktop')
]
for p in possible_paths:
    if os.path.exists(os.path.join(p, 'pv_smart_calc.py')):
        sys.path.insert(0, p)
        break

from pv_smart_calc import smart_calc

# ========== 页面配置 ==========
st.set_page_config(
    page_title="光伏收益测算",
    page_icon="☀️",
    layout="wide"
)

# ========== 城市数据（用于下拉框） ==========
CITIES = [
    # 安徽
    "合肥", "黄山", "铜陵", "宿州", "芜湖", "蚌埠", "安庆", "马鞍山", "滁州", "阜阳",
    # 江苏
    "南京", "苏州", "无锡", "常州", "南通", "扬州", "盐城", "徐州", "镇江", "泰州", "连云港", "淮安", "宿迁",
    # 浙江
    "杭州", "宁波", "温州", "嘉兴", "湖州", "绍兴", "金华", "衢州", "舟山", "台州", "丽水",
    # 上海
    "上海",
    # 北京
    "北京",
    # 广东
    "广州", "深圳", "佛山", "东莞", "中山", "珠海", "江门", "惠州", "肇庆", "汕头",
    # 湖北
    "武汉", "宜昌", "襄阳", "荆州", "黄冈", "孝感",
    # 湖南
    "长沙", "株洲", "湘潭", "衡阳", "岳阳", "常德",
    # 四川
    "成都", "绵阳", "德阳", "宜宾", "南充", "泸州",
    # 重庆
    "重庆",
    # 陕西
    "西安", "咸阳", "榆林", "延安",
    # 山东
    "济南", "青岛", "烟台", "潍坊", "临沂", "济宁", "泰安", "威海",
    # 河南
    "郑州", "洛阳", "开封", "南阳", "新乡", "安阳",
    # 河北
    "石家庄", "唐山", "保定", "廊坊", "沧州",
    # 江西
    "南昌", "九江", "赣州", "上饶",
    # 福建
    "福州", "厦门", "泉州", "漳州", "莆田",
    # 其他
    "天津", "沈阳", "大连", "长春", "哈尔滨"
]

# ========== 侧边栏 - 参数输入 ==========
st.sidebar.header("📋 项目参数")

with st.sidebar.form("project_form"):
    location = st.selectbox("📍 安装地点", CITIES, index=0)
    capacity = st.number_input("⚡ 装机功率 (kWp)", min_value=10, max_value=10000, value=250, step=10)
    fixed_price = st.number_input("💰 固定电价 (元/kWh)", min_value=0.1, max_value=2.0, value=0.4, step=0.01)
    consumption = st.slider("🔋 消纳比例", 0.0, 1.0, 0.5, 0.05)
    loan_ratio = st.slider("🏦 贷款比例", 0.0, 1.0, 0.7, 0.1)
    loan_rate = st.number_input("📈 贷款利率 (%)", min_value=1.0, max_value=10.0, value=6.0, step=0.5)
    
    submitted = st.form_submit_button("🚀 开始测算", type="primary")

# ========== 主页面 ==========
st.title("☀️ 光伏收益测算工具")
st.markdown("—— 快速评估光伏项目收益 ——")

if submitted:
    # 执行测算
    r = smart_calc(
        location=location,
        capacity_kw=capacity,
        fixed_price=fixed_price,
        consumption=consumption,
        loan_ratio=loan_ratio,
        loan_rate=loan_rate/100
    )
    
    if "error" in r:
        st.error(f"❌ {r['error']}")
    else:
        # ========== 结果展示 ==========
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 回收期", f"{r['payback']:.1f}年")
        with col2:
            st.metric("📈 7年IRR", f"{r['irr_7']:.1f}%")
        with col3:
            st.metric("💰 7年累计", f"¥{r['total_profit_7y']:.1f}万")
        with col4:
            st.metric("⚡ 年发电量", f"{r['annual_gen']:.1f}万kWh")
        
        # ========== 详细数据 ==========
        st.divider()
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📊 投资融资")
            st.write(f"**总投资:** ¥{r['total_invest']:.1f}万 ({r['params']['cost_per_watt']}元/W)")
            st.write(f"**贷款:** ¥{r['loan']:.1f}万 ({r['params']['loan_ratio']*100:.0f}%)")
            st.write(f"**自筹:** ¥{r['equity']:.1f}万")
            
            st.subheader("💵 年度收益")
            st.write(f"**年收入:** ¥{r['total_revenue']:.2f}万")
            st.write(f"**年还款:** ¥{r['annual_pmt']:.2f}万")
            st.write(f"**运维费:** ¥{r['opex']:.2f}万")
            st.write(f"**年利润:** ¥{r['annual_profit']:.2f}万")
        
        with col_right:
            st.subheader("🔋 发电收益明细")
            st.write(f"**年发电:** {r['annual_gen']:.2f}万kWh")
            st.write(f"**自用({r['params']['consumption']*100:.0f}%):** {r['annual_gen']*r['params']['consumption']:.2f}万kWh × ¥{r['params']['elec_self']} = ¥{r['revenue_self']:.2f}万")
            st.write(f"**上网({(1-r['params']['consumption'])*100:.0f}%):** {r['annual_gen']*(1-r['params']['consumption']):.2f}万kWh × ¥{r['params']['elec_grid']} = ¥{r['revenue_grid']:.2f}万")
        
        # ========== 参数来源 ==========
        st.divider()
        with st.expander("📝 参数来源说明"):
            for note in r["notes"]:
                st.write(f"- {note}")
        
        # ========== 建议 ==========
        st.divider()
        if r["irr_7"] < 0:
            st.warning("⚠️ 建议：7年IRR为负，建议降低贷款比例或提高消纳比例")
        elif r["irr_7"] < 10:
            st.info("💡 建议：收益一般，可考虑优化电价或消纳")
        else:
            st.success("✅ 收益良好，项目可行!")

else:
    # 欢迎页面
    st.info("👈 请在左侧填写项目参数，点击「开始测算」")
    
    st.markdown("""
    ### 📖 使用说明
    
    1. **安装地点** - 选择项目所在城市（影响满发小时数）
    2. **装机功率** - 光伏板总功率 (kWp)
    3. **固定电价** - 自用电价 (元/kWh)
    4. **消纳比例** - 自用占发电量的比例
    5. **贷款比例** - 银行贷款占比
    6. **贷款利率** - 年利率
    
    ### 📊 默认参数
    - 投资单价: 1.8元/W
    - 贷款年限: 7年
    - 上网电价: 0.2元/kWh
    - 运维费率: 2%/年
    """)
