import tkinter as tk
from tkinter import messagebox
import json
import os

DOSYA_ADI = "notlar.json"

def yukle():
    if os.path.exists(DOSYA_ADI):
        with open(DOSYA_ADI, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def kaydet(notlar):
    with open(DOSYA_ADI, "w", encoding="utf-8") as f:
        json.dump(notlar, f, indent=4, ensure_ascii=False)

def listeyi_guncelle(filtre=""):
    liste.delete(0, tk.END)
    for not_item in notlar:
        if filtre.lower() in not_item["text"].lower() or filtre.lower() in not_item["kategori"].lower():
            liste.insert(tk.END, f"[{not_item['kategori']}] {not_item['text']}")

def not_ekle():
    yeni_not = giris.get()
    kategori = kategori_giris.get()
    if yeni_not.strip() == "" or kategori.strip() == "":
        messagebox.showwarning("Uyarı", "Not ve kategori boş olamaz!")
        return
    notlar.append({"text": yeni_not, "kategori": kategori})
    kaydet(notlar)
    listeyi_guncelle()
    giris.delete(0, tk.END)
    kategori_giris.delete(0, tk.END)

def not_sil():
    secim = liste.curselection()
    if not secim:
        messagebox.showwarning("Uyarı", "Silmek için bir not seçin!")
        return
    index = secim[0]
    silinen = notlar.pop(index)
    kaydet(notlar)
    listeyi_guncelle()
    messagebox.showinfo("Silindi", f"'{silinen['text']}' silindi.")

def not_duzenle():
    secim = liste.curselection()
    if not secim:
        messagebox.showwarning("Uyarı", "Düzenlemek için bir not seçin!")
        return
    index = secim[0]
    secili_not = notlar[index]

    duzen_pencere = tk.Toplevel(pencere)
    duzen_pencere.title("Not Düzenle")
    duzen_pencere.geometry("300x200")

    tk.Label(duzen_pencere, text="Yeni Not:").pack(pady=5)
    yeni_not_entry = tk.Entry(duzen_pencere, width=30)
    yeni_not_entry.insert(0, secili_not["text"])
    yeni_not_entry.pack(pady=5)

    tk.Label(duzen_pencere, text="Kategori:").pack(pady=5)
    yeni_kategori_entry = tk.Entry(duzen_pencere, width=30)
    yeni_kategori_entry.insert(0, secili_not["kategori"])
    yeni_kategori_entry.pack(pady=5)

    def kaydet_duzenleme():
        notlar[index]["text"] = yeni_not_entry.get()
        notlar[index]["kategori"] = yeni_kategori_entry.get()
        kaydet(notlar)
        listeyi_guncelle()
        duzen_pencere.destroy()
        messagebox.showinfo("Başarılı", "Not düzenlendi!")

    tk.Button(duzen_pencere, text="Kaydet", command=kaydet_duzenleme, bg="lightblue").pack(pady=10)

def not_ara(*args):
    filtre = arama_giris.get()
    listeyi_guncelle(filtre)

# Ana pencere
pencere = tk.Tk()
pencere.title("📝 Gelişmiş Not Defteri")
pencere.geometry("500x550")

notlar = yukle()

# Arama kutusu
tk.Label(pencere, text="🔍 Ara:").pack(pady=2)
arama_giris = tk.Entry(pencere, width=40)
arama_giris.pack(pady=5)
arama_giris.bind("<KeyRelease>", not_ara)

# Not giriş alanı
tk.Label(pencere, text="📝 Yeni Not:").pack(pady=2)
giris = tk.Entry(pencere, width=40)
giris.pack(pady=5)

# Kategori giriş alanı
tk.Label(pencere, text="🏷️ Kategori:").pack(pady=2)
kategori_giris = tk.Entry(pencere, width=40)
kategori_giris.pack(pady=5)
kategori_giris.insert(0, "Genel")

# Butonlar
ekle_btn = tk.Button(pencere, text="Not Ekle", command=not_ekle, bg="lightgreen")
ekle_btn.pack(pady=5)

sil_btn = tk.Button(pencere, text="Seçili Notu Sil", command=not_sil, bg="lightcoral")
sil_btn.pack(pady=5)

duzenle_btn = tk.Button(pencere, text="Seçili Notu Düzenle", command=not_duzenle, bg="lightblue")
duzenle_btn.pack(pady=5)

# Not listesi
tk.Label(pencere, text="📋 Kaydedilmiş Notlar:").pack(pady=5)
liste = tk.Listbox(pencere, width=60, height=15)
liste.pack(pady=10)

listeyi_guncelle()

pencere.mainloop()
