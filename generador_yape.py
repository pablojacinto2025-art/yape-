import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.title("Generador Rápido de Vouchers Yape")
st.write("Modifica solo la fecha, hora y operación al instante:")

# Solo dejamos los campos que necesitas cambiar
fecha = st.text_input("Fecha", value="20 set. 2026")
hora = st.text_input("Hora", value="09:15 p. m.")
operacion = st.text_input("Nro. de Operación", value="5648702")

if st.button("Generar Voucher"):
    # Detectar la imagen base automáticamente
    img_name = "image_3.png"
    if not os.path.exists(img_name):
        if os.path.exists("image_3.png.JPG"):
            img_name = "image_3.png.JPG"
        else:
            st.error("Error: No se encuentra la imagen base en el repositorio. Súbela como 'image_3.png'.")
            st.stop()

    # Abrir la imagen base original fresca
    img = Image.open(img_name).convert("RGBA")
    draw = ImageDraw.Draw(img)

    try:
        font_texto = ImageFont.truetype("arial.ttf", 10)
    except:
        font_texto = ImageFont.load_default()

    # --- LIMPIAR SOLO LAS ZONAS DE FECHA, HORA Y OPERACIÓN ---
    # Esto borra el texto viejo de la plantilla original usando rectángulos blancos exactos
    draw.rectangle([35, 430, 220, 460], fill="white")    # Limpiar zona de fecha y hora
    draw.rectangle([680, 590, 840, 620], fill="white")   # Limpiar zona de número de operación

    # --- DIBUJAR LOS NUEVOS DATOS EN SU POSICIÓN CORRECTA ---
    fecha_hora_str = f"{fecha}  |  {hora}"
    
    # Escribir Fecha y Hora
    draw.text((40, 435), fecha_hora_str, fill="#555555", font=font_texto)
    
    # Escribir Nro de Operación
    draw.text((690, 600), operacion, fill="#2b2b2b", font=font_texto)

    # Guardar resultado actualizado
    output_path = "voucher_salida.png"
    img.convert("RGB").save(output_path)

    # Mostrar resultado limpio en la web
    st.success("¡Voucher generado con éxito!")
    st.image(output_path, caption="Vista previa actualizada de la evidencia", width=280)
    
    with open(output_path, "rb") as file:
        st.download_button(
            label="📥 Descargar Imagen Lista",
            data=file,
            file_name=f"voucher_{operacion}.png",
            mime="image/png"
        )
