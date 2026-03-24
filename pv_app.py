#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光伏收益测算网页版 - Streamlit App
"""

import streamlit as st

# ========== 城市数据 ==========
CITY_DATA = {
    "合肥": {"lat": 31.82, "hours": 1100, "default_price": 0.40},
    "黄山": {"lat": 29.32, "hours": 1050, "default_price": 0.39},
    "铜陵": {"lat": 30.94, "hours": 1080, "default_price": 0.39},
    "宿州": {"lat": 33.65, "hours": 1100, "default_price": 0.38},
    "芜湖": {"lat": 31.33, "hours": 1080, "default_price": 0.39},
    "蚌埠": {"lat": 32.92, "hours": 1080, "default_price": 0.39},
    "安庆": {"lat": 30.53, "hours": 1050, "default_price": 0.39},
    "马鞍山": {"lat": 31.67, "hours": 1080, "default_price": 0.39},
    "滁州": {"lat": 32.30, "hours": 1080, "default_price": 0.38},
    "阜阳": {"lat": 32.89, "hours": 1080, "default_price": 0.38},
    # 江苏
    "南京": {"lat": 32.06, "hours": 1080, "default_price": 0.40},
    "苏州": {"lat": 31.30, "hours": 1050, "default_price": 0.40},
    "无锡": {"lat": 31.49, "hours": 1050, "default_price": 0.40},
    "常州": {"lat": 31.81, "hours": 1050, "default_price": 0.40},
    "南通": {"lat": 31.98, "hours": 1050, "default_price": 0.40},
    "扬州": {"lat": 32.39, "hours": 1050, "default_price": 0.40},
    "盐城": {"lat": 33.35, "hours": 1050, "default_price": 0.40},
    "徐州": {"lat": 34.21, "hours": 1100, "default_price": 0.40},
    "镇江": {"lat": 32.20, "hours": 1050, "default_price": 0.40},
    "泰州": {"lat": 32.46, "hours": 1050, "default_price": 0.40},
    "连云港": {"lat": 34.59, "hours": 1100, "default_price": 0.40},
    "淮安": {"lat": 33.55, "hours": 1050, "default_price": 0.40},
    "宿迁": {"lat": 33.96, "hours": 1080, "default_price": 0.40},
    # 浙江
    "杭州": {"lat": 30.27, "hours": 1050, "default_price": 0.40},
    "宁波": {"lat": 29.87, "hours": 1000, "default_price": 0.40},
    "温州": {"lat": 28.00, "hours": 950, "default_price": 0.40},
    "嘉兴": {"lat": 30.75, "hours": 1050, "default_price": 0.40},
    "湖州": {"lat": 30.87, "hours": 1050, "default_price": 0.40},
    "绍兴": {"lat": 30.00, "hours": 1000, "default_price": 0.40},
    "金华": {"lat": 29.08, "hours": 1000, "default_price": 0.40},
    "衢州": {"lat": 28.97, "hours": 1000, "default_price": 0.40},
    "舟山": {"lat": 30.04, "hours": 950, "default_price": 0.40},
    "台州": {"lat": 28.66, "hours": 950, "default_price": 0.40},
    "丽水": {"lat": 28.46, "hours": 950, "default_price": 0.40},
    # 上海
    "上海": {"lat": 31.23, "hours": 1050, "default_price": 0.40},
    # 北京
    "北京": {"lat": 39.90, "hours": 1200, "default_price": 0.40},
    # 广东
    "广州": {"lat": 23.13, "hours": 950, "default_price": 0.45},
    "深圳": {"lat": 22.54, "hours": 950, "default_price": 0.45},
    "佛山": {"lat": 23.02, "hours": 950, "default_price": 0.45},
    "东莞": {"lat": 23.04, "hours": 950, "default_price": 0.45},
    "中山": {"lat": 22.52, "hours": 950, "default_price": 0.45},
    "珠海": {"lat": 22.27, "hours": 950, "default_price": 0.45},
    "江门": {"lat": 22.58, "hours": 950, "default_price": 0.45},
    "惠州": {"lat": 23.11, "hours": 950, "default_price": 0.45},
    "肇庆": {"lat": 23.05, "hours": 950, "default_price": 0.45},
    "汕头": {"lat": 23.35, "hours": 950, "default_price": 0.45},
    # 湖北
    "武汉": {"lat": 30.58, "hours": 1000, "default_price": 0.40},
    "宜昌": {"lat": 30.69, "hours": 950, "default_price": 0.40},
    "襄阳": {"lat": 32.01, "hours": 1000, "default_price": 0.40},
    "荆州": {"lat": 30.33, "hours": 950, "default_price": 0.40},
    "黄冈": {"lat": 30.45, "hours": 950, "default_price": 0.40},
    "孝感": {"lat": 30.92, "hours": 950, "default_price": 0.40},
    # 湖南
    "长沙": {"lat": 28.23, "hours": 1000, "default_price": 0.40},
    "株洲": {"lat": 27.83, "hours": 950, "default_price": 0.40},
    "湘潭": {"lat": 27.82, "hours": 950, "default_price": 0.40},
    "衡阳": {"lat": 26.89, "hours": 950, "default_price": 0.40},
    "岳阳": {"lat": 29.35, "hours": 950, "default_price": 0.40},
    "常德": {"lat": 29.04, "hours": 950, "default_price": 0.40},
    # 四川
    "成都": {"lat": 30.67, "hours": 950, "default_price": 0.40},
    "绵阳": {"lat": 31.47, "hours": 950, "default_price": 0.40},
    "德阳": {"lat": 31.13, "hours": 950, "default_price": 0.40},
    "宜宾": {"lat": 28.77, "hours": 900, "default_price": 0.40},
    "南充": {"lat": 30.80, "hours": 900, "default_price": 0.40},
    "泸州": {"lat": 28.87, "hours": 900, "default_price": 0.40},
    # 重庆
    "重庆": {"lat": 29.56, "hours": 900, "default_price": 0.40},
    # 陕西
    "西安": {"lat": 34.34, "hours": 1100, "default_price": 0.40},
    "咸阳": {"lat": 34.33, "hours": 1100, "default_price": 0.40},
    "榆林": {"lat": 38.29, "hours": 1400, "default_price": 0.40},
    "延安": {"lat": 36.59, "hours": 1200, "default_price": 0.40},
    # 山东
    "济南": {"lat": 36.65, "hours": 1150, "default_price": 0.40},
    "青岛": {"lat": 36.07, "hours": 1100, "default_price": 0.40},
    "烟台": {"lat": 37.52, "hours": 1200, "default_price": 0.40},
    "潍坊": {"lat": 36.71, "hours": 1150, "default_price": 0.40},
    "临沂": {"lat": 35.10, "hours": 1100, "default_price": 0.40},
    "济宁": {"lat": 35.41, "hours": 1100, "default_price": 0.40},
    "泰安": {"lat": 36.19, "hours": 1150, "default_price": 0.40},
    "威海": {"lat": 37.51, "hours": 1200, "default_price": 0.40},
    # 河南
    "郑州": {"lat": 34.76, "hours": 1100, "default_price": 0.40},
    "洛阳": {"lat": 34.62, "hours": 1100, "default_price": 0.40},
    "开封": {"lat": 34.79, "hours": 1100, "default_price": 0.40},
    "南阳": {"lat": 33.00, "hours": 1050, "default_price": 0.40},
    "新乡": {"lat": 35.30, "hours": 1100, "default_price": 0.40},
    "安阳": {"lat": 36.10, "hours": 1150, "default_price": 0.40},
    # 河北
    "石家庄": {"lat": 38.04, "hours": 1100, "default_price": 0.40},
    "唐山": {"lat": 39.63, "hours": 1200, "default_price": 0.40},
    "保定": {"lat": 38.87, "hours": 1150, "default_price": 0.40},
    "廊坊": {"lat": 39.52, "hours": 1150, "default_price": 0.40},
    "沧州": {"lat": 38.30, "hours": 1150, "default_price": 0.40},
    # 江西
    "南昌": {"lat": 28.68, "hours": 1000, "default_price": 0.40},
    "九江": {"lat": 29.71, "hours": 1000, "default_price": 0.40},
    "赣州": {"lat": 25.85, "hours": 950, "default_price": 0.40},
    "上饶": {"lat": 28.45, "hours": 950, "default_price": 0.40},
    # 福建
    "福州": {"lat": 26.08, "hours": 950, "default_price": 0.40},
    "厦门": {"lat": 24.48, "hours": 900, "default_price": 0.40},
    "泉州": {"lat": 24.87, "hours": 900, "default_price": 0.40},
    "漳州": {"lat": 24.51, "hours": 900, "default_price": 0.40},
    "莆田": {"lat": 25.45, "hours": 950, "default_price": 0.40},
    # 其他
    "天津": {"lat": 39.13, "hours": 1150, "default_price": 0.40},
    "沈阳": {"lat": 41.80, "hours": 1150, "default_price": 0.40},
    "大连": {"lat": 38.91, "hours": 1100, "default_price": 0.40},
    "长春": {"lat": 43.88, "hours": 1200, "default_price": 0.40},
    "哈尔滨": {"lat": 45.75, "hours": 1200, "default_price": 0.40},
}

# ========== 默认参数 ==========
DEFAULT_PARAMS = {
    "cost_per_watt": 1.8,      # 元/W
    "loan_ratio": 0.7,          # 贷款70%
    "loan_rate": 0.06,          # 6%
    "loan_years": 7,            # 7年
    "feed_price": 0.2,          # 上网电价
    "opex_ratio": 0.02,         # 运维费率
    "pr": 0.80,                # 系统效率
    "tilt": 30,                # 倾角
}

def smart_calc(location, capacity_kw, fixed_price, consumption, loan_ratio, loan_rate):
    """计算光伏收益"""
    params = {}
    notes = []
    
    # 地点
    city_info = CITY_DATA.get(location, {"lat": 31.0, "hours": 1000, "default_price": 0.40})
    params["location"] = location
    params["lat"] = city_info["lat"]
    params["full_hours"] = city_info["hours"]
    notes.append(f"📍 满发小时: {city_info['hours']}h")
    
    params["capacity_kw"] = capacity_kw
    params["elec_self"] = fixed_price
    params["consumption"] = consumption
    params["loan_ratio"] = loan_ratio
    params["loan_rate"] = loan_rate
    params["elec_grid"] = DEFAULT_PARAMS["feed_price"]
    params["cost_per_watt"] = DEFAULT_PARAMS["cost_per_watt"]
    params["loan_years"] = DEFAULT_PARAMS["loan_years"]
    params["opex_ratio"] = DEFAULT_PARAMS["opex_ratio"]
    
    notes.append(f"💰 自用电价: {fixed_price}元/kWh")
    notes.append(f"🔋 消纳比例: {consumption*100:.0f}%")
    notes.append(f"🏦 贷款: {loan_ratio*100:.0f}% / {loan_rate*100:.1f}%")
    
    # 计算
    annual_gen = params["capacity_kw"] * params["full_hours"] / 10000  # 万kWh
    
    self_gen = annual_gen * params["consumption"]
    grid_gen = annual_gen * (1 - params["consumption"])
    revenue_self = self_gen * params["elec_self"]
    revenue_grid = grid_gen * params["elec_grid"]
    total_revenue = revenue_self + revenue_grid
    
    total_invest = params["capacity_kw"] * 1000 * params["cost_per_watt"] / 10000
    loan = total_invest * params["loan_ratio"]
    equity = total_invest - loan
    
    monthly_rate = params["loan_rate"] / 12
    n = params["loan_years"] * 12
    if monthly_rate > 0:
        monthly_pay = loan * monthly_rate * (1+monthly_rate)**n / ((1+monthly_rate)**n - 1)
        annual_pmt = monthly_pay * 12
    else:
        annual_pmt = 0
    
    opex = total_invest * params["opex_ratio"]
    annual_profit = total_revenue - annual_pmt - opex
    
    if total_revenue > 0:
        payback = total_invest / total_revenue
    else:
        payback = float('inf')
    
    total_profit_7y = annual_profit * 7
    
    # IRR简化计算
    cashflows = [-equity]
    annual_cf_with_loan = total_revenue - annual_pmt - opex
    annual_cf_no_loan = total_revenue - opex
    
    for y in range(1, params["loan_years"] + 1):
        cashflows.append(annual_cf_with_loan)
    for y in range(params["loan_years"] + 1, 26):
        cashflows.append(annual_cf_no_loan)
    
    def npv(r, cfs):
        return sum(cf / (1+r)**i for i, cf in enumerate(cfs))
    
    irr_7 = 0
    try:
        for ir in range(-50, 100):
            r = ir / 100
            if npv(r, cashflows) > 0:
                continue
            r1, r2 = r - 0.01, r
            for _ in range(50):
                r_mid = (r1 + r2) / 2
                if npv(r_mid, cashflows) > 0:
                    r1 = r_mid
                else:
                    r2 = r_mid
            irr_7 = (r1 + r2) / 2 * 100
            break
    except:
        irr_7 = 0
    

    return {
        "params": params,
        "notes": notes,
        "annual_gen": annual_gen,
        "revenue_self": revenue_self,
        "revenue_grid": revenue_grid,
        "total_revenue": total_revenue,
        "total_invest": total_invest,
        "loan": loan,
        "equity": equity,
        "annual_pmt": annual_pmt,
        "opex": opex,
        "annual_profit": annual_profit,
        "payback": payback,
        "irr_7": irr_7,
        "total_profit_7y": total_profit_7y,
    }

# ========== 页面配置 ==========
st.set_page_config(
    page_title="光伏收益测算",
    page_icon="☀️",
    layout="wide"
)

# ========== 城市列表 ==========
CITIES = list(CITY_DATA.keys())

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
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 回收期", f"{r['payback']:.1f}年")
        with col2:
            st.metric("📈 7年IRR", f"{r['irr_7']:.1f}%")
        with col3:
            st.metric("💰 7年累计", f"¥{r['total_profit_7y']:.1f}万")
        with col4:
            st.metric("⚡ 年发电量", f"{r['annual_gen']:.1f}万kWh")
        
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
        
        st.divider()
        with st.expander("📝 参数来源说明"):
            for note in r["notes"]:
                st.write(f"- {note}")
        
        st.divider()
        if r["irr_7"] < 0:
            st.warning("⚠️ 建议：7年IRR为负，建议降低贷款比例或提高消纳比例")
        elif r["irr_7"] < 10:
            st.info("💡 建议：收益一般，可考虑优化电价或消纳")
        else:
            st.success("✅ 收益良好，项目可行!")

else:
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
