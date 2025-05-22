import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'Tesseract-OCR\tessdata'

class OCRApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Texto da Imagem")
        self.geometry("850x500")
        self.resizable(False,False)
        self.attributes('-alpha', 0.92)

        # Label para exibir a imagem
        self.image_label = ctk.CTkLabel(self, text="Nenhuma imagem carregada", width=400, height=400)
        self.image_label.grid(row=0, column=0, padx=10, pady=10)

        # Botão para selecionar imagem
        self.select_button = ctk.CTkButton(self, text="Selecionar Imagem", command=self.select_image, fg_color="black", hover_color="#121212")
        self.select_button.grid(row=1, column=0, pady=(0, 10))

        # Botão para extrair texto
        self.extract_button = ctk.CTkButton(self, text="Extrair Texto", command=self.extract_text, state="disabled",fg_color="#202020", hover_color="#121212", text_color_disabled="#404040")
        self.extract_button.grid(row=2, column=0, pady=(0, 10))

        # Caixa de texto para mostrar o texto extraído
        self.text_box = ctk.CTkTextbox(self, width=400, height=400, fg_color="#202020")
        self.text_box.grid(row=0, column=1, rowspan=3, padx=10, pady=10)

        # Variável da imagem
        self.loaded_image = None

    def select_image(self):
        filepath = filedialog.askopenfilename(
            title="Selecione uma Imagem",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp"), ("Todos arquivos", "*.*")]
        )
        if not filepath:
            return

        try:
            self.loaded_image = Image.open(filepath)
            img_resized = self.loaded_image.copy()
            img_resized.thumbnail((400, 400))

            self.imgtk = ImageTk.PhotoImage(img_resized)
            self.image_label.configure(image=self.imgtk, text="")

            self.extract_button.configure(state="normal")

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a imagem.\n{e}")
            self.loaded_image = None
            self.extract_button.configure(state="disabled")

    def extract_text(self):
        if self.loaded_image is None:
            messagebox.showwarning("Aviso", "Por favor, selecione uma imagem primeiro.")
            return

        try:
            img = self.loaded_image.convert("RGB") if self.loaded_image.mode != "RGB" else self.loaded_image
            extracted_text = pytesseract.image_to_string(img, lang='por')

            self.text_box.delete("1.0", "end")
            self.text_box.insert("1.0", extracted_text)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao extrair texto.\n{e}")

if __name__ == "__main__":
    app = OCRApp()
    app.mainloop()
