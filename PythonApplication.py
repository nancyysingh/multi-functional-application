import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
from cryptography.fernet import Fernet
import pyttsx3
import requests
import wikipedia
from bs4 import BeautifulSoup
import webbrowser
import speech_recognition as sr
import pyaudio
import qrcode
import os
import img2pdf
from pdf2docx import Converter
from tkinter import filedialog
from PIL import Image, ImageTk
import psutil
import math
from tkinter import Tk, Label, StringVar, OptionMenu

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Functional Application")
        self.root.geometry("600x400")
        self.root.configure(bg="#ADD8E6")  # Light blue

     
        self.bg_index = 0 #index for app shining

        # Display a greeting message or animation
        self.greeting_label = tk.Label(self.root, text="Multi-Function Application using Python", font=("Times New Roman", 25, "bold"), fg="white", bg="#DC143C")
        self.greeting_label.pack(pady=10)

        
        functionalities_text = "     Functionalities:\n\n1. Google Translate\n2. Text Encrypt/Decrypt\n3. Text to Speech\n4. Wikipedia Search\n5. Dictionary\n6. YouTube Song Play\n7. QR Code Generator\n8. File Converter\n9. System Information"
        self.functionalities_label = tk.Label(self.root, text=functionalities_text, font=("Times New Roman", 17 , "bold"), fg="black", bg = "white" ,justify=tk.LEFT)
        self.functionalities_label.pack(pady=5)

        self.main_frame = tk.Frame(root, bg="#00FFFF")
        self.main_frame.pack(fill="both", expand=True, padx=450, pady=5)


        self.option_var = tk.StringVar()
        self.option_var.set("Select an Option")

        options = ["Language Translator", "Data Encrypt/Decrypt", "Text to Voice", "Voice to Text", "Wikipedia Search", "Dictionary", "YouTube Song Play", "QR Code Generator", "File Converter", "System Information"]


        self.option_menu = ttk.Combobox(self.main_frame, textvariable=self.option_var, values=options, state="readonly", font=("Helvetica", 16))  # Increased font size to 16
        self.option_menu.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.select_button = tk.Button(self.main_frame, text="Select", command=self.select_option, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=15, pady=10)  # Increased padding
        self.select_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER, y=0.5)


        self.colors = {
            "Language Translator": "#00FFFF",
            "Data Encrypt/Decrypt": "#00FFFF",
            "Text to Voice": "#00FFFF",
            "Weather Forecast": "#00FFFF",
            "Wikipedia Search": "#00FFFF",
            "Dictionary": "#00FFFF",
            "Voice to Text": "#00FFFF",
            "YouTube Song Play": "#00FFFF",
            "QR Code Generator": "#00FFFF",
            "File Converter": "#00FFFF",  # Hot pink
            "System Information": "#00FFFF",  # Deep pink
            "default": None   ,        # Light blue
}


    
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            if widget not in [self.option_menu, self.select_button]:
                widget.destroy()

    def select_option(self):
        self.clear_frame()
        option = self.option_var.get()
        new_bg_color = self.colors.get(option, self.colors["default"])
        self.main_frame.configure(bg=new_bg_color)

        if option == "Language Translator":
            self.language_translator()
        elif option == "Data Encrypt/Decrypt":
            self.data_encrypt_decrypt()
        elif option == "Text to Voice":
            self.text_to_voice()
        elif option == "Wikipedia Search":
            self.wikipedia_search()
        elif option == "Dictionary":
            self.dictionary_lookup()
        elif option == "Voice to Text":
            self.voice_to_text()
        elif option == "YouTube Song Play":
            self.youtube_song_play()
        elif option == "QR Code Generator":
            self.qr_code_generator()
        elif option == "File Converter":
            self.file_converter()
        elif option == "System Information":
            self.system_information()


    def dictionary_lookup(self):
        self.dictionary_var = tk.StringVar()
        self.dictionary_entry = tk.Entry(self.main_frame, textvariable=self.dictionary_var, font=("Helvetica", 12), width=30)
        self.dictionary_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.dictionary_button = tk.Button(self.main_frame, text="Lookup", command=self.lookup_dictionary, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.dictionary_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.dictionary_output = tk.Text(self.main_frame, height=7, width=40, font=("Helvetica", 12))
        self.dictionary_output.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def lookup_dictionary(self):
        word = self.dictionary_var.get().strip().lower()
        url = f"https://www.dictionary.com/browse/{word}"

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            meanings = soup.find_all('meta', attrs={'name': 'description'})

            if not meanings:
                self.dictionary_output.delete("1.0", "end")
                self.dictionary_output.insert("1.0", "No definition found.")
                return

            definition = meanings[0]['content'].split(':')[-1].strip()

            self.dictionary_output.delete("1.0", "end")
            self.dictionary_output.insert("1.0", f"{word.capitalize()}:\n{definition}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def language_translator(self):
        self.translator = Translator()

        self.input_text = tk.Text(self.main_frame, height=3, width=40, font=("Helvetica", 12))
        self.input_text.place(relx=0.5, rely=0.4, anchor=tk.CENTER,y=40)

        self.lang_var = tk.StringVar()
        self.lang_menu = ttk.Combobox(self.main_frame, textvariable=self.lang_var, values=list(LANGUAGES.values()), state="readonly", font=("Helvetica", 12))
        self.lang_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER,y=60)

        self.translate_button = tk.Button(self.main_frame, text="Translate", command=self.translate_text, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.translate_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER ,y=70)

        self.output_text = tk.Text(self.main_frame, height=3, width=40, font=("Helvetica", 12))
        self.output_text.place(relx=0.5, rely=0.7, anchor=tk.CENTER, y=80)

    def translate_text(self):
        input_text = self.input_text.get("1.0", "end-1c")
        lang = self.lang_var.get()
        lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(lang)]

        try:
            translation = self.translator.translate(input_text, dest=lang_code)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", translation.text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def data_encrypt_decrypt(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

        self.input_text = tk.Text(self.main_frame, height=3, width=40, font=("Helvetica", 12))
        self.input_text.place(relx=0.5, rely=0.4, anchor=tk.CENTER, y=20)

        self.encrypt_button = tk.Button(self.main_frame, text="Encrypt", command=self.encrypt_text, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.encrypt_button.place(relx=0.4, rely=0.5, anchor=tk.CENTER,y=50)

        self.decrypt_button = tk.Button(self.main_frame, text="Decrypt", command=self.decrypt_text, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.decrypt_button.place(relx=0.6, rely=0.5, anchor=tk.CENTER, y=50)

        self.output_text = tk.Text(self.main_frame, height=3, width=40, font=("Helvetica", 12))
        self.output_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER , y=80)

    def encrypt_text(self):
        input_text = self.input_text.get("1.0", "end-1c")
        encrypted_text = self.cipher_suite.encrypt(input_text.encode())
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", encrypted_text.decode())

    def decrypt_text(self):
        input_text = self.input_text.get("1.0", "end-1c")
        try:
            decrypted_text = self.cipher_suite.decrypt(input_text.encode())
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", decrypted_text.decode())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def text_to_voice(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 130)
        self.input_text = tk.Text(self.main_frame, height=3, width=40, font=("Helvetica", 12))
        self.input_text.place(relx=0.5, rely=0.4, anchor=tk.CENTER, y=20)

        self.tts_button = tk.Button(self.main_frame, text="Text to Speech", command=self.text_to_speech, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.tts_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=50)

    def text_to_speech(self):
        input_text = self.input_text.get("1.0", "end-1c")
        self.engine.say(input_text)
        self.engine.runAndWait()



    def wikipedia_search(self):
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.main_frame, textvariable=self.search_var, font=("Helvetica", 12), width=30)
        self.search_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.search_button = tk.Button(self.main_frame, text="Search", command=self.search_wikipedia, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.search_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.search_output = tk.Text(self.main_frame, height=7, width=40, font=("Helvetica", 12))
        self.search_output.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    

    def voice_to_text(self):
       self.voice_output = tk.Text(self.main_frame, height=7, width=40, font=("Helvetica", 12))
       self.voice_output.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

       self.record_button = tk.Button(self.main_frame, text="Record", command=self.record_voice, font=("Helvetica", 12), bg="#4CAF50", fg="white")
       self.record_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)  # Adjusted position to be beside the output text field


    def record_voice(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
          try:
              self.voice_output.delete("1.0", "end")
              self.voice_output.insert("1.0", "Listening...")
              self.root.update_idletasks()
              audio = recognizer.listen(source)
              text = recognizer.recognize_google(audio)
              self.voice_output.delete("1.0", "end")
              self.voice_output.insert("1.0", text)
          except Exception as e:
              self.voice_output.delete("1.0", "end")
              self.voice_output.insert("1.0", str(e))

    def search_wikipedia(self):
        query = self.search_var.get()
        try:
            summary = wikipedia.summary(query, sentences=3)
            self.search_output.delete("1.0", "end")
            self.search_output.insert("1.0", summary)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def youtube_song_play(self):
        self.song_var = tk.StringVar()
        self.song_entry = tk.Entry(self.main_frame, textvariable=self.song_var, font=("Helvetica", 12), width=30)
        self.song_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.search_button = tk.Button(self.main_frame, text="Search", command=self.search_youtube, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.search_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def search_youtube(self):
        song_name = self.song_var.get().strip()
        if song_name:
            query = song_name.replace(" ", "+")
            url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(url)


    
    def qr_code_generator(self):
      self.qr_input_var = tk.StringVar()
      self.qr_input_entry = tk.Entry(self.main_frame, textvariable=self.qr_input_var, font=("Helvetica", 12), width=30)
      self.qr_input_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    # Position the Generate QR Code button
      self.generate_button = tk.Button(self.main_frame, text="Generate QR Code", command=self.generate_qr_code, font=("Helvetica", 12), bg="#4CAF50", fg="white")
      self.generate_button.place(relx=0.87, rely=0.4, anchor=tk.CENTER)

      self.qr_canvas = tk.Canvas(self.main_frame, width=200, height=200)
      self.qr_canvas.place(relx=0.5, rely=0.7, anchor=tk.CENTER)


    def generate_qr_code(self):
        data = self.qr_input_var.get().strip()
        if data:
            # Generate QR code using qrcode module
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Create a PIL Image object from the QR code
            img = qr.make_image(fill='black', back_color='white')
            img = img.resize((200, 200), resample=Image.LANCZOS)  # Resize for better display

            # Convert PIL Image to Tkinter PhotoImage
            self.qr_image = ImageTk.PhotoImage(img)

            # Clear previous content on canvas
            self.qr_canvas.delete("all")

            # Display the QR code on canvas
            self.qr_canvas.create_image(0, 0, anchor=tk.NW, image=self.qr_image)
        else:
            messagebox.showerror("Error", "Please enter data for QR code.")

    def file_converter(self):
       self.file_label = tk.Label(self.main_frame, text="Select a file to convert:", font=("Helvetica", 12), bg=self.colors["File Converter"])
       self.file_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER, y=70)

       self.file_button = tk.Button(self.main_frame, text="Browse", command=self.browse_file, font=("Helvetica", 12), bg="#4CAF50", fg="white")
       self.file_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER, y=80)

       self.convert_pdf_to_word_button = tk.Button(self.main_frame, text="Convert PDF to Word", command=self.convert_pdf_to_word, font=("Helvetica", 12), bg="#4CAF50", fg="white")
       self.convert_pdf_to_word_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER, y=85)

       self.convert_image_to_pdf_button = tk.Button(self.main_frame, text="Convert Image to PDF", command=self.convert_image_to_pdf, font=("Helvetica", 12), bg="#4CAF50", fg="white")
       self.convert_image_to_pdf_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=100)

    def browse_file(self):
       self.filepath = filedialog.askopenfilename()
       if self.filepath:
         self.file_label.config(text=f"Selected file: {self.filepath}")

    def convert_pdf_to_word(self):
       if not hasattr(self, 'filepath') or not self.filepath:
          messagebox.showerror("Error", "No file selected.")
          return

       if not self.filepath.lower().endswith('.pdf'):
          messagebox.showerror("Error", "Selected file is not a PDF.")
          return

       try:
           output_docx_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("DOCX files", "*.docx")])
           if not output_docx_path:
             return

           converter = Converter(self.filepath)
           converter.convert(output_docx_path, start=0, end=None)
           converter.close()
           messagebox.showinfo("Success", "PDF converted to DOCX successfully.")
       except Exception as e:
          messagebox.showerror("Error", str(e))

    def convert_image_to_pdf(self):
       if not hasattr(self, 'filepath') or not self.filepath:
          messagebox.showerror("Error", "No file selected.")
          return

       if not self.filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
          messagebox.showerror("Error", "Selected file is not an image.")
          return

       try:
          output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
          if not output_pdf_path:
            return

          image = Image.open(self.filepath)
          pdf_bytes = img2pdf.convert(image.filename)
          with open(output_pdf_path, 'wb') as f:
             f.write(pdf_bytes)
          messagebox.showinfo("Success", "Image converted to PDF successfully.")
       except Exception as e:
          messagebox.showerror("Error", str(e))

    def system_information(self):
        self.clear_frame()

        # CPU Information
        cpu_label = tk.Label(self.main_frame, text="CPU Usage:", font=("Helvetica", 12))
        cpu_label.place(relx=0.3, rely=0.2, anchor=tk.CENTER, y= 60)

        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_text = f"{cpu_percent}%"
        cpu_value_label = tk.Label(self.main_frame, text=cpu_text, font=("Helvetica", 12, "bold"))
        cpu_value_label.place(relx=0.7, rely=0.2, anchor=tk.CENTER, y=60)

        # Memory Information
        mem_label = tk.Label(self.main_frame, text="Memory Usage:", font=("Helvetica", 12))
        mem_label.place(relx=0.3, rely=0.3, anchor=tk.CENTER, y=80)

        mem = psutil.virtual_memory()
        mem_text = f"Used: {self.get_size(mem.used)} | Total: {self.get_size(mem.total)}"
        mem_value_label = tk.Label(self.main_frame, text=mem_text, font=("Helvetica", 12, "bold"))
        mem_value_label.place(relx=0.7, rely=0.3, anchor=tk.CENTER, y=80)

        # Disk Information
        disk_label = tk.Label(self.main_frame, text="Disk Usage:", font=("Helvetica", 12))
        disk_label.place(relx=0.3, rely=0.4, anchor=tk.CENTER, y=100)

        disk = psutil.disk_usage('/')
        disk_text = f"Used: {self.get_size(disk.used)} | Total: {self.get_size(disk.total)}"
        disk_value_label = tk.Label(self.main_frame, text=disk_text, font=("Helvetica", 12, "bold"))
        disk_value_label.place(relx=0.7, rely=0.4, anchor=tk.CENTER, y=100)

        # Add a button to refresh the information
        refresh_button = tk.Button(self.main_frame, text="Refresh", command=self.system_information, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        refresh_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=120)

    def get_size(self, bytes, suffix="B"):
        # Helper function to convert bytes to human-readable format
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f} {unit}{suffix}"
            bytes /= factor
        return f"{bytes:.2f} {unit}{suffix}"




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
