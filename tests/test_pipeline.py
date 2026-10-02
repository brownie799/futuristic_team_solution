
from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.analytics import kpis
from src.investment_optimizer import investment_plan

def test_load_and_clean():
    d=clean_data(load_data())
    assert len(d["orders"])==30000
    assert len(d["products"])==500
    assert len(d["customers"])==5000

def test_budget():
    d=clean_data(load_data())
    p=investment_plan(d)
    assert p["Allocation"].sum()==1000000
    assert (p["Allocation"]>0).all()
