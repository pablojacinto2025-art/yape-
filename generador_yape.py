import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.title("Generador Rápido de Vouchers Yape")
st.write("Modifica la fecha, hora y operación al instante:")

fecha = st.text_input("Fecha", value="22 set. 2026")
hora = st.text_input("Hora", value="01:15 p. m.")
operacion = st.text_input("Nro. de Operación", value="5648702")

if st.button("Generar Voucher"):
    img_name = "image_3.png"
    if not os.path.exists(img_name):
        if os.path.exists("image_3.png.JPG"):
            img_name = "image_3.png.JPG"
        else:
            st.error("Error: No se encuentra la imagen base en el repositorio. Súbela como 'image_3.png'.")
            st.stop()

    img = Image.open(img_name).convert("RGBA")
    draw = ImageDraw.Draw(img)

    try:
        font_texto = ImageFont.truetype("arial.ttf", 10)
    except:
        font_texto = ImageFont.load_default()

    # Coordenadas exactas en base a la resolución de tu imagen base:
    # 1. Limpiar la zona exacta donde está la fecha y hora original en la tarjeta
    draw.rectangle([70, 200, 190, 218], fill="white")
    
    # 2. Limpiar la zona exacta donde está el número de operación original
    draw.rectangle([160, 285, 230, 298], fill="white")

    # Escribir los nuevos datos exactamente en el lugar limpio
    fecha_hora_str = f"{fecha}  |  {hora}"
    draw.text((72, 203), fecha_hora_str, fill="#555555", font=font_texto)
    draw.text((165, 287), operacion, fill="#2b2b2b", font=font_texto)

    output_path = "voucher_salida.png"
    img.convert("RGB").save(output_path)

    st.success("¡Voucher generado con éxito!")
    st.image(output_path, caption="Vista previa actualizada de la evidencia", width=280)
    
    with open(output_path, "rb") as file:
        st.download_button(
            label="📥 Descargar Imagen Lista",
            data=file,
            file_name=f"voucher_{operacion}.png",
            mime="image/png"
        )
