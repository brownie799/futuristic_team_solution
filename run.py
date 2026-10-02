
from pathlib import Path
from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.analytics import kpis, category_analysis, region_delivery_analysis, channel_analysis, customer_analysis, return_analysis, product_analysis
from src.investment_optimizer import investment_plan, allocation_summary
from src.report_generator import generate_report

ROOT=Path(__file__).resolve()
d=clean_data(load_data())
out=ROOT/"outputs"
(out/"tables").mkdir(parents=True,exist_ok=True)
for name,df in {
    "category_analysis":category_analysis(d),"region_delivery":region_delivery_analysis(d),
    "channel_analysis":channel_analysis(d),"customer_churn":customer_analysis(d),
    "return_analysis":return_analysis(d),"product_analysis":product_analysis(d),
    "investment_plan":investment_plan(d)
}.items():
    df.to_csv(out/"tables"/f"{name}.csv",index=False)
import json
(out/"final_results").mkdir(parents=True,exist_ok=True)
(out/"final_results"/"kpis.json").write_text(json.dumps(kpis(d),indent=2))
(out/"final_results"/"investment_summary.json").write_text(json.dumps(allocation_summary(d),indent=2))
generate_report(d,out/"../report/ACCkart_Analytical_Report.pdf")
print("Pipeline completed.")
print(json.dumps(allocation_summary(d),indent=2))
