from Export_Read import ImportEstimate, EstimateModel

"""Сбор и десериализация JSON"""

estimate_json = r"C:\Users\Вадим\Desktop\Estimates"
imp = ImportEstimate.read_json(estimate_json)

x = list(map(ImportEstimate.import_json, imp))
print(ImportEstimate.create_df(x))

# print(estimate)
