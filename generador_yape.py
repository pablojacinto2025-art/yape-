import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.title("Generador Rápido de Vouchers Yape")
st.write("Modifica los datos y genera tu comprobante al instante:")

# Campos de entrada en la página web
monto = st.text_input("Monto (S/)", value="100")
nombre = st.text_input("Nombre del Receptor", value="Juan Quispe")
fecha = st.text_input("Fecha", value="20 set. 2026")
hora = st.text_input("Hora", value="09:15 p. m.")
operacion = st.text_input("Nro. de Operación", value="5648702")

if st.button("Generar Voucher"):
    # Detectar si el archivo existe (probando ambos nombres comunes)
    img_name = "image_3.png"
    if not os.path.exists(img_name):
        if os.path.exists("image_3.png.JPG"):
            img_name = "image_3.png.JPG"
        else:
            st.error("Error: No se encuentra la imagen base en el repositorio. Súbela como 'image_3.png'.")
            st.stop()

    # Abrir la imagen base fresca cada vez
    img = Image.open(img_name).convert("RGBA")
    draw = ImageDraw.Draw(img)

    try:
        font_monto = ImageFont.truetype("arialbd.ttf", 22)
        font_texto = ImageFont.truetype("arial.ttf", 10)
        font_peq = ImageFont.truetype("arial.ttf", 9)
    except:
        font_monto = ImageFont.load_default()
        font_texto = ImageFont.load_default()
        font_peq = ImageFont.load_default()

    # --- BORRADO / LIMPIEZA DE ZONAS (Opcional para evitar capas dobles) ---
    # Dibuja rectángulos blancos limpios sobre los textos viejos de la plantilla base
    draw.rectangle([20, 135, 150, 165], fill="white")  # Limpiar zona monto
    draw.rectangle([20, 180, 180, 200], fill="white")  # Limpiar zona nombre
    draw.rectangle([35, 198, 180, 215], fill="white")  # Limpiar fecha/hora
    draw.rectangle([160, 280, 240, 298], fill="white") # Limpiar operación

    # --- DIBUJAR NUEVOS DATOS ---
    draw.text((25, 140), f"S/ {monto}", fill="#2b2b2b", font=font_monto)
    draw.text((25, 185), nombre, fill="#2b2b2b", font=font_texto)
    
    fecha_hora_str = f"{fecha}  |  {hora}"
    draw.text((38, 202), fecha_hora_str, fill="#555555", font=font_peq)
    
    draw.text((170, 287), operacion, fill="#2b2b2b", font=font_texto)

    # Guardar con un nombre único basado en la operación actual para forzar actualización
    output_path = f"voucher_salida.png"
    img.convert("RGB").save(output_path)

    # Mostrar resultado actualizado en la web
    st.success("¡Voucher generado con éxito!")
    st.image(output_path, caption="Vista previa actualizada de la evidencia", width=280)
    
    with open(output_path, "rb") as file:
        st.download_button(
            label="📥 Descargar Imagen Lista",
            data=file,
            file_name=f"voucher_{operacion}.png",
            mime="image/png"
        )
