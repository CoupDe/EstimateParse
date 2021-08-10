from Parse import Estimate, EstimateABC  # !!! Я использую одни и те-же библеотеки в разных  модулях, как правильно
# записать импорт что-бы библиотека распространялясь на все остальные модули из одного места
from Export import EstimateExport, EstimateModel

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
    print(instance.estimate_path["read_file_path"])  # Del ###
    instance.get_rows()

for instance in Estimate.all_instances:
    instance.search_data()

for instance in Estimate.all_instances:
    print(instance.__dict__)

print(Estimate.__dict__)

# choice = input("Вы хотите сформировать папку со сметами: ")
# while choice.lower() != {"n", "y"}:
#     if choice.lower() == "y":
#         print("Da")
#         break
#     elif choice.lower() == "n":
#         print("No")
#         break
#     else:
#         choice = input(f"Не вверный ввод {choice}s\nПовторите ввод: ")
ex = EstimateExport
ex.get_path(Estimate.all_instances[1])

ES = EstimateModel(**Estimate.all_instances[1].__dict__)
print(ES.__dict__)