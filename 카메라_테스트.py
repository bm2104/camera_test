import streamlit as st
from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout

st.title('카메라 테스트')


class CameraApp(App):
    def build(self):
        layout = BoxLayout()
        
        # 카메라 위젯 생성
        camera = Camera(play=True, resolution=(640, 480))
        layout.add_widget(camera)
        
        return layout


if st.button('카메라'): 
    if __name__ == '__main__':
        CameraApp().run()