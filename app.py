import streamlit as st
from PIL import Image
from io import BytesIO

from processing import (
    mean_filter,
    gaussian_filter,
    histogram,
    linear_contrast,
    equalize_gray
)


st.set_page_config(
    page_title="Обработка изображений",
    layout="wide"
)

st.title("Обработка изображений")

uploaded_file = st.file_uploader(
    "Загрузите изображение",
    type=["png", "jpg", "jpeg", "bmp"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    method = st.sidebar.selectbox(
        "Метод обработки",
        [
            "Усредняющий фильтр",
            "Фильтр Гаусса",
            "Линейное контрастирование",
            "Эквализация серого изображения"
        ]
    )

    if method in ["Усредняющий фильтр", "Фильтр Гаусса"]:
        source = image

        size = st.sidebar.select_slider(
            "Размер фильтра",
            options=[3, 5, 7, 9, 11],
            value=3
        )

        if method == "Усредняющий фильтр":
            result = mean_filter(image, size)
        else:
            sigma = st.sidebar.slider(
                "Сигма",
                min_value=0.5,
                max_value=5.0,
                value=1.0,
                step=0.1
            )

            result = gaussian_filter(image, size, sigma)

    else:
        source = image.convert("L")

        if method == "Линейное контрастирование":
            result = linear_contrast(source)
        else:
            result = equalize_gray(source)

        st.caption(
            "Для этих двух методов сравниваем изображения "
            "в оттенках серого."
        )

    left, right = st.columns(2)

    with left:
        st.subheader("Исходное изображение")
        st.image(source, use_container_width=True)

        st.write("Гистограмма до обработки")
        st.bar_chart(histogram(source))

    with right:
        st.subheader("Результат")
        st.image(result, use_container_width=True)

        st.write("Гистограмма после обработки")
        st.bar_chart(histogram(result))

    st.caption(
        "На гистограммах: по горизонтали — яркость от 0 до 255, "
        "по вертикали — количество пикселей. "
        "Для цветных изображений показана гистограмма "
        "после перевода в оттенки серого."
    )

    buffer = BytesIO()
    result.save(buffer, format="PNG")

    st.download_button(
        "Скачать результат",
        data=buffer.getvalue(),
        file_name="result.png",
        mime="image/png"
    )

else:
    st.info("Загрузите изображение, чтобы начать обработку.")