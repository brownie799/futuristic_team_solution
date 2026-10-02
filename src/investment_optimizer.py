
import pandas as pd
from .analytics import channel_analysis, category_analysis, region_delivery_analysis, customer_analysis, return_analysis, kpis

BUDGET = 1_000_000

def investment_plan(d):
    ch=channel_analysis(d); cat=category_analysis(d); reg=region_delivery_analysis(d)
    cust=customer_analysis(d); rr=return_analysis(d)
    # Scenario assumptions are explicit and conservative enough to audit.
    # Channel ROI is historical profit/spend from the supplied campaign data.
    def chroi(name):
        row=ch[ch.Channel==name]
        return float(row.iloc[0].Weighted_ROI_Pct/100) if not row.empty else 0
    # Operational levers use scenario savings / incremental profit estimates tied to observed losses.
    west=reg[reg.Region=="West"].iloc[0]
    grocery=cat[cat.Category=="Grocery"].iloc[0]
    medium=cust[cust.Churn_Risk=="Medium"].iloc[0]
    avg_delivered_profit=d["orders"].loc[d["orders"].Order_Status=="Delivered","Profit"].mean()
    late_cost=rr[rr.Return_Reason=="Late delivery"].iloc[0].Total_Cost
    levers=[
      ("Referral growth",350000,chroi("Referral"),"Historical weighted campaign ROI"),
      ("Email retention campaigns",200000,chroi("Email"),"Historical weighted campaign ROI"),
      ("Google Ads efficiency scale",100000,chroi("Google Ads"),"Historical weighted campaign ROI"),
      ("West delivery reliability",150000,(west.Compensation*0.15 + late_cost*0.05)/150000,
       "Scenario: 15% West compensation reduction + 5% late-delivery return-cost reduction"),
      ("Medium-risk customer reactivation",100000,(medium.Customers*0.12*avg_delivered_profit)/100000,
       "Scenario: 12% of medium-risk customers generate one incremental delivered order"),
      ("Grocery margin repair",100000,max(0,(-grocery.Profit)*0.40)/100000,
       "Scenario: recover 40% of observed Grocery loss through pricing/assortment controls")
    ]
    plan=pd.DataFrame(levers,columns=["Initiative","Allocation","Expected_ROI","Evidence_or_Assumption"])
    plan["Expected_Incremental_Profit"]=plan.Allocation*plan.Expected_ROI
    plan["Expected_Total_Value"]=plan.Allocation+plan.Expected_Incremental_Profit
    plan["ROI_Pct"]=plan.Expected_ROI*100
    return plan

def allocation_summary(d):
    plan=investment_plan(d)
    return {
        "budget":float(plan.Allocation.sum()),
        "expected_incremental_profit":float(plan.Expected_Incremental_Profit.sum()),
        "expected_roi_pct":float(plan.Expected_Incremental_Profit.sum()/plan.Allocation.sum()*100)
    }
