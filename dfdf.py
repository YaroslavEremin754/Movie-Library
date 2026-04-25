import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "movies.json"


def load_movies():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_movies():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

def add_movie():
    title = entry_title.get().strip()
    genre = entry_genre.get().strip()
    year = entry_year.get().strip()
    rating = entry_rating.get().strip()

    if not title or not genre or not year or not rating:
        messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
        return

    if not year.isdigit() or int(year) < 1895 or int(year) > 2100:
        messagebox.showerror("Ошибка", "Год должен быть числом от 1895 до 2100!")
        return

    if not (rating.replace('.', '', 1).isdigit() and 0 <= float(rating) <= 10):
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
        return

    movies.append({
        "title": title,
        "genre": genre,
        "year": int(year),
        "rating": float(rating)
    })
    save_movies()
    update_table()
    clear_entries()

def clear_entries():
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)

def update_table():
    for i in tree.get_children():
        tree.delete(i)
    
    for movie in movies:
        tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

def on_filter():
    genre = entry_filter_genre.get().strip()
    year = entry_filter_year.get().strip()
    
    for i in tree.get_children():
        tree.delete(i)
    
    for movie in movies:
        if genre and movie["genre"].lower() != genre.lower():
            continue
        if year and str(movie["year"]) != year:
            continue
        tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))


movies = load_movies()


root = tk.Tk()
root.title("Movie Library")
root.geometry("800x500")


tk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_title = tk.Entry(root, width=40)
entry_title.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_genre = tk.Entry(root, width=40)
entry_genre.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Год выпуска:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_year = tk.Entry(root, width=40)
entry_year.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Рейтинг:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_rating = tk.Entry(root, width=40)
entry_rating.grid(row=3, column=1, padx=5, pady=5)

btn_add = tk.Button(root, text="Добавить фильм", command=add_movie)
btn_add.grid(row=4, columnspan=2, pady=10)


tk.Label(root, text="Фильтр по жанру:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
entry_filter_genre = tk.Entry(root, width=40)
entry_filter_genre.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Фильтр по году:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
entry_filter_year = tk.Entry(root, width=40)
entry_filter_year.grid(row=6, column=1, padx=5, pady=5)

btn_filter = tk.Button(root, text="Применить фильтр", command=on_filter)
btn_filter.grid(row=7, columnspan=2, pady=10)


columns = ("Название", "Жанр", "Год", "Рейтинг")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)
tree.grid(row=8, columnspan=2, padx=10, pady=10)


update_table()

root.mainloop()
