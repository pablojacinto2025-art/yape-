import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont
import os

class GeneradorYapeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Comprobantes Yape")
        self.root.geometry("400x480")
        self.root.config(bg="#f4f4f4")

        # Campos por defecto basados en tu captura
        self.monto_var = tk.StringVar(value="20")
        self.nombre_var = tk.StringVar(value="Rivera Rivera")
        self.fecha_var = tk.StringVar(value="17 set. 2026")
        self.hora_var = tk.StringVar(value="06:15 p. m.")
        self.operacion_var = tk.StringVar(value="5648702")

        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.root, text="Editar Comprobante Yape", font=("Arial", 13, "bold"), bg="#f4f4f4", fg="#720072").pack(pady=12)

        frame = tk.Frame(self.root, bg="#f4f4f4")
        frame.pack(pady=5)

        campos = [
            ("Monto (S/):", self.monto_var),
            ("Nombre:", self.nombre_var),
            ("Fecha:", self.fecha_var),
            ("Hora:", self.hora_var),
            ("Nro. Operación:", self.operacion_var)
        ]

        for i, (label_text, var) in enumerate(campos):
            tk.Label(frame, text=label_text, font=("Arial", 10, "bold"), bg="#f4f4f4").grid(row=i, column=0, sticky="w", pady=6, padx=5)
            tk.Entry(frame, textvariable=var, font=("Arial", 11), width=22).grid(row=i, column=1, pady=6, padx=5)

        btn_generar = tk.Button(self.root, text="Generar Imagen", font=("Arial", 11, "bold"), bg="#720072", fg="white", command=self.generar_voucher)
        btn_generar.pack(pady=20)

    def generar_voucher(self):
        if not os.path.exists("image_3.png"):
            messagebox.showerror("Error", "No se encuentra el archivo 'image_3.png' en la carpeta. Guárdalo ahí.")
            return

        try:
            # Abrir la imagen base
            img = Image.open("image_3.png").convert("RGBA")
            draw = ImageDraw.Draw(img)
            
            # Como la imagen base es de resolución estándar, ajustamos una escala proporcional
            # Usamos fuente por defecto o del sistema si está disponible
            try:
                font_monto = ImageFont.truetype("arialbd.ttf", 22)
                font_texto = ImageFont.truetype("arial.ttf", 10)
                font_peq = ImageFont.truetype("arial.ttf", 9)
            except:
                font_monto = ImageFont.load_default()
                font_texto = ImageFont.load_default()
                font_peq = ImageFont.load_default()

            # Coordenadas exactas para la estructura de tu voucher:
            # 1. Monto (S/ 20)
            draw.text((25, 140), f"S/ {self.monto_var.get()}", fill="#2b2b2b", font=font_monto)

            # 2. Nombre del receptor
            draw.text((25, 185), self.nombre_var.get(), fill="#2b2b2b", font=font_texto)

            # 3. Fecha y Hora
            fecha_hora_str = f"{self.fecha_var.get()}  |  {self.hora_var.get()}"
            draw.text((38, 202), fecha_hora_str, fill="#555555", font=font_peq)

            # 4. Número de Operación (alineado a la derecha abajo del bloque)
            draw.text((170, 287), self.operacion_var.get(), fill="#2b2b2b", font=font_texto)

            # Guardar resultado final
            output_name = f"voucher_final_{self.operacion_var.get()}.png"
            img.convert("RGB").save(output_name)

            messagebox.showinfo("¡Listo!", f"¡Comprobante generado con éxito!\nGuardado como: {output_name}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneradorYapeApp(root)
    root.mainloop()