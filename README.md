# Python Apriori Lab

-------------------------

Dibuat oleh Naufal Maulana Malik

Dibimbing oleh Dr. Widodo, S.Kom., M.Kom. dan Murien Nugraheni, S.T., M.Cs.

S1 Pendidikan Teknik Informatika dan Komputer Universitas Negeri Jakarta 2024

## Deskripsi Modul

Python Apriori Lab adalah modul Apriori yang dibuat untuk menghasilkan data berupa _association rules_ dengan parameter
jalur berkas (_filepath_), nilai dukungan minimum (_minimum support value_), dan nilai kepastian minimum (_minimum 
confidence value_).

## Syarat Penggunaan Modul

1. Nama _file_ yang digunakan umumnya berekstensi .csv dan berawal dari direktori akar seperti _C:\asal_direktori_ dan 
sejenisnya.

    ```
    C:\Users\62853\PycharmProjects\apriori_lab\bin_dataset\new_binary_data.csv
    ```

2. Isian _file_ yang digunakan umumnya berisi label berupa berbagai nama produk atau barang dan di bawah label tersebut 
berisi berbagai data berupa bilangan biner (0 dan 1). 

## Prosedur Penggunaan Modul
    
 ```python3
from apriori import Apriori

filepath = r"C:\Users\62853\PycharmProjects\apriori_lab\bin_dataset\new_binary_data.csv"
apriori = Apriori(filepath=filepath, min_support=0.1, min_confidence=0.9)

apriori.start_now()

apriori.get_description_result()
apriori.get_summary()
 ```

## Hasil Penggunaan Modul

```
Iterasi 1
Jumlah data yang memenuhi minimum support :: 16 data 

Iterasi 2
Jumlah data yang memenuhi minimum support :: 60 data 
Jumlah kepingan data yang memenuhi minimum support :: 14 data 

Iterasi 3
Jumlah data yang memenuhi minimum support :: 48 data 
Jumlah kepingan data yang memenuhi minimum support :: 7 data 

Apriori Selesai
3 kali iterasi

Jumlah data yang diambil :: 163
Jumlah data yang bernilai di atas minimum support :: 124
Jumlah data yang bernilai di atas minimum confidence :: 16
Jumlah data yang valid :: 16

Min-sup        : 10 persen 
Min-confidence : 90 persen 
Iterasi        : 3 kali
```

## Simpulan Penggunaan Modul

Python Apriori Lab adalah modul Apriori yang sangat mudah digunakan dalam berbagai kasus, seperti _market basket analysis_
dan seterusnya.

## Dokumentasi

Python Apriori Lab memiliki tautan dokumentasi yang akan ditampilkan dalam beberapa waktu dekat.