import psycopg2


db = psycopg2.connect(
    dbname = "library_db",
    user = "postgres",
    password = 777777,
    host = "localhost",
    port = 5432
)


cursor = db.cursor()

cursor.execute("""
     DROP TABLE IF EXISTS  books;

    CREATE TABLE IF NOT EXISTS books(
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        author VARCHAR(100),
        price INTEGER,
        quantity INTEGER
    );

""")


books =[
    ("Atom Habits", "Jeyms Clir", 75.000, 5),
    ("Binafsha Shulasi", "Usoma Muslim", 70.000, 7),
    ("The Psychology of Money", "Morgan Housel", 80.000, 4),
    ("Deep Work", "Cal Newport", 89.000, 9),
    ("Odam bolish qiyin", "O'lmas Umarbekov", 50.000, 10)
]


cursor.executemany("""INSERT INTO books(title, author, price, quantity) VALUES (%s, %s, %s, %s)""", books)


while True:
    print()
    print("KUTUB XONA BOSHQARUV TIZIMI")
    print("1. Barcha kitoblarni korish")
    print("2. Yangi kitob qo'shish")
    print("3. Kitob malumotlarini yangilash")
    print("4. Kitobni o'chirish")
    print("5. Kitobni ID boyicha qidirish")
    print("6. Kitoblarni umumiy sonini korish")
    print("0. Dasturdan chiqish")


    choose = input("Bittasini tanlang! ")


    if choose == "1":
        cursor.execute("""SELECT * FROM books ORDER BY id""")
        books = cursor.fetchall()

        if len(books) == 0:
            print("Kitob yoq!")
        else:
            print(f"ID: {books[0]}, Name: {books[1]}, muallifi: {books[2]}, Narxi: {books[3]}, Miqdori: {books[4]}")

    elif choose == "2":
        title = input("Kitob nomini kiriting:  ")
        author = input("Kitob muallifini kiriting: ")
        price = int(input("Kitob narxini kiriting: "))
        quantity = int(input("Kitob nechta yoki miqdorini kiriting: "))

        cursor.execute("""INSERT INTO books(title, author, price, quantity) VALUES (%s, %s, %s, %s)""", (title, author, price, quantity))

        db.commit()
        print("Kitob qoshildi")



    elif choose == "3":
        book_id = int(input("Kitob ID sini kiriting: "))

        cursor.execute("""SELECT * FROM books WHERE id = %s""", (book_id,))
        book = cursor.fetchone()

        if book:
            price = int(input("Yangi kitob narxini kiriting: "))
            quantity = int(input("Yangi miqdorni kiriting: "))

            cursor.execute("""UPDATE books SET price = %s, quantity = %s WHERE id = %s""", (price, quantity, book_id))

            db.commit()
            print("Kitob yangilandi")
        else:
            print("Bunday ID li kitob yo'q")


    elif choose == "4":
        book_id = int(input("Kitob ID sini kiriting: "))

        cursor.execute("""SELECT * FROM books WHERE id = %s""", (book_id,))
        book = cursor.fetchone()


        if book:
            answer = input("Kitob ni rostdan ochirasmi (ha/yoq) ")
            if answer == "ha":
                cursor.execute("""SELECT * FROM books WHERE id = %s""", (book_id,))

                db.commit()
                print("Kitob ochirildi")
            else:
                print("ochirish bekor qilindi ")
        else:
            print("Kitob topilmadi")


    elif choose == "5":
        book_id = int(input("Kitob ID sini kiriting: "))

        cursor.execute("""SELECT * FROM books WHERE id = %s""", (int(book_id),))
        book = cursor.fetchone()


        if book:
            print(f"ID: {book[0]}, Name: {book[1]}, Muallifi: {book[2]}, Narxi: {book[3]}, Miqdori: {book[4]}")
        else:
            print("Kitob topilmadi")

    elif choose == "6":
        cursor.execute("""SELECT SUM(quantity) FROM books""")
        hammasi = cursor.fetchone()[0]
        print(f"Kutub honadagi kitoblar umumiy soni: {hammasi}")


    elif choose == "0":
        print("Dasturdan chiqildi")
        break
    

db.commit()
db.close()