from Export_Read import ImportEstimate

"""Сбор и десериализация JSON"""

estimate_json = r"C:\Users\Вадим\Desktop\Estimates"
imp = ImportEstimate
print(len(imp.read_json(estimate_json)), imp.read_json(estimate_json))