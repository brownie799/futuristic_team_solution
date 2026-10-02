
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from .analytics import kpis, category_analysis, region_delivery_analysis, channel_analysis, customer_analysis, return_analysis, evidence
from .investment_optimizer import investment_plan, allocation_summary

def money(x): return f"₹{x:,.0f}"
def pct(x): return f"{x:.1f}%"

def generate_report(d, out_path):
    out_path=Path(out_path); out_path.parent.mkdir(parents=True,exist_ok=True)
    K=kpis(d); E=evidence(d); plan=investment_plan(d)
    cat=category_analysis(d); reg=region_delivery_analysis(d); ch=channel_analysis(d)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, fontSize=22, leading=26))
    doc=SimpleDocTemplate(str(out_path),pagesize=A4,rightMargin=38,leftMargin=38,topMargin=38,bottomMargin=38)
    story=[]
    story += [Paragraph("ACCkart Investment Intelligence",styles["TitleCenter"]),
              Paragraph("₹10 Lakh Decision — Analytical Report",styles["Heading2"]),
              Spacer(1,12),
              Paragraph("Objective: allocate the supplied ₹10,00,000 budget using evidence from orders, products, customer behaviour, marketing, returns and delivery data.",styles["BodyText"]),
              Spacer(1,12)]
    story += [Paragraph("1. Executive Summary",styles["Heading1"]),
      Paragraph(f"ACCkart records {K['orders']:,} orders and ₹{K['revenue']:,.0f} net revenue. Total recorded order profit is {money(K['profit'])}, producing a {pct(K['margin_pct'])} margin. Electronics contributes {E['electronics_revenue_share']:.1f}% of revenue but its observed margin is only {E['electronics_margin']:.1f}%. Grocery is loss-making at {money(E['grocery_profit'])}. West has a {E['west_delay_rate']:.1f}% delivery-delay rate. These signals support a balanced investment approach: scale historically productive acquisition/retention channels while funding targeted delivery, retention and margin repair.",styles["BodyText"]),
      Spacer(1,10)]
    story += [Paragraph("2. Core KPIs",styles["Heading1"])]
    tdata=[["Metric","Value"],["Orders",f"{K['orders']:,}"],["Net Revenue",money(K["revenue"])],["Profit",money(K["profit"])],
           ["Profit Margin",pct(K["margin_pct"])],["AOV",money(K["aov"])],["Return Rate",pct(K["return_rate_pct"])],
           ["Cancellation Rate",pct(K["cancel_rate_pct"])],["Return Cost",money(K["return_cost"])],
           ["Campaign Spend",money(K["campaign_spend"])],["Delivery Compensation",money(K["delivery_compensation"])]]
    tab=Table(tdata,colWidths=[190,290]); tab.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#172033")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.25,colors.grey),("PADDING",(0,0),(-1,-1),6)])); story += [tab,Spacer(1,10)]
    story += [Paragraph("3. Evidence-backed Insights",styles["Heading1"])]
    bullets=[
      f"Electronics is the scale driver: {E['electronics_revenue_share']:.1f}% of net revenue, but its observed margin is {E['electronics_margin']:.1f}%.",
      f"Grocery records {money(E['grocery_profit'])} in profit, indicating a margin/assortment problem rather than a simple growth opportunity.",
      f"West delivery delay rate is {E['west_delay_rate']:.1f}%, with {money(E['west_compensation'])} of compensation recorded in that region.",
      f"Late delivery is associated with {money(E['late_delivery_return_cost'])} of return cost across the return dataset.",
      f"The highest historical weighted campaign ROI channel in the supplied campaign data is {E['best_channel']} at {E['best_channel_roi']:.1f}%.",
      f"Medium churn risk represents {E['medium_customers']:,} customers, creating a measurable reactivation pool."
    ]
    for b in bullets: story.append(Paragraph("• "+b,styles["BodyText"]))
    story += [Spacer(1,8),Paragraph("4. ₹10 Lakh Investment Plan",styles["Heading1"])]
    rows=[["Initiative","Allocation","Scenario ROI","Expected Incremental Profit"]]
    for _,r in plan.iterrows(): rows.append([r.Initiative,money(r.Allocation),pct(r.ROI_Pct),money(r.Expected_Incremental_Profit)])
    rows.append(["TOTAL",money(plan.Allocation.sum()),pct(plan.Expected_Incremental_Profit.sum()/plan.Allocation.sum()*100),money(plan.Expected_Incremental_Profit.sum())])
    tab=Table(rows,colWidths=[190,85,85,120]); tab.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#172033")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.25,colors.grey),("PADDING",(0,0),(-1,-1),5),("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold")])); story += [tab,Spacer(1,8)]
    story += [Paragraph("5. Methodology & Assumptions",styles["Heading1"]),
      Paragraph("Channel initiatives use historical weighted profit/spend from the supplied campaign dataset. Operational initiatives use explicit scenario assumptions rather than pretending future impact is known: West delivery assumes 15% reduction in West compensation plus 5% reduction in late-delivery return cost; medium-risk reactivation assumes 12% of medium-risk customers produce one additional delivered order; Grocery margin repair assumes recovery of 40% of the observed Grocery loss. These assumptions should be stress-tested during presentation.",styles["BodyText"]),
      Spacer(1,8),Paragraph("6. Risks & Controls",styles["Heading1"]),
      Paragraph("Key risks are non-linear campaign response, attribution bias, delivery improvements not translating into retention, customer response uncertainty, and the possibility that Grocery losses have structural cost drivers. Controls: use staged pilots, cap spend by channel, monitor incremental profit rather than revenue alone, compare pre/post cohorts, and stop or reallocate funds when observed ROI falls below the scenario threshold.",styles["BodyText"]),
      Spacer(1,8),Paragraph("7. Final Recommendation",styles["Heading1"]),
      Paragraph("Use the ₹10 lakh as a portfolio of measurable experiments rather than a single bet. The proposed plan puts the largest share into channels with demonstrated historical contribution, while reserving budget for the most visible operational leaks: West delivery, medium-risk customer reactivation and Grocery margin repair. The dashboard should be used as the monitoring layer and the allocation should be revisited as actual incremental results arrive.",styles["BodyText"])]
    doc.build(story)
    return out_path
