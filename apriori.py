# import os
import _csv


# Time Complexity :: O(mn)
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


# Time Complexity :: O(m*n^2)
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


# Time Complexity :: O(n^2)
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


# Time Complexity ::: O(n)
def items_binary_list_generator(nested_list):  # Algorithm Complexity :: O(3n)
    binaries = []
    for i in range(min(map(len, nested_list))):  # O(n)
        ls = list(lst[i] for lst in nested_list)  # O(1)
        if ls == [1 for ele in range(len(nested_list))]:
            binaries.append(1)  # O(1)
        else:
            binaries.append(0)  # O(1)

    return binaries


# Time Complexity ::: O(n*m)
def initial_generator(items_joined, initial):
    for item_joined in items_joined:  # O(n)
        lst = []  # O(1)
        for item in item_joined:  # O(m)
            lst.append(initial[item])  # O(1)
        initial[", ".join(item_joined)] = items_binary_list_generator(lst)  # O(3n)

    return initial


class Apriori:

    def __init__(self, path, min_support, min_confidence):
        self.items_which_above_support_value = {}
        self.items_which_above_confidence_value = {}
        self.items_which_above_lift_ratio = {}
        self.items_dictionary = {}
        self.filepath = path                          # O(1)
        self.minimum_support = min_support                # O(1)
        self.minimum_confidence = min_confidence          # O(1)
        self.rows = []                                    # O(1)
        self.items = None                                 # O(1)
        self.items_by_number = {}
        self.initial = {}
        self.iteration = 0

        # Time Complexity O(1)
        with open(self.filepath, encoding="UTF-8") as source_file:    # O(1)
            csv_reader = _csv.reader(source_file)                       # O(1)
            self.items = list(csv_reader)[0]                            # O(n)

        # Time Complexity O(m * n)
        with open(self.filepath, encoding="UTF-8") as source_file:  # O(1)
            csv_reader = _csv.reader(source_file)                       # O(1)
            for row in list(csv_reader)[1:]:                            # O(m)
                integers = []                                               # O(1)
                for binary in row:                                          # O(n)
                    integers.append(int(binary))                                # O(1)
                self.rows.append(integers)                                  # O(1)

        # From Line 110 Into Line 121, The Time Complexity of LOC is O(m * n)

    def start_now(self, maximum_iteration=10):

        # Time Complexity :: O(m * n)
        self.initial = {}
        for i in range(len(self.items)):
            lst = []
            for row in self.rows:
                lst.append(row[i])

            self.initial[self.items[i]] = lst

        # Time Complexity ::: O(1)
        nested_dict = []

        # Time Complexity ::: O(1)
        it = 1

        # Time Complexity ::: O(1)
        print(f"Iterasi {it}")

        # Time Complexity ::: O(1)
        self.items_by_number = items_counting(self.initial)  # O(n ^ 2)

        # Time Complexity ::: O(n)
        output = item_selecting_with_minimum_support(len(self.rows), self.items_by_number, self.minimum_support, it)

        # Time Complexity for output variable
        # O(1) = O(1 + n^2 + 1 + 1)
        # O(1) = O(3 + n^2)
        # O(1) = O(n^2)
        # O(n^2) = O(1)
        # O(n) = O(1)

        # Simplified Time Complexity
        # O(n)
        items_selected, self.items_dictionary = output

        # Time Complexity ::: O(n)
        nested_dict.append(self.items_dictionary)  # O(1)

        print(f"Jumlah data yang memenuhi minimum support :: {len(items_selected)} data ")  # O(1)
        print()

        # Time Complexity ::: O(n)
        items_joined = item_joining(items_selected, items_selected)

        # Time Complexity ::: O(m * n)
        self.initial = initial_generator(items_joined, self.initial)

        # Time Complexity ::: O(1)
        items_joined.clear()

        # Time Complexity ::: O(1)
        it = 2

        # Time Complexity ::: O(1)
        ignite_apriori = True

        # Time Complexity ::: O(n^(n log m))
        while ignite_apriori:
            # Time Complexity ::: O(n^2)
            self.items_by_number = items_counting(self.initial)

            # Time Complexity ::: O(n)
            output = item_selecting_with_minimum_support(len(self.rows), self.items_by_number, self.minimum_support, it)
            items_selected, self.items_dictionary = output

            # Time Complexity ::: O(mn^2)
            items_pruned = item_pruning(items_selected)

            # Time Complexity ::: O(n)
            nested_dict.append(self.items_dictionary)

            # Time Complexity ::: O(mn)
            items_joined = item_joining(items_selected, items_pruned)

            # Time Complexity ::: O(nm)
            self.initial = initial_generator(items_joined, self.initial)

            # Time Complexity ::: O(1)
            if len(items_selected) != 0 and len(items_pruned) != 0 and it <= maximum_iteration:
                print(f"Iterasi {it}")
                print(f"Jumlah data yang memenuhi minimum support :: {len(items_selected)} data ")
                print(f"Jumlah kepingan data yang memenuhi minimum support :: {len(items_pruned)} data ")
                ignite_apriori = True
                print()
            else:
                ignite_apriori = False
                self.iteration = it - 1
                print("Apriori Selesai")
                print(f"{self.iteration} kali iterasi")

            # Time Complexity ::: O(1)
            it += 1

        # Time Complexity ::: O(n*m)
        self.items_which_above_support_value = {}
        for dct in nested_dict:
            for key, value in dct.items():
                self.items_which_above_support_value[key] = value

        # Time Complexity ::: O(n^2)
        self.items_which_above_confidence_value = {}
        for items_set, support_value in self.items_which_above_support_value.items():
            for i in range(items_set.count(", ")):
                antecedent = ", ".join(items_set.split(", ")[:i + 1])
                consequent = ", ".join(items_set.split(", ")[i + 1:])
                rules = f"{antecedent} ==> {consequent}"
                confidence_value = round(support_value / self.items_which_above_support_value[antecedent], 3)
                if confidence_value >= self.minimum_confidence:
                    self.items_which_above_confidence_value[rules] = confidence_value

        # Time Complexity ::: O(n)
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


if __name__ == '__main__':
    filepath = r"C:\Users\62853\PycharmProjects\apriori_lab\bin_dataset\new_binary_data.csv"

    # Time Complexity :: O(m * n)
    apriori = Apriori(path=filepath, min_support=0.1, min_confidence=0.9)

    # Time Complexity :: O(n^(log m base n))
    apriori.start_now()

    # Time Complexity :: O(1)
    apriori.get_description_result()

    # Time Complexity :: O(1)
    apriori.get_summary()

    # Overall Time Complexity :: O(n^(log m base n))
