import streamlit as st
import fitz  # PyMuPDF
import io
from zipfile import ZipFile
import sys

# PDF 페이지를 JPG 이미지로 변환하는 함수
def pdf_to_jpg(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images = []
    for i in range(len(doc)):
        page = doc.load_page(i)
        pix = page.get_pixmap()
        img_buffer = io.BytesIO(pix.tobytes("jpeg"))
        img_buffer.seek(0)
        images.append((img_buffer, f"page_{i+1}.jpg"))
    return images

st.title("PDF to JPG Converter")

# PDF 파일 업로드
pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

if pdf_file:
    st.write("Converting PDF to JPG...")
    images = pdf_to_jpg(pdf_file)
    
    # 각 페이지를 JPG로 변환하고 개별 다운로드 버튼 추가
    for img_buffer, filename in images:
        st.image(img_buffer, caption=filename)
        st.download_button(
            label=f"Download {filename}",
            data=img_buffer,
            file_name=filename,
            mime="image/jpeg"
        )

    # 모든 JPG 파일을 ZIP으로 다운로드할 수 있는 버튼 추가
    if images:
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            for img_buffer, filename in images:
                zip_file.writestr(filename, img_buffer.getvalue())
        zip_buffer.seek(0)
        
        st.download_button(
            label="Download All as ZIP",
            data=zip_buffer,
            file_name="images.zip",
            mime="application/zip"
        )

    st.success("Conversion complete!")

# 종료 버튼 추가
if st.button("Exit Application"):
    st.write("Exiting the application...")
    sys.exit(0)
