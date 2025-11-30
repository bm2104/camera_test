import streamlit as st
from PIL import Image

st.title('📷 카메라 테스트')

# 카메라 입력 위젯
picture = st.camera_input("사진을 찍어주세요")

if picture:
    # PIL 이미지로 변환
    img = Image.open(picture)
    
    # 이미지 표시
    st.image(img, caption='촬영된 사진', use_column_width=True)
    
    # 이미지 정보 표시
    st.write(f"이미지 크기: {img.size}")
    st.write(f"이미지 형식: {img.format}")