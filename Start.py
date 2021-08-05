from Parse import Estimate, EstimateABC

anotherPath = r"C:\Users\Вадим\Desktop\Estimate\Сметы\00.АС\Копия s955096311.xlsx"
estimatePath = r"C:\Users\Вадим\Desktop\Estimate\Сметы"
# ABC expansion
rf = Estimate.get_read_file(estimatePath)
for s in rf:
    if s[1] == "abc":
        EstimateABC(s[0])
    if s[1] == "smt":
        # EstimateSMT()
        pass
Estimate.count_pack()

for instance in Estimate.all_instances:
    print(instance.estimate_path["read_file_path"])
    instance.get_rows()


rows = pe.get_rows(Estimate.all_instances[3])
print(rows)
es = EstimateABC
d = es.search_data(rows)
estimates = Estimate()
print(estimates.__dict__)
print(vars(d[0]))
print(d[0].construction_object)
print(d[1].__dict__)
