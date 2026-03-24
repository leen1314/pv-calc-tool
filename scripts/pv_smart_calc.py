#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光伏收益智能测算工具
根据用户输入的部分参数，自动补全其他参数并标注来源
"""

# ========== 城市数据 ==========
CITY_DATA = {
    "合肥": {"lat": 31.82, "hours": 1100, "default_price": 0.40},
    "黄山": {"lat": 29.32, "hours": 1050, "default_price": 0.39},
    "铜陵": {"lat": 30.94, "hours": 1080, "default_price": 0.39},
    "北京": {"lat": 39.90, "hours": 1200, "default_price": 0.40},
    "上海": {"lat": 31.23, "hours": 1050, "default_price": 0.40},
    "南京": {"lat": 32.06, "hours": 1080, "default_price": 0.40},
    "杭州": {"lat": 30.27, "hours": 1050, "default_price": 0.40},
    "武汉": {"lat": 30.58, "hours": 1000, "default_price": 0.40},
    "长沙": {"lat": 28.23, "hours": 1000, "default_price": 0.40},
    "广州": {"lat": 23.13, "hours": 950, "default_price": 0.45},
    "深圳": {"lat": 22.54, "hours": 950, "default_price": 0.45},
    "成都": {"lat": 30.67, "hours": 950, "default_price": 0.40},
    "重庆": {"lat": 29.56, "hours": 900, "default_price": 0.40},
    "西安": {"lat": 34.34, "hours": 1100, "default_price": 0.40},
    "济南": {"lat": 36.65, "hours": 1150, "default_price": 0.40},
    "郑州": {"lat": 34.76, "hours": 1100, "default_price": 0.40},
    "宿州": {"lat": 33.65, "hours": 1100, "default_price": 0.38},
}

# ========== 默认参数 ==========
DEFAULT_PARAMS = {
    "cost_per_watt": 1.8,     # 元/W
    "feed_price": 0.20,       # 上网电价
    "loan_rate": 0.06,        # 贷款利率6%
    "loan_years": 7,          # 贷款年限
    "loan_ratio": 0.70,       # 贷款比例70%
    "opex_ratio": 0.02,       # 运维费率2%
    "pr": 0.80,               # 系统效率
    "tilt": 0,                # 倾角
}

def get_city_info(location):
    """获取城市数据"""
    for city in CITY_DATA:
        if city in location:
            return CITY_DATA[city]
    return {"lat": 31.0, "hours": 1050, "default_price": 0.40}  # 默认合肥

def smart_calc(
    location=None,        # 安装地点
    capacity_kw=None,     # 装机功率(kWp)
    fixed_price=None,     # 固定电价(自用)
    consumption=None,      # 消纳比例
    loan_ratio=None,      # 贷款比例（可选）
    **kwargs
):
    """
    智能测算 - 只输入必要参数
    """
    params = {}
    notes = []
    
    # 1. 地点
    if location:
        city_info = get_city_info(location)
        params["location"] = location
        params["lat"] = city_info["lat"]
        params["full_hours"] = city_info["hours"]
        notes.append(f"📍 满发小时: {city_info['hours']}h (基于{location}数据)")
    else:
        return {"error": "请提供安装地点"}
    
    # 2. 装机功率
    if capacity_kw:
        params["capacity_kw"] = capacity_kw
    else:
        return {"error": "请提供装机功率"}
    
    # 3. 固定电价
    if fixed_price:
        params["elec_self"] = fixed_price
        notes.append(f"💰 自用电价: {fixed_price}元/kWh (用户给定)")
    else:
        params["elec_self"] = city_info["default_price"]
        notes.append(f"💰 自用电价: {params['elec_self']}元/kWh (默认)")
    
    # 4. 消纳比例
    if consumption is not None:
        params["consumption"] = consumption
        notes.append(f"🔋 消纳比例: {consumption*100:.0f}% (用户给定)")
    else:
        params["consumption"] = 0.5
        notes.append(f"🔋 消纳比例: 50% (默认)")
    
    # 5. 贷款（可选）
    if loan_ratio is not None:
        params["loan_ratio"] = loan_ratio
        notes.append(f"🏦 贷款比例: {loan_ratio*100:.0f}% (用户给定)")
    else:
        params["loan_ratio"] = DEFAULT_PARAMS["loan_ratio"]  # 默认70%
        notes.append(f"🏦 贷款比例: {params['loan_ratio']*100:.0f}% (默认)")
    
    # 6. 其他默认参数
    params["elec_grid"] = DEFAULT_PARAMS["feed_price"]
    notes.append(f"⚡ 上网电价: {DEFAULT_PARAMS['feed_price']}元/kWh (默认)")
    
    params["cost_per_watt"] = DEFAULT_PARAMS["cost_per_watt"]
    if "loan_rate" not in params:
        params["loan_rate"] = kwargs.get("loan_rate", DEFAULT_PARAMS["loan_rate"])
        if kwargs.get("loan_rate"):
            notes.append(f"🏦 贷款利率: {params['loan_rate']*100:.0f}% (用户给定)")
        else:
            notes.append(f"🏦 贷款利率: {params['loan_rate']*100:.0f}%/{DEFAULT_PARAMS['loan_years']}年 (默认)")
    
    params["loan_years"] = DEFAULT_PARAMS["loan_years"]
    params["opex_ratio"] = DEFAULT_PARAMS["opex_ratio"]
    params["pr"] = DEFAULT_PARAMS["pr"]
    params["tilt"] = DEFAULT_PARAMS["tilt"]
    
    notes.append(f"📊 运维费率: {DEFAULT_PARAMS['opex_ratio']*100:.0f}% (默认)")
    
    # ========== 计算 ==========
    # 发电量
    annual_gen = params["capacity_kw"] * params["full_hours"] / 10000  # 万kWh
    
    # 收入
    self_gen = annual_gen * params["consumption"]
    grid_gen = annual_gen * (1 - params["consumption"])
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
        annual_pmt = monthly_pay * 12  # 月供×12 = 年供
    else:
        annual_pmt = 0
    
    # 运维
    opex = total_invest * params["opex_ratio"]
    
    # 收益
    annual_profit = total_revenue - annual_pmt - opex
    
    # 回收期 = 总投资 / 年收入（不计还款）
    if total_revenue > 0:
        payback = total_invest / total_revenue
    else:
        payback = float('inf')
    
    # 7年累计
    total_profit_7y = annual_profit * 7
    
    # IRR计算（基于自有资金现金流）
    # 第0年投入自有资金，第1-7年减去还款，第8年后只扣运维
    equity = total_invest - loan
    cashflows = [-equity]
    annual_cf_with_loan = total_revenue - annual_pmt - opex
    annual_cf_no_loan = total_revenue - opex
    
    for y in range(1, params["loan_years"] + 1):
        cashflows.append(annual_cf_with_loan)
    for y in range(params["loan_years"] + 1, 26):
        cashflows.append(annual_cf_no_loan)
    
    # 手动IRR计算
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
    
    result = {
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
    
    return result

def print_result(r):
    """打印结果"""
    print("\n" + "=" * 60)
    print(f"  ☀️ {r['params']['location']} {r['params']['capacity_kw']}kWp 光伏收益测算")
    print("=" * 60)
    
    # 参数来源
    print("\n【参数来源】")
    for note in r["notes"]:
        print(f"  {note}")
    
    # 发电量
    print(f"""
【发电量】
  年发电: {r['annual_gen']:.2f}万kWh
  自用({r['params']['consumption']*100:.0f}%): {r['annual_gen']*r['params']['consumption']:.2f}万kWh × ¥{r['params']['elec_self']} = ¥{r['revenue_self']:.2f}万
  上网({(1-r['params']['consumption'])*100:.0f}%): {r['annual_gen']*(1-r['params']['consumption']):.2f}万kWh × ¥{r['params']['elec_grid']} = ¥{r['revenue_grid']:.2f}万
""")
    
    # 投资
    print(f"""【投资融资】
  投资: ¥{r['params']['cost_per_watt']}/W = ¥{r['total_invest']:.1f}万
  贷款: {r['params']['loan_ratio']*100:.0f}% = ¥{r['loan']:.1f}万
  自筹: ¥{r['equity']:.1f}万
""")
    
    # 收益
    print(f"""【收益】
  年收入: ¥{r['total_revenue']:.2f}万
  年还款: ¥{r['annual_pmt']:.2f}万
  运维: ¥{r['opex']:.2f}万
  ═════════════════════════════════════
  年利润: ¥{r['annual_profit']:.2f}万
""")
    
    print("-" * 60)
    print(f"  📊 回收期: {r['payback']:.1f}年 (投资/年收入)")
    print(f"  📈 7年IRR: {r['irr_7']:.1f}%")
    print(f"  💰 7年累计: ¥{r['total_profit_7y']:.1f}万")
    print("-" * 60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 命令行参数
        location = sys.argv[1] if len(sys.argv) > 1 else None
        capacity = float(sys.argv[2]) if len(sys.argv) > 2 else None
        price = float(sys.argv[3]) if len(sys.argv) > 3 else None
        consumption = float(sys.argv[4]) if len(sys.argv) > 4 else None
        loan = float(sys.argv[5])/100 if len(sys.argv) > 5 else None
        
        r = smart_calc(location, capacity, price, consumption, loan)
    else:
        # 交互模式
        print("\n📱 智能光伏测算 - 输入参数")
        print("=" * 40)
        location = input("安装地点(如合肥/黄山): ").strip() or None
        capacity = input("装机功率(kWp): ").strip()
        capacity = float(capacity) if capacity else None
        price = input("固定电价(元/kWh): ").strip()
        price = float(price) if price else None
        consumption = input("消纳比例(0-1): ").strip()
        consumption = float(consumption) if consumption else None
        loan = input("贷款比例(0-100%): ").strip()
        loan = float(loan)/100 if loan else None
        
        r = smart_calc(location, capacity, price, consumption, loan)
    
    if "error" in r:
        print(f"\n❌ {r['error']}")
    else:
        print_result(r)
