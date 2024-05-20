import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import shutil
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


def open_camera():
    try:
        subprocess.run(["python", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to open camera:\n{e}")


def add_data_to_database(student_info):
    try:
        # Firebase'e bağlan
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://faceattendacerealtime-43c65-default-rtdb.firebaseio.com/"})
        ref = db.reference('Students')

        # Yeni öğrenci bilgilerini Firebase veritabanına ekle
        ref.push(student_info)

        messagebox.showinfo("Bilgi", "Veritabanına başarıyla eklendi!")
    except Exception as e:
        messagebox.showerror("Hata", f"Bilgi eklenirken bir hata oluştu:\n{e}")


def show_data_entry_form(file_path):
    # Yeni bir Tkinter penceresi oluştur
    data_entry_window = tk.Toplevel()
    data_entry_window.title("Öğrenci Bilgi Girişi")
    data_entry_window.geometry("400x400")

    # Etiketler ve giriş kutuları oluştur
    ttk.Label(data_entry_window, text="Adı Soyadı:").pack()
    name_entry = ttk.Entry(data_entry_window)
    name_entry.pack()

    ttk.Label(data_entry_window, text="Bölümü:").pack()
    major_entry = ttk.Entry(data_entry_window)
    major_entry.pack()

    ttk.Label(data_entry_window, text="Başlama Yılı:").pack()
    starting_year_entry = ttk.Entry(data_entry_window)
    starting_year_entry.pack()

    ttk.Label(data_entry_window, text="Toplam Katılım:").pack()
    total_attendance_entry = ttk.Entry(data_entry_window)
    total_attendance_entry.pack()

    ttk.Label(data_entry_window, text="Statü:").pack()
    standing_entry = ttk.Entry(data_entry_window)
    standing_entry.pack()

    ttk.Label(data_entry_window, text="Sınıfı:").pack()
    year_entry = ttk.Entry(data_entry_window)
    year_entry.pack()

    ttk.Label(data_entry_window, text="Son Katılım Zamanı:").pack()
    last_attendance_time_entry = ttk.Entry(data_entry_window)
    last_attendance_time_entry.pack()

    def add_to_database():
        # Kullanıcının girdiği bilgileri al
        student_info = {
            "name": name_entry.get(),
            "major": major_entry.get(),
            "starting_year": int(starting_year_entry.get()),
            "total_attendance": int(total_attendance_entry.get()),
            "standing": standing_entry.get(),
            "year": year_entry.get(),
            "last_attendance_time": last_attendance_time_entry.get()
        }

        # Veritabanına öğrenci bilgilerini ekle
        add_data_to_database(student_info)

        # Pencereyi kapat
        data_entry_window.destroy()

    # Kaydet butonu
    save_button = ttk.Button(data_entry_window, text="Kaydet", command=add_to_database)
    save_button.pack(pady=10)


def new_user():
    file_path = filedialog.askopenfilename(
        title="Resim Dosyası Seçinn",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    if file_path:
        try:
            # Dosyanın adını ve uzantısını al
            file_name = os.path.basename(file_path)
            # Dosyanın kaydedileceği yeni dizini belirle
            destination_dir = r"C:\Users\alii2\PycharmProjects\pythonProject1\Images"
            os.makedirs(destination_dir, exist_ok=True)
            # Dosyanın kaydedileceği yeni yolu belirle
            destination_path = os.path.join(destination_dir, file_name)
            # Dosyayı belirtilen konuma kopyala
            shutil.copy(file_path, destination_path)
            messagebox.showinfo("Dosya Yüklendi", f"Dosya başarıyla yüklendi: {destination_path}")

            # Öğrenci adını dosya adından al
            student_name = os.path.splitext(file_name)[0]

            # Veritabanına eklemek için kullanıcıdan bilgi girişi iste
            show_data_entry_form(destination_path)
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", f"Dosya yüklenirken bir hata oluştu: {e}")
    else:
        messagebox.showwarning("Dosya Seçilmedi", "Herhangi bir dosya seçilmedi.")


# Tkinter arayüzü oluşturma
root = tk.Tk()
root.title("Kamera Arayüzü")
root.geometry("700x600")
root.resizable(False, False)
root.configure(bg='#2ecc71')

# Stil oluşturma
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14), padding=10)
style.configure("TLabel", font=("Helvetica", 16), background='#2ecc71', foreground='white')

# Başlık etiketi
title_label = ttk.Label(root, text="Kamera Kontrol Arayüzü", style="TLabel")
title_label.pack(pady=20)

# Buton oluşturma
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

open_camera_button = ttk.Button(button_frame, text="Kamerayı Aç", command=open_camera)
open_camera_button.grid(row=0, column=0, padx=10, pady=10)

new_user_button = ttk.Button(button_frame, text="Yeni Kullanıcı Ekle", command=new_user)
new_user_button.grid(row=0, column=1, padx=10, pady=10)

# Butonları renklendirme
open_camera_button_style = ttk.Style()
open_camera_button_style.configure("TButton", background='#27ae60', foreground='black', padding=6,
                                   font=('Helvetica', 14))
open_camera_button_style.map("TButton", background=[('active', '#2ecc71')])

new_user_button_style = ttk.Style()
new_user_button_style.configure("TButton", background='#27ae60', foreground='black', padding=6, font=('Helvetica', 14))
new_user_button_style.map("TButton", background=[('active', '#2ecc71')])
# Alt bilgi etiketi
footer_label = ttk.Label(root, text="Lütfen kamerayı açmak veya yeni kullanıcı eklemek için butona basın.",
                         style="TLabel")
footer_label.pack(side=tk.BOTTOM, pady=20)

# Ana döngüyü başlatma
root.mainloop()
