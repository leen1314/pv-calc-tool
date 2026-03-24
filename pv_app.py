#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光伏收益测算网页版 - Streamlit App v2.0
增强版：加入发电量修正参数
"""

import streamlit as st

# ========== 城市数据 ==========
CITY_DATA = {
    "合肥": {"lat": 31.82, "hours": 1100, "default_price": 0.40, "avg_temp": 16},
    "黄山": {"lat": 29.32, "hours": 1050, "default_price": 0.39, "avg_temp": 16},
    "铜陵": {"lat": 30.94, "hours": 1080, "default_price": 0.39, "avg_temp": 17},
    "宿州": {"lat": 33.65, "hours": 1100, "default_price": 0.38, "avg_temp": 15},
    "芜湖": {"lat": 31.33, "hours": 1080, "default_price": 0.39, "avg_temp": 16},
    "蚌埠": {"lat": 32.92, "hours": 1080, "default_price": 0.39, "avg_temp": 15},
    "安庆": {"lat": 30.53, "hours": 1050, "default_price": 0.39, "avg_temp": 17},
    "马鞍山": {"lat": 31.67, "hours": 1080, "default_price": 0.39, "avg_temp": 16},
    "滁州": {"lat": 32.30, "hours": 1080, "default_price": 0.38, "avg_temp": 15},
    "阜阳": {"lat": 32.89, "hours": 1080, "default_price": 0.38, "avg_temp": 15},
    # 江苏
    "南京": {"lat": 32.06, "hours": 1080, "default_price": 0.40, "avg_temp": 16},
    "苏州": {"lat": 31.30, "hours": 1050, "default_price": 0.40, "avg_temp": 17},
    "无锡": {"lat": 31.49, "hours": 1050, "default_price": 0.40, "avg_temp": 17},
    "常州": {"lat": 31.81, "hours": 1050, "default_price": 0.40, "avg_temp": 16},
    "南通": {"lat": 31.98, "hours": 1050, "default_price": 0.40, "avg_temp": 16},
    "扬州": {"lat": 32.39, "hours": 1050, "default_price": 0.40, "avg_temp": 16},
    "盐城": {"lat": 33.35, "hours": 1050, "default_price": 0.40, "avg_temp": 15},
    "徐州": {"lat": 34.21, "hours": 1100, "default_price": 0.40, "avg_temp": 14},
    "镇江": {"lat": 32.20, "hours": 1050, "default_price": 0.40, "avg_temp": 16},
    "泰州": {"lat": 32.46, "hours": 1050, "default_price": 0.40, "avg_temp": 16},
    "连云港": {"lat": 34.59, "hours": 1100, "default_price": 0.40, "avg_temp": 14},
    "淮安": {"lat": 33.55, "hours": 1050, "default_price": 0.40, "avg_temp": 15},
    "宿迁": {"lat": 33.96, "hours": 1080, "default_price": 0.40, "avg_temp": 15},
    # 浙江
    "杭州": {"lat": 30.27, "hours": 1050, "default_price": 0.40, "avg_temp": 17},
    "宁波": {"lat": 29.87, "hours": 1000, "default_price": 0.40, "avg_temp": 17},
    "温州": {"lat": 28.00, "hours": 950, "default_price": 0.40, "avg_temp": 18},
    "嘉兴": {"lat": 30.75, "hours": 1050, "default_price": 0.40, "avg_temp": 17},
    "湖州": {"lat": 30.87, "hours": 1050, "default_price": 0.40, "avg_temp": 17},
    "绍兴": {"lat": 30.00, "hours": 1000, "default_price": 0.40, "avg_temp": 17},
    "金华": {"lat": 29.08, "hours": 1000, "default_price": 0.40, "avg_temp": 18},
    "衢州": {"lat": 28.97, "hours": 1000, "default_price": 0.40, "avg_temp": 18},
    "舟山": {"lat": 30.04, "hours": 950, "default_price": 0.40, "avg_temp": 17},
    "台州": {"lat": 28.66, "hours": 950, "default_price": 0.40, "avg_temp": 18},
    "丽水": {"lat": 28.46, "hours": 950, "default_price": 0.40, "avg_temp": 18},
    # 上海
    "上海": {"lat": 31.23, "hours": 1050, "default_price": 0.40, "avg_temp": 17},
    # 北京
    "北京": {"lat": 39.90, "hours": 1200, "default_price": 0.40, "avg_temp": 13},
    # 广东
    "广州": {"lat": 23.13, "hours": 950, "default_price": 0.45, "avg_temp": 22},
    "深圳": {"lat": 22.54, "hours": 950, "default_price": 0.45, "avg_temp": 23},
    "佛山": {"lat": 23.02, "hours": 950, "default_price": 0.45, "avg_temp": 22},
    "东莞": {"lat": 23.04, "hours": 950, "default_price": 0.45, "avg_temp": 23},
    "中山": {"lat": 22.52, "hours": 950, "default_price": 0.45, "avg_temp": 22},
    "珠海": {"lat": 22.27, "hours": 950, "default_price": 0.45, "avg_temp": 22},
    "江门": {"lat": 22.58, "hours": 950, "default_price": 0.45, "avg_temp": 22},
    "惠州": {"lat": 23.11, "hours": 950, "default_price": 0.45, "avg_temp": 22},
    "肇庆": {"lat": 23.05, "hours": 950, "default_price": 0.45, "avg_temp": 22},
    "汕头": {"lat": 23.35, "hours": 950, "default_price": 0.45, "avg_temp": 22},
    # 湖北
    "武汉": {"lat": 30.58, "hours": 1000, "default_price": 0.40, "avg_temp": 17},
    "宜昌": {"lat": 30.69, "hours": 950, "default_price": 0.40, "avg_temp": 17},
    "襄阳": {"lat": 32.01, "hours": 1000, "default_price": 0.40, "avg_temp": 16},
    "荆州": {"lat": 30.33, "hours": 950, "default_price": 0.40, "avg_temp": 17},
    "黄冈": {"lat": 30.45, "hours": 950, "default_price": 0.40, "avg_temp": 17},
    "孝感": {"lat": 30.92, "hours": 950, "default_price": 0.40, "avg_temp": 17},
    # 湖南
    "长沙": {"lat": 28.23, "hours": 1000, "default_price": 0.40, "avg_temp": 17},
    "株洲": {"lat": 27.83, "hours": 950, "default_price": 0.40, "avg_temp": 18},
    "湘潭": {"lat": 27.82, "hours": 950, "default_price": 0.40, "avg_temp": 18},
    "衡阳": {"lat": 26.89, "hours": 950, "default_price": 0.40, "avg_temp": 18},
    "岳阳": {"lat": 29.35, "hours": 950, "default_price": 0.40, "avg_temp": 17},
    "常德": {"lat": 29.04, "hours": 950, "default_price": 0.40, "avg_temp": 17},
    # 四川
    "成都": {"lat": 30.67, "hours": 950, "default_price": 0.40, "avg_temp": 17},
    "绵阳": {"lat": 31.47, "hours": 950, "default_price": 0.40, "avg_temp": 17},
    "德阳": {"lat": 31.13, "hours": 950, "default_price": 0.40, "avg_temp": 17},
    "宜宾": {"lat": 28.77, "hours": 900, "default_price": 0.40, "avg_temp": 18},
    "南充": {"lat": 30.80, "hours": 900, "default_price": 0.40, "avg_temp": 17},
    "泸州": {"lat": 28.87, "hours": 900, "default_price": 0.40, "avg_temp": 18},
    # 重庆
    "重庆": {"lat": 29.56, "hours": 900, "default_price": 0.40, "avg_temp": 18},
    # 陕西
    "西安": {"lat": 34.34, "hours": 1100, "default_price": 0.40, "avg_temp": 14},
    "咸阳": {"lat": 34.33, "hours": 1100, "default_price": 0.40, "avg_temp": 14},
    "榆林": {"lat": 38.29, "hours": 1400, "default_price": 0.40, "avg_temp": 9},
    "延安": {"lat": 36.59, "hours": 1200, "default_price": 0.40, "avg_temp": 12},
    # 山东
    "济南": {"lat": 36.65, "hours": 1150, "default_price": 0.40, "avg_temp": 14},
    "青岛": {"lat": 36.07, "hours": 1100, "default_price": 0.40, "avg_temp": 13},
    "烟台": {"lat": 37.52, "hours": 1200, "default_price": 0.40, "avg_temp": 13},
    "潍坊": {"lat": 36.71, "hours": 1150, "default_price": 0.40, "avg_temp": 13},
    "临沂": {"lat": 35.10, "hours": 1100, "default_price": 0.40, "avg_temp": 14},
    "济宁": {"lat": 35.41, "hours": 1100, "default_price": 0.40, "avg_temp": 14},
    "泰安": {"lat": 36.19, "hours": 1150, "default_price": 0.40, "avg_temp": 14},
    "威海": {"lat": 37.51, "hours": 1200, "default_price": 0.40, "avg_temp": 13},
    # 河南
    "郑州": {"lat": 34.76, "hours": 1100, "default_price": 0.40, "avg_temp": 15},
    "洛阳": {"lat": 34.62, "hours": 1100, "default_price": 0.40, "avg_temp": 15},
    "开封": {"lat": 34.79, "hours": 1100, "default_price": 0.40, "avg_temp": 15},
    "南阳": {"lat": 33.00, "hours": 1050, "default_price": 0.40, "avg_temp": 15},
    "新乡": {"lat": 35.30, "hours": 1100, "default_price": 0.40, "avg_temp": 15},
    "安阳": {"lat": 36.10, "hours": 1150, "default_price": 0.40, "avg_temp": 14},
    # 河北
    "石家庄": {"lat": 38.04, "hours": 1100, "default_price": 0.40, "avg_temp": 13},
    "唐山": {"lat": 39.63, "hours": 1200, "default_price": 0.40, "avg_temp": 12},
    "保定": {"lat": 38.87, "hours": 1150, "default_price": 0.40, "avg_temp": 13},
    "廊坊": {"lat": 39.52, "hours": 1150, "default_price": 0.40, "avg_temp": 13},
    "沧州": {"lat": 38.30, "hours": 1150, "default_price": 0.40, "avg_temp": 13},
    # 江西
    "南昌": {"lat": 28.68, "hours": 1000, "default_price": 0.40, "avg_temp": 18},
    "九江": {"lat": 29.71, "hours": 1000, "default_price": 0.40, "avg_temp": 17},
    "赣州": {"lat": 25.85, "hours": 950, "default_price": 0.40, "avg_temp": 19},
    "上饶": {"lat": 28.45, "hours": 950, "default_price": 0.40, "avg_temp": 18},
    # 福建
    "福州": {"lat": 26.08, "hours": 950, "default_price": 0.40, "avg_temp": 20},
    "厦门": {"lat": 24.48, "hours": 900, "default_price": 0.40, "avg_temp": 21},
    "泉州": {"lat": 24.87, "hours": 900, "default_price": 0.40, "avg_temp": 21},
    "漳州": {"lat": 24.51, "hours": 900, "default_price": 0.40, "avg_temp": 21},
    "莆田": {"lat": 25.45, "hours": 950, "default_price": 0.40, "avg_temp": 20},
    # 其他
    "天津": {"lat": 39.13, "hours": 1150, "default_price": 0.40, "avg_temp": 13},
    "沈阳": {"lat": 41.80, "hours": 1150, "default_price": 0.40, "avg_temp": 9},
    "大连": {"lat": 38.91, "hours": 1100, "default_price": 0.40, "avg_temp": 11},
    "长春": {"lat": 43.88, "hours": 1200, "default_price": 0.40, "avg_temp": 6},
    "哈尔滨": {"lat": 45.75, "hours": 1200, "default_price": 0.40, "avg_temp": 5},
}

# ========== 默认参数 ==========
DEFAULT_PARAMS = {
    "cost_per_watt": 1.8,      # 元/W
    "loan_ratio": 0.7,          # 贷款70%
    "loan_rate": 0.06,          # 6%
    "loan_years": 7,            # 7年
    "feed_price": 0.2,          # 上网电价
    "opex_ratio": 0.02,         # 运维费率
    "pr": 0.80,                # 系统效率（默认）
    "tilt": 30,                # 倾角
    "temp_coeff": 0.004,       # 温度系数 %/℃
    "temp_ref": 25,            # 组件参考温度
    "dust_loss": 0.03,         # 灰尘遮挡损失
    "dc_loss": 0.02,          # 直流侧线损
    "ac_loss": 0.01,          # 交流侧线损
}

def smart_calc(location, capacity_kw, fixed_price, consumption, loan_ratio, loan_rate,
               pr=None, tilt=30, dust_loss=None, dc_loss=None, ac_loss=None):
    """计算光伏收益 - 增强版"""
    params = {}
    notes = []
    
    # 地点
    city_info = CITY_DATA.get(location, {"lat": 31.0, "hours": 1000, "default_price": 0.40, "avg_temp": 16})
    params["location"] = location
    params
    params["lat"] = city_info["lat"]
    params["full_hours"] = city_info["hours"]
    params["avg_temp"] = city_info.get("avg_temp", 25)
    notes.append(f"📍 满发小时: {city_info['hours']}h (理论)")
    
    params["capacity_kw"] = capacity_kw
    params["elec_self"] = fixed_price
    params["consumption"] = consumption
    params["loan_ratio"] = loan_ratio
    params["loan_rate"] = loan_rate
    params["elec_grid"] = DEFAULT_PARAMS["feed_price"]
    params["cost_per_watt"] = DEFAULT_PARAMS["cost_per_watt"]
    params["loan_years"] = DEFAULT_PARAMS["loan_years"]
    params["opex_ratio"] = DEFAULT_PARAMS["opex_ratio"]
    
    # ====== 修正参数处理 ======
    # PR值
    params["pr"] = pr if pr else DEFAULT_PARAMS["pr"]
    notes.append(f"🔧 系统效率PR: {params['pr']*100:.0f}%")
    
    # 倾角
    params["tilt"] = tilt
    notes.append(f"📐 组件倾角: {tilt}°")
    
    # 灰尘损失
    params["dust_loss"] = dust_loss if dust_loss is not None else DEFAULT_PARAMS["dust_loss"]
    notes.append(f"🌫️ 灰尘遮挡: {params['dust_loss']*100:.0f}%")
    
    # 线损
    params["dc_loss"] = dc_loss if dc_loss is not None else DEFAULT_PARAMS["dc_loss"]
    params["ac_loss"] = ac_loss if ac_loss is not None else DEFAULT_PARAMS["ac_loss"]
    notes.append(f"⚡ 线损: 直流{params['dc_loss']*100:.0f}% + 交流{params['ac_loss']*100:.0f}%")
    
    # 温度衰减
    temp_diff = params["avg_temp"] - DEFAULT_PARAMS["temp_ref"]
    temp_loss = temp_diff * DEFAULT_PARAMS["temp_coeff"] * 100
    if temp_loss > 0:
        notes.append(f"🌡️ 温度衰减: -{temp_loss:.1f}% (年均温{params['avg_temp']}°C)")
    else:
        notes.append(f"🌡️ 温度增益: +{abs(temp_loss):.1f}%")
    
    # ====== 发电量计算 ======
    # 理论发电量
    theoretical_gen = params["capacity_kw"] * params["full_hours"] / 10000  # 万kWh
    
    # 实际发电量 = 理论 × PR × (1-各项损失)
    total_loss = params["pr"] - 1 + params["dust_loss"] + params["dc_loss"] + params["ac_loss"]
    if temp_loss > 0:
        total_loss += temp_loss / 100
    
    actual_gen = theoretical_gen * (1 + total_loss)  # 万kWh
    
    notes.append(f"📊 修正后年发电: {actual_gen:.2f}万kWh (理论×{1+total_loss:.2f})")
    
    params["theoretical_gen"] = theoretical_gen
    params["actual_gen"] = actual_gen
    
    # ====== 收益计算 ======
    self_gen = actual_gen * params["consumption"]
    grid_gen = actual_gen * (1 - params["consumption"])
    revenue_self = self_gen * params["elec_self"]
    revenue_grid = grid_gen * params["elec_grid"]
    total_revenue = revenue_self + revenue_grid
    
    # 投资
    total_invest = params["capacity_kw"] * 1000 * params["cost_per_watt"] / 10000
    loan = total_invest * params["loan_ratio"]
    equity = total_invest - loan
    
    # 还款
    monthly_rate = params["loan_rate"] / 12
    n = params["loan_years"] * 12
    if monthly_rate > 0:
        monthly_pay = loan * monthly_rate * (1+monthly_rate)**n / ((1+monthly_rate)**n - 1)
        annual_pmt = monthly_pay * 12
    else:
        annual_pmt = 0
    
    # 运维
    opex = total_invest * params["opex_ratio"]
    
    # 收益
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
        "theoretical_gen": theoretical_gen,
        "actual_gen": actual_gen,
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
    page_title="光伏收益测算 v2.0",
    page_icon="☀️",
    layout="wide"
)

# ========== 城市列表 ==========
CITIES = list(CITY_DATA.keys())

# ========== 侧边栏 - 参数输入 ==========
st.sidebar.header("📋 项目参数")

with st.sidebar.form("project_form"):
    st.markdown("### 🏠 基本参数")
    location = st.selectbox("📍 安装地点", CITIES, index=0)
    capacity = st.number_input("⚡ 装机功率 (kWp)", min_value=10, max_value=10000, value=250, step=10)
    fixed_price = st.number_input("💰 固定电价 (元/kWh)", min_value=0.1, max_value=2.0, value=0.4, step=0.01)
    consumption = st.slider("🔋 消纳比例", 0.0, 1.0, 0.5, 0.05)
    
    st.markdown("### 💳 融资参数")
    loan_ratio = st.slider("🏦 贷款比例", 0.0, 1.0, 0.7, 0.1)
    loan_rate = st.number_input("📈 贷款利率 (%)", min_value=1.0, max_value=10.0, value=6.0, step=0.5)
    
    st.markdown("### 🔧 发电量修正")
    pr_pct = st.slider("🔧 系统效率PR (%)", 60, 95, 80, 1)
    pr = pr_pct / 100
    tilt = st.slider("📐 组件倾角 (°)", 0, 45, 30, 5)
    dust_loss_pct = st.slider("🌫️ 灰尘遮挡损失 (%)", 0, 10, 3, 1)
    dust_loss = dust_loss_pct / 100
    
    submitted = st.form_submit_button("🚀 开始测算", type="primary")

# ========== 主页面 ==========
st.title("☀️ 光伏收益测算工具 v2.0")
st.markdown("—— 增强版：支持发电量修正 ——")

if submitted:
    r = smart_calc(
        location=location,
        capacity_kw=capacity,
        fixed_price=fixed_price,
        consumption=consumption,
        loan_ratio=loan_ratio,
        loan_rate=loan_rate/100,
        pr=pr,
        tilt=tilt,
        dust_loss=dust_loss
    )
    
    if "error" in r:
        st.error(f"❌ {r['error']}")
    else:
        # 核心指标
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 回收期", f"{r['payback']:.1f}年")
        with col2:
            st.metric("📈 7年IRR", f"{r['irr_7']:.1f}%")
        with col3:
            st.metric("💰 7年累计", f"¥{r['total_profit_7y']:.1f}万")
        with col4:
            st.metric("⚡ 实际年发电", f"{r['actual_gen']:.1f}万kWh")
        
        # 发电量对比
        st.divider()
        col_theory, col_actual = st.columns(2)
        with col_theory:
            st.metric("📉 理论发电量", f"{r['theoretical_gen']:.1f}万kWh", 
                     delta=f"未修正", delta_color="off")
        with col_actual:
            st.metric("✅ 实际发电量", f"{r['actual_gen']:.1f}万kWh",
                     delta=f"+{(r['actual_gen']/r['theoretical_gen']-1)*100:.1f}%", 
                     delta_color="normal")
        
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
            st.write(f"**实际年发电:** {r['actual_gen']:.2f}万kWh")
            st.write(f"**自用({r['params']['consumption']*100:.0f}%):** {r['actual_gen']*r['params']['consumption']:.2f}万kWh × ¥{r['params']['elec_self']} = ¥{r['revenue_self']:.2f}万")
            st.write(f"**上网({(1-r['params']['consumption'])*100:.0f}%):** {r['actual_gen']*(1-r['params']['consumption']):.2f}万kWh × ¥{r['params']['elec_grid']} = ¥{r['revenue_grid']:.2f}万")
            
            st.subheader("🔧 损耗明细")
            st.write(f"PR系统效率: {r['params']['pr']*100:.0f}%")
            st.write(f"灰尘遮挡: {r['params']['dust_loss']*100:.0f}%")
            st.write(f"线损: {(r['params']['dc_loss']+r['params']['ac_loss'])*100:.0f}%")
        
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
    
    **基本参数：**
    - 安装地点 - 选择项目所在城市
    - 装机功率 - 光伏板总功率 (kWp)
    - 固定电价 - 自用电价 (元/kWh)
    - 消纳比例 - 自用占发电量的比例
    
    **发电量修正：**
    - **PR值** - 系统效率，一般0.75-0.82，保守取0.78
    - **倾角** - 组件安装角度，最佳角度=当地纬度±5°
    - **灰尘损失** - 北方取5-8%，南方取2-3%
    
    ### 📊 默认参数
    - 投资单价: 1.8元/W
    - 贷款年限: 7年
    - 上网电价: 0.2元/kWh
    - 运维费率: 2%/年
    - 直流线损: 2%
    - 交流线损: 1%
    """)
