import os
import _csv

current_path = os.getcwd()  # O(1)
source_filepath = r"dataset\0002.csv"  # O(1)
destination_filepath = r"bin_dataset\new_binary_data.csv"

source = os.path.join(current_path, source_filepath)  # O(1)
destination = os.path.join(current_path, destination_filepath)


def dig_items_from_(source_path, destination_path):
    items = []
    transactions = []
    binary_data = []

    with open(source_path, encoding="UTF-8") as source_file:
        csv_reader = _csv.reader(source_file)  # O(1)
        for index, transaction in list(csv_reader)[1:]:  # O(n)
            transactions.append(transaction)
            for item in transaction.split(", "):  # O(m)
                if item not in items:
                    items.append(item)

    for transaction in transactions:
        encoded_data = []
        for item in items:
            if item in transaction.split(", "):
                encoded_data.append(1)
            else:
                encoded_data.append(0)
        binary_data.append(encoded_data)

    try:
        with open(destination_path, encoding="UTF-8", mode="w", newline="") as destination_file:
            csv_writer = _csv.writer(destination_file)
            csv_writer.writerow(items)
            csv_writer.writerows(binary_data)
    except FileNotFoundError:
        with open(destination_path, encoding="UTF-8", mode="x") as destination_file:
            pass


def item_joining(items_before_join, items_pruned):  # Complexity Algorithm :: O(mn)
    items_after_join = []  # O(1)

    for item_before_join in items_before_join:  # O(m)
        for item in items_pruned:  # O(n)
            lst = []  # O(1)
            if item not in item_before_join.split(", "):
                lst.extend(item_before_join.split(", "))  # O(1)
                lst.append(item)  # O(1)
                # print(lst)
                if lst not in items_after_join:
                    items_after_join.append(lst)  # O(1)

    return items_after_join


# O(nk)
def item_pruning(items_before_join):  # Complexity Algorithm :: O(m*n)

    items_pruned = []  # O(1)

    for item_before_join in items_before_join:     # O(n)
        for item in item_before_join.split(", "):   # O(k)
            if item not in items_pruned:                # O(1)
                items_pruned.append(item)                   # O(1)

    return items_pruned  # O(mn^2)


# Complexity Algorithm :: # O(n)
def item_selecting_with_minimum_support(count_of_data, items_by_number, minimum_support, iteration):
    items_before_joining = []  # O(1)
    items_which_above_minimum_support = {}  # O(1)

    iteration -= 1  # O(1)

    for key, value in items_by_number.items():                          # O(n)
        support_value = round(value / count_of_data, 3)                     # O(1)
        if support_value >= minimum_support:                                # O(1)
            if key.count(", ") == iteration:                                    # O(1)
                items_before_joining.append(key)                                    # O(1)
                items_which_above_minimum_support[key] = support_value              # O(1)

    # O(n), O(n)

    return items_before_joining, items_which_above_minimum_support


# O(n^2)
def items_counting(initial):  # Complexity Algorithm :: O(n^2)
    items_by_number = {}  # O(1)

    # Complexity Algorithm :: O(n(2+n)) >> O(2n+n^2) >> O(n^2) or O(2n)
    for key, value in initial.items():  # O(n)
        count = 0                           # O(1)
        for val in value:                   # O(n)
            if val == 1:                        # O(1)
                count += 1
        items_by_number[key] = count        # O(1)

    return items_by_number


# O(2n)
def items_binary_list_generator(nested_list):  # Algorithm Complexity :: O(3n)
    binaries = []
    for i in range(min(map(len, nested_list))):  # O(n)
        ls = list(lst[i] for lst in nested_list)  # O(1)
        if ls == [1 for ele in range(len(nested_list))]:
            binaries.append(1)  # O(1)
        else:
            binaries.append(0)  # O(1)

    return binaries


# O(n^2)
def initial_generator(items_joined, initial):
    for item_joined in items_joined:  # O(n)
        lst = []  # O(1)
        for item in item_joined:  # O(m)
            lst.append(initial[item])  # O(1)
        initial[", ".join(item_joined)] = items_binary_list_generator(lst)  # O(3n)

    return initial


class Apriori:

    def __init__(self, filepath, min_support, min_confidence):
        self.items_which_above_support_value = {}
        self.items_which_above_confidence_value = {}
        self.items_which_above_lift_ratio = {}
        self.items_dictionary = {}
        self.filepath = filepath                          # O(1)
        self.minimum_support = min_support                # O(1)
        self.minimum_confidence = min_confidence          # O(1)
        self.rows = []                                    # O(1)
        self.items = None                                 # O(1)
        self.items_by_number = {}
        self.initial = {}
        self.iteration = 0

        with open(self.filepath, encoding="UTF-8") as source_file:    # O(1)
            csv_reader = _csv.reader(source_file)                       # O(1)
            self.items = list(csv_reader)[0]                            # O(n)

        # O(n)

        with open(self.filepath, encoding="UTF-8") as source_file:  # O(1)
            csv_reader = _csv.reader(source_file)                       # O(1)
            for row in list(csv_reader)[1:]:                            # O(m)
                integers = []                                               # O(1)
                for binary in row:                                          # O(n)
                    integers.append(int(binary))                                # O(1)
                self.rows.append(integers)                                  # O(1)

        # O(1+m(2+n)) >>> O(1+2m+mn) >>> O(mn)

    def start_now(self, maximum_iteration=10):

        self.initial = {}                             # O(1)
        for i in range(len(self.items)):              # O(n)
            lst = []                                    # O(1)
            for row in self.rows:                       # O(mn)
                lst.append(row[i])                          # O(1)

            self.initial[self.items[i]] = lst         # O(1)

        # O(2 + n(1+mn)) >>> O(2 + n + mn^2) >>> O(mn^2)

        nested_dict = []   # O(1)

        it = 1

        # O(1)
        print(f"Iterasi {it}")

        # O(1)
        self.items_by_number = items_counting(self.initial)  # O(mn^2) = O(1)

        # O(1)
        output = item_selecting_with_minimum_support(len(self.rows), self.items_by_number, self.minimum_support, it)
        items_selected, self.items_dictionary = output  # O(1)

        nested_dict.append(self.items_dictionary)  # O(1)
        print(f"Jumlah data yang memenuhi minimum support :: {len(items_selected)} data ")  # O(1)
        print()
        items_joined = item_joining(items_selected, items_selected)  # O(n^2)

        self.initial = initial_generator(items_joined, self.initial)  # O(n^2)
        items_joined.clear()  # O(1)

        it = 2  # O(1)
        apriori = True
        # O(n log n)
        while apriori:   # k = ???
            self.items_by_number = items_counting(self.initial)  # O(n^2)
            output = item_selecting_with_minimum_support(len(self.rows), self.items_by_number, self.minimum_support, it)
            items_selected, self.items_dictionary = output  # O(n)
            items_pruned = item_pruning(items_selected)  # O(n/2)
            nested_dict.append(self.items_dictionary)       # O(n/2)
            items_joined = item_joining(items_selected, items_pruned)  # O(n^2/2)
            self.initial = initial_generator(items_joined, self.initial)  # O(n^(k+2)/2)
            if len(items_selected) != 0 and len(items_pruned) != 0 and it <= maximum_iteration:
                print(f"Iterasi {it}")  # O(1)
                print(f"Jumlah data yang memenuhi minimum support :: {len(items_selected)} data ")  # O(1)
                print(f"Jumlah kepingan data yang memenuhi minimum support :: {len(items_pruned)} data ")  # O(1)
                apriori = True
                print()
            else:
                apriori = False
                self.iteration = it - 1
                print("Apriori Selesai")
                print(f"{self.iteration} kali iterasi")

            it += 1

        # (2 + n^2 + 3n + 3n + n + 2 + n^2 + 3n^3 + 1 + n^2 + 3)^k = 1
        # (5 + 3n^3 + 2n^2 + 6n)^k = 1
        # (3n^3 + 2n^2 + 6n)^k = 1
        # (n(3n^2 + 2n + 6))^k = 1
        # (n(3n 3)(n 2)))

        self.items_which_above_support_value = {}
        for dct in nested_dict:
            for key, value in dct.items():
                self.items_which_above_support_value[key] = value

        self.items_which_above_confidence_value = {}
        for items_set, support_value in self.items_which_above_support_value.items():
            for i in range(items_set.count(", ")):
                antecedent = ", ".join(items_set.split(", ")[:i + 1])
                consequent = ", ".join(items_set.split(", ")[i + 1:])
                rules = f"{antecedent} ==> {consequent}"
                confidence_value = round(support_value / self.items_which_above_support_value[antecedent], 3)
                if confidence_value >= self.minimum_confidence:
                    self.items_which_above_confidence_value[rules] = confidence_value

        self.items_which_above_lift_ratio = {}
        for items_set, confidence_value in self.items_which_above_confidence_value.items():
            consequent = items_set.split(" ==> ")[1]
            lift_ratio = round(confidence_value / self.items_which_above_support_value[consequent], 3)
            if lift_ratio >= 1.00:
                self.items_which_above_lift_ratio[items_set] = lift_ratio

    def get_summary(self):
        print(f"Min-sup        : {int(self.minimum_support * 100)} persen ")
        print(f"Min-confidence : {int(self.minimum_confidence * 100)} persen ")
        print(f"Iterasi        : {self.iteration} kali ")

    def show_items_which_above_minimum_support(self):
        i = 0
        for key, value in self.items_which_above_support_value.items():
            print(i + 1, key, value)
            i += 1
        print()

    def show_items_which_above_minimum_confidence(self):
        i = 0
        for key, value in self.items_which_above_confidence_value.items():
            print(i + 1, key, value)
            i += 1
        print()

    def show_items_which_above_lift_ratio(self):
        i = 0
        for key, value in self.items_which_above_lift_ratio.items():
            print(i + 1, key, value)
            i += 1
        print()

    def get_description_result(self):
        print()
        print(f"Jumlah data yang diambil :: {len(self.rows)}")
        print(f"Jumlah data yang bernilai di atas minimum support :: {len(self.items_which_above_support_value)}")
        print(f"Jumlah data yang bernilai di atas minimum confidence :: {len(self.items_which_above_confidence_value)}")
        print(f"Jumlah data yang valid :: {len(self.items_which_above_lift_ratio)}")
        print()
