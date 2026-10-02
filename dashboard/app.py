import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.analytics import kpis, category_analysis, region_delivery_analysis, channel_analysis, customer_analysis, return_analysis
from src.investment_optimizer import investment_plan, allocation_summary

st.set_page_config(page_title="FUTURISTIC // ACCkart AI Command Center", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

@st.cache_data(show_spinner=False)
def get_data():
    return clean_data(load_data())

d = get_data(); K = kpis(d); PLAN = investment_plan(d); SUMMARY = allocation_summary(d)

# ---------- FUTURISTIC DESIGN SYSTEM ----------
st.markdown(r'''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;600;700;800&display=swap');
:root{--bg:#050611;--card:rgba(18,20,38,.76);--line:rgba(255,255,255,.10);--white:#f7f9ff;--muted:#929bb5;--cyan:#35e7ff;--violet:#9d6cff;--pink:#ff4fb3;--lime:#b7ff52;--yellow:#ffd45a;--orange:#ff9b54;}
html,body,[class*="css"]{font-family:Manrope,sans-serif}.stApp{background:#050611;color:var(--white)}
[data-testid="stAppViewContainer"]{background:radial-gradient(circle at 85% 8%,rgba(53,231,255,.18),transparent 25%),radial-gradient(circle at 10% 20%,rgba(157,108,255,.18),transparent 28%),radial-gradient(circle at 70% 80%,rgba(255,79,179,.10),transparent 25%),linear-gradient(135deg,#050611,#090b1c 55%,#060711)}
[data-testid="stHeader"]{background:transparent}.block-container{max-width:1700px;padding:20px 32px 55px}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#08091a,#0c0b1d 55%,#090a16);border-right:1px solid rgba(255,255,255,.10)}
section[data-testid="stSidebar"] .block-container{padding:22px 16px}
.stButton>button{border-radius:14px;border:1px solid rgba(255,255,255,.10);background:linear-gradient(145deg,#171a31,#0d1021);color:#fff;box-shadow:6px 6px 18px #02030a,-3px -3px 10px rgba(255,255,255,.025)}
.stButton>button:hover{border-color:var(--cyan);color:var(--cyan);box-shadow:0 0 22px rgba(53,231,255,.15)}
[data-baseweb="select"]>div{background:#101326;border-color:rgba(255,255,255,.10);color:#fff}
.brand{display:flex;gap:12px;align-items:center;margin-bottom:24px}.brand-orb{width:45px;height:45px;border-radius:16px;display:grid;place-items:center;font-size:22px;color:#fff;background:conic-gradient(from 30deg,var(--cyan),var(--violet),var(--pink),var(--yellow),var(--cyan));box-shadow:0 0 28px rgba(53,231,255,.22),inset 0 0 14px rgba(255,255,255,.35)}
.brand-title{font-weight:800;letter-spacing:.16em;font-size:14px}.brand-sub{font:9px 'DM Mono';color:var(--muted);letter-spacing:.1em}
.hero{position:relative;overflow:hidden;border:1px solid rgba(255,255,255,.11);border-radius:32px;padding:32px;margin-bottom:15px;background:linear-gradient(135deg,rgba(24,27,53,.90),rgba(8,10,24,.78));box-shadow:0 35px 100px rgba(0,0,0,.35),inset 0 1px rgba(255,255,255,.08)}
.hero:before{content:"";position:absolute;width:420px;height:420px;right:-100px;top:-230px;border-radius:50%;background:radial-gradient(circle,rgba(53,231,255,.22),transparent 65%);filter:blur(4px)}
.hero:after{content:"✦";position:absolute;right:70px;top:35px;font-size:130px;color:rgba(255,255,255,.035);transform:rotate(18deg)}
.eyebrow{font:10px 'DM Mono';color:var(--cyan);letter-spacing:.18em}.hero h1{font-size:clamp(34px,5vw,68px);line-height:.94;letter-spacing:-.06em;margin:12px 0}.gradient{background:linear-gradient(90deg,#fff,var(--cyan),var(--violet),var(--pink));-webkit-background-clip:text;background-clip:text;color:transparent}.hero p{max-width:820px;color:#a7aec2;line-height:1.7;font-size:14px}.pills{display:flex;gap:8px;flex-wrap:wrap;margin-top:20px}.pill{border:1px solid rgba(255,255,255,.10);padding:7px 11px;border-radius:999px;background:rgba(255,255,255,.035);font:9px 'DM Mono';color:#b9c1d5}.pill.live{color:var(--lime);box-shadow:0 0 18px rgba(183,255,82,.06)}
.kpis{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin:12px 0 15px}.kpi{min-height:118px;padding:17px;border-radius:22px;border:1px solid rgba(255,255,255,.10);background:linear-gradient(145deg,rgba(26,29,53,.86),rgba(12,14,29,.82));box-shadow:8px 8px 25px rgba(0,0,0,.23),-3px -3px 14px rgba(255,255,255,.018);position:relative;overflow:hidden}.kpi:after{content:"";position:absolute;right:-35px;bottom:-45px;width:100px;height:100px;border-radius:50%;background:radial-gradient(circle,rgba(53,231,255,.25),transparent 70%)}.kpi .label{font:9px 'DM Mono';color:#818aa4;letter-spacing:.13em}.kpi .num{font-size:25px;font-weight:800;margin-top:14px;letter-spacing:-.045em}.kpi .delta{font-size:10px;color:#788299;margin-top:5px}
.section{border:1px solid rgba(255,255,255,.09);border-radius:25px;background:rgba(11,13,29,.72);padding:20px;margin-bottom:15px;box-shadow:0 25px 70px rgba(0,0,0,.20),inset 0 1px rgba(255,255,255,.04)}.section-head{display:flex;justify-content:space-between;align-items:end;margin-bottom:15px}.section-kicker{font:9px 'DM Mono';color:#707a95;letter-spacing:.15em;text-transform:uppercase}.section-title{font-size:18px;font-weight:800;margin-top:5px}.rainbow-line{height:2px;background:linear-gradient(90deg,var(--cyan),var(--violet),var(--pink),var(--yellow),var(--lime));border-radius:99px;box-shadow:0 0 18px rgba(157,108,255,.4);margin:0 0 18px}
.signal{padding:15px;border-radius:17px;background:linear-gradient(135deg,rgba(255,255,255,.04),rgba(255,255,255,.012));border:1px solid rgba(255,255,255,.07);margin-bottom:9px}.signal .tag{font:9px 'DM Mono';letter-spacing:.12em}.signal b{display:block;font-size:12px;margin:5px 0}.signal span{font-size:10px;color:#8993aa;line-height:1.55}.c-cyan{color:var(--cyan)}.c-pink{color:var(--pink)}.c-lime{color:var(--lime)}.c-yellow{color:var(--yellow)}.c-violet{color:#b9a5ff}
.chat-shell{border:1px solid rgba(255,255,255,.10);border-radius:26px;padding:18px;background:linear-gradient(145deg,rgba(25,26,53,.88),rgba(10,12,28,.88));box-shadow:inset 0 1px rgba(255,255,255,.06),0 25px 80px rgba(0,0,0,.25)}.chat-head{display:flex;align-items:center;gap:12px}.bot{width:45px;height:45px;border-radius:15px;display:grid;place-items:center;background:linear-gradient(135deg,var(--cyan),var(--violet),var(--pink));box-shadow:0 0 25px rgba(157,108,255,.25);font-size:20px}.chat-title{font-weight:800}.chat-sub{font:9px 'DM Mono';color:var(--lime);letter-spacing:.12em}.bubble{padding:12px 14px;border-radius:15px;margin:10px 0;font-size:11px;line-height:1.6}.bubble.ai{background:rgba(53,231,255,.055);border:1px solid rgba(53,231,255,.12)}.bubble.user{background:rgba(157,108,255,.08);border:1px solid rgba(157,108,255,.14)}
.badge{display:inline-block;padding:5px 9px;border-radius:999px;font:8px 'DM Mono';letter-spacing:.1em;border:1px solid rgba(255,255,255,.10)}.badge.hot{color:#ff7bc4;background:rgba(255,79,179,.07)}.badge.smart{color:var(--cyan);background:rgba(53,231,255,.07)}
.footer{text-align:center;padding:20px;color:#59637a;font:9px 'DM Mono';letter-spacing:.08em}
@media(max-width:1150px){.kpis{grid-template-columns:repeat(3,1fr)}}@media(max-width:700px){.block-container{padding:12px}.kpis{grid-template-columns:repeat(2,1fr)}.hero{padding:22px}}
</style>''', unsafe_allow_html=True)

# ---------- HELPERS ----------
def money(v):
    if abs(v)>=1e7:return f"₹{v/1e7:.2f} Cr"
    if abs(v)>=1e5:return f"₹{v/1e5:.2f} L"
    return f"₹{v:,.0f}"

def fig_base(fig,height=330):
    fig.update_layout(template='plotly_dark',height=height,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=10,r=10,t=45,b=10),font=dict(family='Manrope',color='#aeb7cc',size=10),title_font=dict(size=13,color='#f4f6ff'),legend=dict(bgcolor='rgba(0,0,0,0)'))
    fig.update_xaxes(showgrid=False,zeroline=False)
    fig.update_yaxes(showgrid=False,zeroline=False)
    return fig

# ---------- SIDEBAR ----------
st.sidebar.markdown("<div class='brand'><div class='brand-orb'>✦</div><div><div class='brand-title'>FUTURISTIC</div><div class='brand-sub'>ACCKART / AI DECISION LAB</div></div></div>",unsafe_allow_html=True)
view=st.sidebar.radio('COMMAND CENTER',['✦ Executive Universe','◉ Opportunity Radar','◎ Investment Lab','✧ Seller Copilot','◌ Buyer Copilot','◇ Data Observatory'])
st.sidebar.markdown('---')
st.sidebar.markdown("<span class='badge hot'>SPECIAL MENTION</span> <span class='badge smart'>AI + BI</span>",unsafe_allow_html=True)
st.sidebar.caption('Team FUTURISTIC · Evidence-first commerce intelligence')
st.sidebar.caption('30K orders · 500 products · 5K customers · 1K campaigns')

# ---------- HERO ----------
st.markdown(f'''<div class='hero'><div class='eyebrow'>TEAM FUTURISTIC / ACCKART DECISION INTELLIGENCE</div><h1>Commerce, but <span class='gradient'>alive.</span></h1><p>One colourful command center for the ₹10 lakh decision — connecting revenue, margin, customers, marketing, returns, delivery and explainable AI recommendations for sellers and buyers.</p><div class='pills'><span class='pill live'>● DATA CONNECTED</span><span class='pill'>₹10L DECISION</span><span class='pill'>30,000 ORDERS</span><span class='pill'>5,000 CUSTOMERS</span><span class='pill'>MODELLED IMPACT ≠ GUARANTEE</span></div></div>''',unsafe_allow_html=True)

metrics=[('NET REVENUE',money(K['revenue']),'30K orders'),('RECORDED PROFIT',money(K['profit']),f"{K['margin_pct']:.1f}% margin"),('AOV',money(K['aov']),'per order'),('RETURN RATE',f"{K['return_rate_pct']:.1f}%",money(K['return_cost'])+' cost'),('CANCEL RATE',f"{K['cancel_rate_pct']:.1f}%",'order-level'),('DECISION BUDGET','₹10.00 L','investment envelope')]
st.markdown('<div class="kpis">'+''.join(f'<div class="kpi"><div class="label">{a}</div><div class="num">{b}</div><div class="delta">{c}</div></div>' for a,b,c in metrics)+'</div>',unsafe_allow_html=True)

# ---------- EXECUTIVE ----------
if view.startswith('✦'):
    st.markdown('<div class="section"><div class="section-head"><div><div class="section-kicker">01 / Holographic business pulse</div><div class="section-title">The ACCkart universe</div></div><span class="badge smart">LIVE ANALYTICS</span></div><div class="rainbow-line"></div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    cat=category_analysis(d); ch=channel_analysis(d)
    fig=px.bar(cat.sort_values('Revenue'),x='Revenue',y='Category',orientation='h',color='Revenue',color_continuous_scale=['#22244b','#35e7ff'],title='Revenue gravity');fig=fig_base(fig,300);fig.update_coloraxes(showscale=False);c1.plotly_chart(fig,use_container_width=True)
    fig=px.bar(cat.sort_values('Profit'),x='Profit',y='Category',orientation='h',color='Profit',color_continuous_scale=['#ff4fb3','#9d6cff','#b7ff52'],title='Profit pressure');fig=fig_base(fig,300);fig.update_coloraxes(showscale=False);c2.plotly_chart(fig,use_container_width=True)
    fig=px.bar(ch.sort_values('Weighted_ROI_Pct'),x='Weighted_ROI_Pct',y='Channel',orientation='h',color='Weighted_ROI_Pct',color_continuous_scale=['#ff4fb3','#9d6cff','#35e7ff','#b7ff52'],title='Campaign energy');fig=fig_base(fig,300);fig.update_coloraxes(showscale=False);c3.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)
    l,r=st.columns([1,1.25])
    with l:
        st.markdown('<div class="section"><div class="section-kicker">02 / Special mentions</div><div class="section-title">Signals judges can remember</div><div class="rainbow-line"></div>',unsafe_allow_html=True)
        signals=[('c-cyan','REVENUE GIANT','Electronics','~79.3% of revenue is concentrated here, while margin is only ~2.5%.'),('c-pink','PROFIT LEAK','Grocery','Recorded category profit is approximately −₹3.67L.'),('c-yellow','SERVICE ALERT','West','~93.7% delayed deliveries in the supplied delivery data.'),('c-lime','GROWTH LEVER','Retention','Customer-risk analysis is converted into an explicit scenario investment lever.')]
        for cls,tag,title,desc in signals: st.markdown(f'<div class="signal"><div class="tag {cls}">{tag}</div><b>{title}</b><span>{desc}</span></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with r:
        st.markdown('<div class="section"><div class="section-kicker">03 / Capital orbit</div><div class="section-title">Where the ₹10L goes</div><div class="rainbow-line"></div>',unsafe_allow_html=True)
        fig=go.Figure(go.Pie(labels=PLAN['Initiative'],values=PLAN['Allocation'],hole=.64,textinfo='percent',marker=dict(colors=['#35e7ff','#9d6cff','#b7ff52','#ff4fb3','#ffd45a','#ff9b54'])))
        fig.update_layout(height=380,template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',margin=dict(l=0,r=0,t=5,b=0),showlegend=True,legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(size=9)),annotations=[dict(text='<b>₹10L</b><br><span style="font-size:9px">DECISION</span>',x=.5,y=.5,showarrow=False,font=dict(size=23,color='white'))])
        st.plotly_chart(fig,use_container_width=True)
        st.markdown(f'<div class="signal"><div class="tag c-lime">MODELLED OUTCOME</div><b>{money(SUMMARY["expected_incremental_profit"])} incremental profit scenario</b><span>Scenario ROI: {SUMMARY["expected_roi_pct"]:.1f}%. Assumptions are explicitly labelled in Investment Lab.</span></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

# ---------- RADAR ----------
elif view.startswith('◉'):
    reg=region_delivery_analysis(d); rr=return_analysis(d); cust=customer_analysis(d)
    st.markdown('<div class="section"><div class="section-kicker">Opportunity intelligence</div><div class="section-title">The value-recovery radar</div><div class="rainbow-line"></div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    fig=px.bar(reg.sort_values('Delay_Rate'),x='Delay_Rate',y='Region',orientation='h',color='Delay_Rate',color_continuous_scale=['#b7ff52','#ffd45a','#ff4fb3'],title='Delivery reliability');fig=fig_base(fig,350);fig.update_coloraxes(showscale=False);c1.plotly_chart(fig,use_container_width=True)
    fig=px.bar(rr.sort_values('Total_Cost'),x='Total_Cost',y='Return_Reason',orientation='h',color='Total_Cost',color_continuous_scale=['#9d6cff','#ff4fb3'],title='Return-cost pressure');fig=fig_base(fig,350);fig.update_coloraxes(showscale=False);c2.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="section"><div class="section-kicker">Customer intelligence</div><div class="section-title">Who needs attention?</div><div class="rainbow-line"></div>',unsafe_allow_html=True)
    a,b=st.columns([.9,1.4])
    if 'Risk' in cust.columns:
        counts=cust['Risk'].value_counts().reset_index();counts.columns=['Risk','Customers'];fig=px.pie(counts,names='Risk',values='Customers',hole=.62,color_discrete_sequence=['#35e7ff','#9d6cff','#b7ff52','#ff4fb3'],title='Risk mix');fig=fig_base(fig,360);a.plotly_chart(fig,use_container_width=True)
    b.dataframe(cust.round(2),use_container_width=True,hide_index=True,height=360)
    st.markdown('</div>',unsafe_allow_html=True)

# ---------- INVESTMENT ----------
elif view.startswith('◎'):
    st.markdown('<div class="section"><div class="section-kicker">Decision laboratory</div><div class="section-title">The ₹10L investment engine</div><div class="rainbow-line"></div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    fig=go.Figure(go.Pie(labels=PLAN['Initiative'],values=PLAN['Allocation'],hole=.68,textinfo='label+percent',marker=dict(colors=['#35e7ff','#9d6cff','#b7ff52','#ff4fb3','#ffd45a','#ff9b54'])));fig.update_layout(template='plotly_dark',height=440,paper_bgcolor='rgba(0,0,0,0)',margin=dict(l=0,r=0,t=20,b=0),annotations=[dict(text='₹10L',x=.5,y=.5,showarrow=False,font_size=25,font_color='white')]);c1.plotly_chart(fig,use_container_width=True)
    fig=px.bar(PLAN.sort_values('Expected_Incremental_Profit'),x='Expected_Incremental_Profit',y='Initiative',orientation='h',color='ROI_Pct',color_continuous_scale=['#ff4fb3','#9d6cff','#35e7ff','#b7ff52'],title='Modelled incremental profit');fig=fig_base(fig,440);fig.update_coloraxes(showscale=False);c2.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="section"><div class="section-kicker">Traceability</div><div class="section-title">Every rupee has a reason</div><div class="rainbow-line"></div>',unsafe_allow_html=True)
    show=PLAN[['Initiative','Allocation','ROI_Pct','Expected_Incremental_Profit','Evidence_or_Assumption']].copy();show['Allocation']=show['Allocation'].map(money);show['Expected_Incremental_Profit']=show['Expected_Incremental_Profit'].map(money);show['ROI_Pct']=show['ROI_Pct'].map(lambda x:f'{x:.1f}%');st.dataframe(show,use_container_width=True,hide_index=True,height=350);st.info('Historical ROI is measured from supplied campaign data. Delivery, reactivation and Grocery repair contain scenario assumptions; they are not guarantees.')
    st.markdown('</div>',unsafe_allow_html=True)

# ---------- SELLER COPILOT ----------
elif view.startswith('✧'):
    st.markdown('<div class="section"><div class="section-kicker">AI Commerce Copilot</div><div class="section-title">Seller Copilot — turn data into action</div><div class="rainbow-line"></div>',unsafe_allow_html=True)
    a,b=st.columns([.8,1.2])
    with a:
        st.markdown('<div class="chat-shell"><div class="chat-head"><div class="bot">✦</div><div><div class="chat-title">FUTURISTIC Seller AI</div><div class="chat-sub">● GROUNDED IN ACCKART DATA</div></div></div>',unsafe_allow_html=True)
        q=st.selectbox('Quick question',['What should I sell more?','Where am I losing profit?','Which region needs action?','How should I use the ₹10L?'])
        answers={'What should I sell more?':'Electronics drives the largest revenue share (~79.3%), but scale should be paired with margin monitoring because its recorded margin is only ~2.5%.','Where am I losing profit?':'Grocery is the clearest category-level profit leak in the supplied analysis, with approximately −₹3.67L recorded profit.','Which region needs action?':'West is the delivery reliability hotspot, with approximately 93.7% delayed deliveries in the supplied delivery data.','How should I use the ₹10L?':f"Use the Investment Lab allocation. The current model allocates the full ₹10L across referral, retention, Google Ads, West delivery, reactivation and Grocery repair."}
        st.markdown(f'<div class="bubble user">{q}</div><div class="bubble ai"><b>✦ Data-grounded answer</b><br>{answers[q]}</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with b:
        st.markdown('<div class="signal"><div class="tag c-cyan">SELLER PLAYBOOK</div><b>1. Protect high-revenue categories</b><span>Monitor Electronics margin and product-level contribution before blindly increasing volume.</span></div><div class="signal"><div class="tag c-pink">SELLER PLAYBOOK</div><b>2. Repair margin leakage</b><span>Investigate Grocery pricing, cost, returns and fulfilment before scaling demand.</span></div><div class="signal"><div class="tag c-yellow">SELLER PLAYBOOK</div><b>3. Fix experience hotspots</b><span>West delivery reliability is a measurable operational intervention point.</span></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ---------- BUYER COPILOT ----------
elif view.startswith('◌'):
    st.markdown('<div class="section"><div class="section-kicker">AI Shopping Intelligence</div><div class="section-title">Buyer Copilot — explainable recommendations</div><div class="rainbow-line"></div>',unsafe_allow_html=True)
    products=d['products'].copy() if 'products' in d else pd.DataFrame()
    a,b=st.columns([.8,1.2])
    with a:
        st.markdown('<div class="chat-shell"><div class="chat-head"><div class="bot">✦</div><div><div class="chat-title">FUTURISTIC Buyer AI</div><div class="chat-sub">● RECOMMENDATIONS FROM PRODUCT DATA</div></div></div>',unsafe_allow_html=True)
        cat_options=['All'] + (sorted(products['Category'].dropna().astype(str).unique().tolist()) if 'Category' in products.columns else [])
        chosen=st.selectbox('What are you shopping for?',cat_options)
        if not products.empty:
            viewp=products if chosen=='All' else products[products['Category'].astype(str)==chosen]
            cols=[c for c in ['Product_ID','Product_Name','Category','Price','Rating'] if c in viewp.columns]
            if 'Rating' in viewp.columns: viewp=viewp.sort_values(['Rating']+(['Price'] if 'Price' in viewp.columns else []),ascending=[False]+([True] if 'Price' in viewp.columns else []))
            st.dataframe(viewp[cols].head(8),use_container_width=True,hide_index=True)
            st.markdown('<div class="bubble ai"><b>✦ Recommendation logic</b><br>Products are surfaced from the supplied catalog. The dashboard does not claim personal preferences or guarantee product quality; it exposes measurable catalog attributes.</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with b:
        st.markdown('<div class="signal"><div class="tag c-lime">BUYER MODE</div><b>Compare before you buy</b><span>Use category, price and rating signals together rather than relying on one metric.</span></div><div class="signal"><div class="tag c-violet">SMART EXPLANATION</div><b>Why this item?</b><span>The copilot can explain the measurable attributes that caused a product to appear in the shortlist.</span></div><div class="signal"><div class="tag c-pink">TRUST LAYER</div><b>No black-box claims</b><span>Recommendations remain traceable to the uploaded ACCkart product catalog.</span></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ---------- DATA ----------
else:
    st.markdown('<div class="section"><div class="section-kicker">Data Observatory</div><div class="section-title">Trust layer / source health</div><div class="rainbow-line"></div>',unsafe_allow_html=True)
    rows=[{'Dataset':name,'Rows':len(df),'Columns':len(df.columns),'Duplicates':int(df.duplicated().sum()),'Missing Cells':int(df.isna().sum().sum())} for name,df in d.items()];st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True);st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="section"><div class="section-kicker">Schema explorer</div><div class="section-title">Inspect the source tables</div><div class="rainbow-line"></div>',unsafe_allow_html=True);selected=st.selectbox('Dataset',list(d.keys()));st.dataframe(d[selected].head(100),use_container_width=True,hide_index=True,height=430);st.markdown('</div>',unsafe_allow_html=True)

st.markdown('<div class="footer">✦ TEAM FUTURISTIC · ACCKART AI COMMERCE COMMAND CENTER · SOURCE-GROUNDED · HISTORICAL DATA ≠ GUARANTEED FUTURE PERFORMANCE</div>',unsafe_allow_html=True)

# --- FUTURISTIC LIVE PULSE + TIMELINE ---
import time
from datetime import datetime

def futuristic_timeline_section(orders_df, allocation_df=None):
    """Interactive historical pulse and decision timeline.
    Uses actual order dates when available; 'live' means auto-refreshing UI,
    not a claim that the supplied static CSV is a real-time data feed.
    """
    st.markdown("""
    <div class="ft-section">
      <div class="ft-eyebrow">◉ LIVE PULSE / TEMPORAL INTELLIGENCE</div>
      <h2>Business Time Machine</h2>
      <p>Explore historical business movement, rolling performance and the sequence from signal → insight → investment action.</p>
    </div>
    """, unsafe_allow_html=True)

    date_col = next((c for c in ["order_date", "orderDate", "date", "order_dt", "created_at"] if c in orders_df.columns), None)
    if date_col is None:
        st.info("Timeline requires an order/date field in the source data.")
        return

    d = orders_df.copy()
    d["_timeline_date"] = pd.to_datetime(d[date_col], errors="coerce")
    d = d.dropna(subset=["_timeline_date"]).sort_values("_timeline_date")
    if d.empty:
        st.warning("No valid dates were found for the timeline.")
        return

    numeric_candidates = {
        "Revenue": ["revenue", "sales", "order_value", "total_amount", "amount"],
        "Profit": ["profit", "gross_profit", "net_profit"],
        "Orders": ["order_id", "id"]
    }

    def first_col(cands):
        return next((c for c in cands if c in d.columns), None)

    rev = first_col(numeric_candidates["Revenue"])
    prof = first_col(numeric_candidates["Profit"])
    oid = first_col(numeric_candidates["Orders"])

    min_d, max_d = d["_timeline_date"].min().date(), d["_timeline_date"].max().date()
    c1, c2, c3 = st.columns([1.2, 1.2, 1])
    with c1:
        start = st.date_input("FROM", min_d, key="ft_start")
    with c2:
        end = st.date_input("TO", max_d, key="ft_end")
    with c3:
        window = st.selectbox("ROLLING WINDOW", [7, 14, 30], index=2, key="ft_window")

    mask = (d["_timeline_date"].dt.date >= start) & (d["_timeline_date"].dt.date <= end)
    x = d.loc[mask].copy()
    if x.empty:
        st.warning("No records in the selected period.")
        return

    agg = x.set_index("_timeline_date")
    metric = st.selectbox(
        "PULSE METRIC",
        [m for m, col in [("Revenue", rev), ("Profit", prof), ("Orders", oid)] if col],
        key="ft_metric"
    )

    if metric == "Revenue":
        series = pd.to_numeric(agg[rev], errors="coerce").resample("D").sum().fillna(0)
    elif metric == "Profit":
        series = pd.to_numeric(agg[prof], errors="coerce").resample("D").sum().fillna(0)
    else:
        series = agg[oid].resample("D").nunique()

    rolling = series.rolling(window, min_periods=1).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=series.index, y=series.values, mode="lines",
        name=metric, line=dict(width=2.5, color="#00E5FF"),
        fill="tozeroy", fillcolor="rgba(0,229,255,.08)"
    ))
    fig.add_trace(go.Scatter(
        x=rolling.index, y=rolling.values, mode="lines",
        name=f"{window}D rolling", line=dict(width=3, color="#C45CFF", dash="dot")
    ))
    fig.update_layout(
        height=390, margin=dict(l=10,r=10,t=25,b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(8,12,30,.65)",
        font=dict(color="#EAF6FF"), hovermode="x unified",
        xaxis=dict(showgrid=False), yaxis=dict(gridcolor="rgba(255,255,255,.06)")
    )
    st.plotly_chart(fig, use_container_width=True, key="ft_pulse_chart")

    # Decision timeline
    st.markdown("### ◈ DECISION TIMELINE")
    events = []
    events.append((min_d, "DATA", "ACCkart dataset enters the intelligence pipeline"))
    if rev:
        peak_day = series.idxmax().date()
        events.append((peak_day, "SIGNAL", f"{metric} peak detected: {series.max():,.0f}"))
    if prof:
        low_day = pd.to_numeric(agg[prof], errors="coerce").resample("D").sum().fillna(0).idxmin().date()
        events.append((low_day, "RISK", "Lowest daily profit signal detected"))
    events.append((max_d, "DECISION", "₹10L investment strategy prepared"))

    events = sorted(events, key=lambda z: z[0])
    for dt, kind, msg in events:
        badge = {"DATA":"DATA", "SIGNAL":"SIGNAL", "RISK":"RISK", "DECISION":"ACTION"}[kind]
        st.markdown(
            f"""<div class="ft-timeline">
            <div class="ft-dot"></div>
            <div class="ft-date">{dt.strftime('%d %b %Y')}</div>
            <div class="ft-badge">{badge}</div>
            <div class="ft-event">{msg}</div>
            </div>""",
            unsafe_allow_html=True
        )

    # Auto-refresh toggle: visual refresh only; source remains static unless replaced.
    live = st.toggle("◉ AUTO-REFRESH VISUAL PULSE", value=False, key="ft_live")
    if live:
        st.caption("Auto-refresh updates the dashboard view. The supplied CSV files remain the source of truth.")
        time.sleep(1)
        st.rerun()

