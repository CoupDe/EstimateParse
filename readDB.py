from Export_Read import ImportEstimate, EstimateModel

"""Сбор и десериализация JSON"""

estimate_json = r"C:\Users\Вадим\Desktop\Estimates"
imp = ImportEstimate.read_json(estimate_json)

with open(imp[0], encoding="utf-8") as f:
    estimate = ImportEstimate.import_json(f)
    print(estimate.price_year)

# print(estimate)
