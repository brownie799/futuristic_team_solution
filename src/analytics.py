
import pandas as pd
import numpy as np

def build_models(d):
    o=d["orders"]; p=d["products"]; c=d["customers"]; m=d["campaigns"]; r=d["returns"]; dl=d["delivery"]
    order_product=o.merge(p[["Product_ID","Product_Name","Category","Subcategory","Brand","Profit_Per_Unit",
                              "Return_Rate_Pct","Stock_Quantity","Reorder_Level"]],on="Product_ID",how="left")
    return order_product

def kpis(d):
    o=d["orders"]; r=d["returns"]; dl=d["delivery"]; m=d["campaigns"]
    rev=o["Net_Revenue"].sum(); profit=o["Profit"].sum()
    return {
        "orders": int(len(o)), "delivered_orders": int((o["Order_Status"]=="Delivered").sum()),
        "revenue": float(rev), "profit": float(profit),
        "margin_pct": float(profit/rev*100 if rev else 0),
        "aov": float(rev/len(o) if len(o) else 0),
        "return_rate_pct": float(o["Return_Flag"].mean()*100),
        "cancel_rate_pct": float(o["Cancellation_Flag"].mean()*100),
        "return_cost": float(r["Total_Return_Cost"].sum()),
        "campaign_spend": float(m["Actual_Spend"].sum()),
        "campaign_profit": float(m["Profit_Generated"].sum()),
        "delivery_compensation": float(dl["Customer_Compensation"].sum())
    }

def category_analysis(d):
    x=build_models(d)
    g=x.groupby("Category").agg(Orders=("Order_ID","count"),Revenue=("Net_Revenue","sum"),
        Profit=("Profit","sum"),Quantity=("Quantity","sum"),Returns=("Return_Flag","sum")).reset_index()
    g["Margin_Pct"]=np.where(g.Revenue!=0,g.Profit/g.Revenue*100,0)
    g["Return_Rate_Pct"]=np.where(g.Orders!=0,g.Returns/g.Orders*100,0)
    return g.sort_values("Profit",ascending=False)

def region_delivery_analysis(d):
    x=d["delivery"].groupby("Region").agg(
        Deliveries=("Delivery_ID","count"),
        Delay_Rate=("Delay_Days",lambda s:(s>0).mean()*100),
        Avg_Delay=("Delay_Days","mean"),
        Compensation=("Customer_Compensation","sum"),
        Damage_Rate=("Damage_Flag","mean")
    ).reset_index()
    x["Damage_Rate"]=x["Damage_Rate"]*100
    return x.sort_values("Delay_Rate",ascending=False)

def channel_analysis(d):
    x=d["campaigns"].groupby("Channel").agg(
        Campaigns=("Campaign_ID","count"),Spend=("Actual_Spend","sum"),
        Revenue=("Revenue_Generated","sum"),Profit=("Profit_Generated","sum"),
        Avg_ROAS=("ROAS","mean"),Avg_ROI_Pct=("ROI_Pct","mean"),
        Avg_Conversion_Pct=("Conversion_Rate_Pct","mean")
    ).reset_index()
    x["Weighted_ROI_Pct"]=np.where(x.Spend!=0,x.Profit/x.Spend*100,0)
    return x.sort_values("Weighted_ROI_Pct",ascending=False)

def customer_analysis(d):
    c=d["customers"]
    return c.groupby("Churn_Risk").agg(
        Customers=("Customer_ID","count"),Avg_Sessions=("Sessions_Last90d","mean"),
        Avg_Carts=("Cart_Adds","mean"),Avg_Checkout=("Checkout_Initiated","mean"),
        Avg_Purchases=("Purchases_Last90d","mean"),Avg_Satisfaction=("Customer_Satisfaction","mean")
    ).reset_index()

def product_analysis(d):
    x=build_models(d).groupby(["Product_ID","Product_Name","Category"]).agg(
        Orders=("Order_ID","count"),Revenue=("Net_Revenue","sum"),Profit=("Profit","sum"),
        Quantity=("Quantity","sum"),Returns=("Return_Flag","sum")
    ).reset_index()
    p=d["products"][["Product_ID","Profit_Margin_Pct","Return_Rate_Pct","Stock_Quantity","Reorder_Level"]]
    return x.merge(p,on="Product_ID",how="left")

def return_analysis(d):
    return d["returns"].groupby("Return_Reason").agg(
        Returns=("Return_ID","count"),Total_Cost=("Total_Return_Cost","sum")
    ).reset_index().sort_values("Total_Cost",ascending=False)

def evidence(d):
    k=kpis(d); cat=category_analysis(d); reg=region_delivery_analysis(d); ch=channel_analysis(d)
    cust=customer_analysis(d); rr=return_analysis(d)
    electronics=cat.loc[cat.Category=="Electronics"].iloc[0]
    grocery=cat.loc[cat.Category=="Grocery"].iloc[0]
    west=reg.loc[reg.Region=="West"].iloc[0]
    medium=cust.loc[cust.Churn_Risk=="Medium"].iloc[0]
    late=rr.loc[rr.Return_Reason=="Late delivery"].iloc[0]
    return {
      "revenue":k["revenue"],"profit":k["profit"],"margin":k["margin_pct"],
      "electronics_revenue_share":float(electronics.Revenue/k["revenue"]*100),
      "electronics_margin":float(electronics.Margin_Pct),
      "grocery_profit":float(grocery.Profit),
      "west_delay_rate":float(west.Delay_Rate),
      "west_compensation":float(west.Compensation),
      "medium_customers":int(medium.Customers),
      "late_delivery_return_cost":float(late.Total_Cost),
      "best_channel":str(ch.iloc[0].Channel),
      "best_channel_roi":float(ch.iloc[0].Weighted_ROI_Pct)
    }
