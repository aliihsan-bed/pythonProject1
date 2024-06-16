import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import shutil
import os
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from PIL import Image, ImageTk
from io import BytesIO

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-43c65-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendacerealtime-43c65.appspot.com"
})

def open_camera():
    try:
        subprocess.run(["python", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to open camera:\n{e}")

def open_camera_threaded():
    threading.Thread(target=open_camera).start()

def add_data_to_database(student_info, image_name):
    try:
        ref = db.reference('Students')
        ref.child(image_name).set(student_info)
        messagebox.showinfo("Bilgi", "Veritabanına başarıyla eklendi!")
    except Exception as e:
        messagebox.showerror("Hata", f"Bilgi eklenirken bir hata oluştu:\n{e}")

def update_data_in_database(student_info, image_name):
    try:
        ref = db.reference(f'Students/{image_name}')
        ref.update(student_info)
        messagebox.showinfo("Bilgi", "Veritabanı başarıyla güncellendi!")
    except Exception as e:
        messagebox.showerror("Hata", f"Bilgi güncellenirken bir hata oluştu:\n{e}")

def upload_image_to_firebase(file_path, file_name):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(f'Images/{file_name}')
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        messagebox.showerror("Yükleme Hatası", f"Resim yüklenirken bir hata oluştu: {e}")
        return False

def resize_image(file_path, size=(216, 216)):
    try:
        image = Image.open(file_path)
        image = image.resize(size, Image.ANTIALIAS)
        resized_path = file_path
        image.save(resized_path)
        return resized_path
    except Exception as e:
        messagebox.showerror("Resim Yeniden Boyutlandırma Hatası", f"Resim yeniden boyutlandırılırken bir hata oluştu: {e}")
        return None

def show_data_entry_form(file_path, image_name):
    data_entry_window = tk.Toplevel()
    data_entry_window.title("Öğrenci Bilgi Girişi")
    data_entry_window.geometry("400x400")

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
        student_info = {
            "name": name_entry.get(),
            "major": major_entry.get(),
            "starting_year": int(starting_year_entry.get()),
            "total_attendance": int(total_attendance_entry.get()),
            "standing": standing_entry.get(),
            "year": year_entry.get(),
            "last_attendance_time": last_attendance_time_entry.get()
        }
        resized_image_path = resize_image(file_path)
        if resized_image_path and upload_image_to_firebase(resized_image_path, f'{image_name}.jpg'):  # Assuming .jpg extension for simplicity
            add_data_to_database(student_info, image_name)
        data_entry_window.destroy()

    save_button = ttk.Button(data_entry_window, text="Kaydet", command=add_to_database)
    save_button.pack(pady=10)

def update_data_entry_form(image_name, user_data):
    data_entry_window = tk.Toplevel()
    data_entry_window.title("Öğrenci Bilgi Güncelleme")
    data_entry_window.geometry("400x400")

    ttk.Label(data_entry_window, text="Adı Soyadı:").pack()
    name_entry = ttk.Entry(data_entry_window)
    name_entry.insert(0, user_data['name'])
    name_entry.pack()

    ttk.Label(data_entry_window, text="Bölümü:").pack()
    major_entry = ttk.Entry(data_entry_window)
    major_entry.insert(0, user_data['major'])
    major_entry.pack()

    ttk.Label(data_entry_window, text="Başlama Yılı:").pack()
    starting_year_entry = ttk.Entry(data_entry_window)
    starting_year_entry.insert(0, user_data['starting_year'])
    starting_year_entry.pack()

    ttk.Label(data_entry_window, text="Toplam Katılım:").pack()
    total_attendance_entry = ttk.Entry(data_entry_window)
    total_attendance_entry.insert(0, user_data['total_attendance'])
    total_attendance_entry.pack()

    ttk.Label(data_entry_window, text="Statü:").pack()
    standing_entry = ttk.Entry(data_entry_window)
    standing_entry.insert(0, user_data['standing'])
    standing_entry.pack()

    ttk.Label(data_entry_window, text="Sınıfı:").pack()
    year_entry = ttk.Entry(data_entry_window)
    year_entry.insert(0, user_data['year'])
    year_entry.pack()

    ttk.Label(data_entry_window, text="Son Katılım Zamanı:").pack()
    last_attendance_time_entry = ttk.Entry(data_entry_window)
    last_attendance_time_entry.insert(0, user_data['last_attendance_time'])
    last_attendance_time_entry.pack()

    def update_in_database():
        student_info = {
            "name": name_entry.get(),
            "major": major_entry.get(),
            "starting_year": int(starting_year_entry.get()),
            "total_attendance": int(total_attendance_entry.get()),
            "standing": standing_entry.get(),
            "year": year_entry.get(),
            "last_attendance_time": last_attendance_time_entry.get()
        }
        update_data_in_database(student_info, image_name)
        data_entry_window.destroy()

    save_button = ttk.Button(data_entry_window, text="Güncelle", command=update_in_database)
    save_button.pack(pady=10)

def update_photo(image_name):
    file_path = filedialog.askopenfilename(
        title="Resim Dosyası Seçin",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    if file_path:
        try:
            file_name = os.path.basename(file_path)
            destination_dir = r"C:\Users\alii2\PycharmProjects\pythonProject1\Images"
            os.makedirs(destination_dir, exist_ok=True)
            destination_path = os.path.join(destination_dir, file_name)
            shutil.copy(file_path, destination_path)
            messagebox.showinfo("Dosya Yüklendi", f"Dosya başarıyla yüklendi: {destination_path}")
            resized_image_path = resize_image(destination_path)
            if resized_image_path and upload_image_to_firebase(resized_image_path, f'{image_name}.jpg'):
                messagebox.showinfo("Bilgi", "Fotoğraf başarıyla güncellendi!")
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", f"Dosya yüklenirken bir hata oluştu: {e}")
    else:
        messagebox.showwarning("Dosya Seçilmedi", "Herhangi bir dosya seçilmedi.")

def new_user():
    file_path = filedialog.askopenfilename(
        title="Resim Dosyası Seçin",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    if file_path:
        try:
            file_name = os.path.basename(file_path)
            destination_dir = r"C:\Users\alii2\PycharmProjects\pythonProject1\Images"
            os.makedirs(destination_dir, exist_ok=True)
            destination_path = os.path.join(destination_dir, file_name)
            shutil.copy(file_path, destination_path)
            messagebox.showinfo("Dosya Yüklendi", f"Dosya başarıyla yüklendi: {destination_path}")
            image_name = os.path.splitext(file_name)[0]
            show_data_entry_form(destination_path, image_name)
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", f"Dosya yüklenirken bir hata oluştu: {e}")
    else:
        messagebox.showwarning("Dosya Seçilmedi", "Herhangi bir dosya seçilmedi.")

def show_user_data():
    user_id_window = tk.Toplevel()
    user_id_window.title("Kullanıcıyı Görüntüle")
    user_id_window.geometry("300x200")

    ttk.Label(user_id_window, text="Kullanıcı ID:").pack(pady=5)
    user_id_entry = ttk.Entry(user_id_window)
    user_id_entry.pack(pady=5)

    def fetch_and_display_user_data():
        user_id = user_id_entry.get()
        ref = db.reference(f'Students/{user_id}')
        try:
            user_data = ref.get()
            if user_data:
                user_data_window = tk.Toplevel()
                user_data_window.title("Kullanıcı Bilgileri")
                user_data_window.geometry("400x600")

                ttk.Label(user_data_window, text=f"Adı Soyadı: {user_data['name']}").pack(pady=5)
                ttk.Label(user_data_window, text=f"Bölümü: {user_data['major']}").pack(pady=5)
                ttk.Label(user_data_window, text=f"Başlama Yılı: {user_data['starting_year']}").pack(pady=5)
                ttk.Label(user_data_window, text=f"Toplam Katılım: {user_data['total_attendance']}").pack(pady=5)
                ttk.Label(user_data_window, text=f"Statü: {user_data['standing']}").pack(pady=5)
                ttk.Label(user_data_window, text=f"Sınıfı: {user_data['year']}").pack(pady=5)
                ttk.Label(user_data_window, text=f"Son Katılım Zamanı: {user_data['last_attendance_time']}").pack(pady=5)

                try:
                    bucket = storage.bucket()
                    blob = bucket.blob(f'Images/{user_id}.jpg')
                    image_data = blob.download_as_bytes()
                    img = Image.open(BytesIO(image_data))
                    img = img.resize((216, 216), Image.ANTIALIAS)
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = tk.Label(user_data_window, image=img_tk)
                    img_label.image = img_tk
                    img_label.pack(pady=10)
                except Exception as e:
                    messagebox.showerror("Hata", f"Resim yüklenirken bir hata oluştu: {e}")

                update_info_button = ttk.Button(user_data_window, text="Bilgileri Güncelle", command=lambda: update_data_entry_form(user_id, user_data))
                update_info_button.pack(pady=10)

                update_photo_button = ttk.Button(user_data_window, text="Fotoğrafı Güncelle", command=lambda: update_photo(user_id))
                update_photo_button.pack(pady=10)
            else:
                messagebox.showerror("Hata", "Kullanıcı bulunamadı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Kullanıcı bilgileri alınırken bir hata oluştu: {e}")

    fetch_button = ttk.Button(user_id_window, text="Göster", command=fetch_and_display_user_data)
    fetch_button.pack(pady=10)

# Tkinter arayüzü oluşturma
root = tk.Tk()
root.title("Kamera Arayüzü")
root.geometry("700x600")
root.resizable(False, False)
root.configure(bg='#2ecc71')

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14), padding=10)
style.configure("TLabel", font=("Helvetica", 16), background='#2ecc71', foreground='white')

title_label = ttk.Label(root, text="Kamera Kontrol Arayüzü", style="TLabel")
title_label.pack(pady=20)

button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

open_camera_button = ttk.Button(button_frame, text="Kamerayı Aç", command=open_camera_threaded)
open_camera_button.grid(row=0, column=0, padx=10, pady=10)

new_user_button = ttk.Button(button_frame, text="Yeni Kullanıcı Ekle", command=new_user)
new_user_button.grid(row=0, column=1, padx=10, pady=10)

view_user_button = ttk.Button(button_frame, text="Kullanıcıyı Görüntüle", command=show_user_data)
view_user_button.grid(row=0, column=2, padx=10, pady=10)

open_camera_button_style = ttk.Style()
open_camera_button_style.configure("TButton", background='#27ae60', foreground='black', padding=6, font=('Helvetica', 14))
open_camera_button_style.map("TButton", background=[('active', '#2ecc71')])

new_user_button_style = ttk.Style()
new_user_button_style.configure("TButton", background='#27ae60', foreground='black', padding=6, font=('Helvetica', 14))
new_user_button_style.map("TButton", background=[('active', '#2ecc71')])

view_user_button_style = ttk.Style()
view_user_button_style.configure("TButton", background='#27ae60', foreground='black', padding=6, font=('Helvetica', 14))
view_user_button_style.map("TButton", background=[('active', '#2ecc71')])

footer_label = ttk.Label(root, text="Lütfen kamerayı açmak, yeni kullanıcı eklemek veya kullanıcı görüntülemek için butona basın.",
                         style="TLabel")
footer_label.pack(side=tk.BOTTOM, pady=20)

root.mainloop()
