import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.title("Generador Rápido de Vouchers Yape")
st.write("Modifica los datos y genera tu comprobante al instante:")

# Campos de entrada en la página web
monto = st.text_input("Monto (S/)", value="20")
nombre = st.text_input("Nombre del Receptor", value="Rivera Rivera")
fecha = st.text_input("Fecha", value="17 set. 2026")
hora = st.text_input("Hora", value="06:15 p. m.")
operacion = st.text_input("Nro. de Operación", value="5648702")

if st.button("Generar Voucher"):
    # Comprobar si la imagen base está subida al repositorio
    if not os.path.exists("image_3.png"):
        st.error("Error: No se encuentra el archivo 'image_3.png' en tu repositorio de GitHub. Súbelo a la misma carpeta.")
    else:
        # Abrir imagen base
        img = Image.open("image_3.png").convert("RGBA")
        draw = ImageDraw.Draw(img)

        try:
            font_monto = ImageFont.truetype("arialbd.ttf", 22)
            font_texto = ImageFont.truetype("arial.ttf", 10)
            font_peq = ImageFont.truetype("arial.ttf", 9)
        except:
            font_monto = ImageFont.load_default()
            font_texto = ImageFont.load_default()
            font_peq = ImageFont.load_default()

        # Dibujar datos exactamente en las coordenadas de tu voucher
        draw.text((25, 140), f"S/ {monto}", fill="#2b2b2b", font=font_monto)
        draw.text((25, 185), nombre, fill="#2b2b2b", font=font_texto)
        
        fecha_hora_str = f"{fecha}  |  {hora}"
        draw.text((38, 202), fecha_hora_str, fill="#555555", font=font_peq)
        
        draw.text((170, 287), operacion, fill="#2b2b2b", font=font_texto)

        # Guardar resultado temporal
        output_path = f"voucher_{operacion}.png"
        img.convert("RGB").save(output_path)

        # Mostrar resultado y botón de descarga en la web
        st.success("¡Voucher generado con éxito!")
        st.image(output_path, caption="Vista previa de la evidencia", width=280)
        
        with open(output_path, "rb") as file:
            st.download_button(
                label="📥 Descargar Imagen Lista",
                data=file,
                file_name=output_path,
                mime="image/png"
            )
