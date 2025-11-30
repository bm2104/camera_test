import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode, RTCConfiguration
import cv2
from pyzbar import pyzbar
import av
import threading

# 전역 변수로 바코드 데이터 저장
if 'barcode_data' not in st.session_state:
    st.session_state.barcode_data = None
    st.session_state.barcode_type = None

class BarcodeScanner(VideoProcessorBase):
    def __init__(self):
        self.barcode_data = None
        self.barcode_type = None
        self.lock = threading.Lock()
    
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # 바코드 검출
        barcodes = pyzbar.decode(img)
        
        for barcode in barcodes:
            # 바코드 데이터 추출
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            
            # 바코드 주변에 사각형 그리기
            (x, y, w, h) = barcode.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # 텍스트 표시
            text = f"{barcode_type}: {barcode_data}"
            cv2.putText(img, text, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # 스레드 안전하게 데이터 저장
            with self.lock:
                self.barcode_data = barcode_data
                self.barcode_type = barcode_type
                st.session_state.barcode_data = barcode_data
                st.session_state.barcode_type = barcode_type
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("🔍 실시간 바코드 스캐너")
st.markdown("카메라를 바코드나 QR 코드에 향하게 하세요")

# RTC 설정
rtc_config = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# WebRTC 스트리머 시작
ctx = webrtc_streamer(
    key="barcode-scanner",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=BarcodeScanner,
    rtc_configuration=rtc_config,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# 바코드 감지 결과 표시
if ctx.state.playing:
    placeholder = st.empty()
    if ctx.video_processor:
        with ctx.video_processor.lock:
            if ctx.video_processor.barcode_data:
                placeholder.success(f"✅ 인식된 바코드: **{ctx.video_processor.barcode_data}** (타입: {ctx.video_processor.barcode_type})")
else:
    st.info("📹 위의 'START' 버튼을 클릭하여 카메라를 시작하세요")

# 세션 상태에 저장된 마지막 스캔 결과 표시
if st.session_state.barcode_data:
    st.markdown("### 📝 마지막 스캔 결과:")
    st.code(st.session_state.barcode_data)
    
    # 클립보드 복사 버튼 (선택사항)
    if st.button("📋 클립보드에 복사"):
        st.write("복사되었습니다!")
        st.balloons()