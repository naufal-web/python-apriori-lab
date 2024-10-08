class OneHotEncoding:

    def __init__(self, source, destination):

        self.source = source
        self.destination = destination

    def encode(self):

        import _csv

        items = []
        transactions = []
        binary_data = []

        with open(self.source, encoding="UTF-8") as source_file:
            csv_reader = _csv.reader(source_file)  # O(1)
            try:
                for index, transaction in list(csv_reader)[1:]:  # O(n)
                    transactions.append(transaction)
                    for item in transaction.split(", "):  # O(m)
                        if item not in items:
                            items.append(item)
            except ValueError:
                print("Belum Bisa")

        for transaction in transactions:
            encoded_data = []
            for item in items:
                if item in transaction.split(", "):
                    encoded_data.append(1)
                else:
                    encoded_data.append(0)
            binary_data.append(encoded_data)

        try:
            with open(self.destination, encoding="UTF-8", mode="w", newline="") as destination_file:
                csv_writer = _csv.writer(destination_file)
                csv_writer.writerow(items)
                csv_writer.writerows(binary_data)
        except FileNotFoundError:
            with open(self.destination, encoding="UTF-8", mode="x") as destination_file:
                pass


if __name__ == '__main__':
    source_path = r"C:\Users\62853\PycharmProjects\apriori_lab\dataset\0001.csv"
    destination_path = r"C:\Users\62853\PycharmProjects\apriori_lab\bin_dataset\new_binary_data_1.csv"

    one_hot_encoding_hub = OneHotEncoding(source=source_path, destination=destination_path)
    one_hot_encoding_hub.encode()
