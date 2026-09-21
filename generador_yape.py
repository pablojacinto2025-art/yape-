import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.title("Generador Rápido de Vouchers Yape")
st.write("Modifica la fecha, la hora y el número de operación:")

fecha = st.text_input("Fecha", value="17 set. 2026")
hora = st.text_input("Hora", value="06:15 p. m.")
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
    w, h = img.size
    draw = ImageDraw.Draw(img)

    try:
        font_texto = ImageFont.truetype("arial.ttf", int(h * 0.022))
    except:
        font_texto = ImageFont.load_default()

    # Limpiar con blanco la zona exacta de la fecha y hora original dentro de la tarjeta
    draw.rectangle([int(w * 0.25), int(h * 0.65), int(w * 0.85), int(h * 0.70)], fill="white")
    
    # Limpiar la zona exacta del número de operación en la parte inferior
    draw.rectangle([int(w * 0.60), int(h * 0.80), int(w * 0.95), int(h * 0.85)], fill="white")

    # Escribir los nuevos datos en su posición exacta
    fecha_hora_str = f"{fecha}  |  {hora}"
    draw.text((int(w * 0.26), int(h * 0.655)), fecha_hora_str, fill="#555555", font=font_texto)
    draw.text((int(w * 0.65), int(h * 0.805)), operacion, fill="#2b2b2b", font=font_texto)

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
