import streamlit as st
from pyzbar import pyzbar
from PIL import Image

st.title('바코드 스캐너')

# Session_state 초기화
if 'show_camera' not in st.session_state:
    st.session_state.show_camera = False

# 버튼 클릭 시 카메라 표시/숨기기
if st.button('카메라 켜기/끄기'):
    st.session_state.show_camera = not st.session_state.show_camera

# 카에라가 켜져 있을 때만 표시
if st.session_state.show_camera:
    img_file = st.camera_input('바코드를 촬영하세요')

    if img_file is not None:
        # 이지지 처리
        img = Image.open(img_file)
        st.image(img, caption='촬영된 이미지')

        # 바코드 인식
        decoded_object = pyzbar.decode(img)

        if decoded_object:
            for obj in decoded_object:
                st.success('바코드 인식 성공!')
                st.write(f'**타입:**{obj.type}')
                st.write(f"**데이터:** {obj.data.decode('utf-8')}")
        else:
            st.warning('바코드를 찾을 수 없습니다.')

        # 카메라 끄기 옵션
        if st.button('완료'):
            st.session_state.show_camera = False
            st.rerun()