import streamlit as st
from PIL import Image
import time

# 페이지 설정 - 와이드 레이아웃, 패딩 최소화
st.set_page_config(
    page_title="바코드 스캐너",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 전체화면 카메라를 위한 CSS
st.markdown("""
<style>
    /* Streamlit 기본 요소 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 패딩 제거 */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* 카메라가 활성화되면 전체화면 */
    .fullscreen-mode [data-testid="stCameraInput"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        z-index: 9999 !important;
        background: black !important;
    }
    
    /* 카메라 비디오 전체화면 */
    .fullscreen-mode video {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
    }
    
    /* 카메라 컨트롤 버튼 스타일 */
    .fullscreen-mode [data-testid="stCameraInput"] button {
        position: fixed !important;
        bottom: 30px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 10000 !important;
        background: #ff4b4b !important;
        border: none !important;
        padding: 20px 40px !important;
        border-radius: 50px !important;
        font-size: 18px !important;
        color: white !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
    }
    
    /* 닫기 버튼 */
    .close-button {
        position: fixed !important;
        top: 20px !important;
        right: 20px !important;
        z-index: 10001 !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 25px !important;
        font-size: 16px !important;
        cursor: pointer !important;
        color: #333 !important;
    }
    
    /* 모바일 최적화 */
    @media only screen and (max-width: 768px) {
        .fullscreen-mode video {
            object-fit: cover !important;
        }
        
        .fullscreen-mode [data-testid="stCameraInput"] button {
            bottom: 50px !important;
            padding: 25px 50px !important;
            font-size: 20px !important;
        }
    }
    
    /* 시작 버튼 스타일 */
    .start-button button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-size: 20px !important;
        padding: 15px 40px !important;
        border-radius: 30px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .start-button button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False
if 'photo_taken' not in st.session_state:
    st.session_state.photo_taken = None
if 'scan_result' not in st.session_state:
    st.session_state.scan_result = None

# 카메라가 비활성화 상태일 때 - 시작 화면
if not st.session_state.camera_active:
    # 중앙 정렬을 위한 컬럼
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("# 📸 바코드 스캐너")
        st.markdown("### 버튼을 눌러 카메라를 시작하세요")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 카메라 시작 버튼
        if st.button("📷 카메라 켜기", key="start_camera", use_container_width=True, help="클릭하면 전체화면 카메라가 열립니다"):
            st.session_state.camera_active = True
            st.session_state.photo_taken = None
            st.session_state.scan_result = None
            st.rerun()
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # 사용 안내
        with st.expander("📖 사용 방법"):
            st.markdown("""
            1. **카메라 켜기** 버튼을 누르면 전체화면 카메라가 열립니다
            2. 바코드를 카메라 화면에 맞춰주세요
            3. **📸 Take Photo** 버튼을 눌러 촬영합니다
            4. 자동으로 바코드를 인식합니다
            5. **닫기** 버튼으로 카메라를 종료합니다
            """)
        
        # 이전 스캔 결과가 있으면 표시
        if st.session_state.scan_result:
            st.markdown("---")
            st.markdown("### 📊 최근 스캔 결과")
            st.success(f"**바코드:** {st.session_state.scan_result['data']}")
            st.info(f"**타입:** {st.session_state.scan_result['type']}")

# 카메라가 활성화된 상태 - 전체화면 카메라
else:
    # 전체화면 모드 적용
    st.markdown('<div class="fullscreen-mode">', unsafe_allow_html=True)
    
    # 닫기 버튼 (오른쪽 상단)
    close_col1, close_col2 = st.columns([10, 1])
    with close_col2:
        if st.button("✖ 닫기", key="close_camera", help="카메라 종료"):
            st.session_state.camera_active = False
            st.rerun()
    
    # 카메라 입력
    photo = st.camera_input("", key=f"camera_{int(time.time())}", label_visibility="collapsed")
    
    # 사진이 찍혔을 때 처리
    if photo is not None:
        st.session_state.photo_taken = photo
        image = Image.open(photo)
        
        # 바코드 인식 시도
        try:
            from pyzbar import pyzbar
            decoded_objects = pyzbar.decode(image)
            
            if decoded_objects:
                # 첫 번째 바코드만 처리
                obj = decoded_objects[0]
                barcode_data = obj.data.decode('utf-8')
                barcode_type = obj.type
                
                # 결과 저장
                st.session_state.scan_result = {
                    'data': barcode_data,
                    'type': barcode_type
                }
                
                # 성공 메시지와 함께 자동으로 카메라 종료
                st.balloons()
                st.success(f"✅ 바코드 인식 성공!")
                st.info(f"**데이터:** {barcode_data}")
                st.info(f"**타입:** {barcode_type}")
                
                # 2초 후 자동으로 메인 화면으로 돌아가기
                time.sleep(2)
                st.session_state.camera_active = False
                st.rerun()
            else:
                # 바코드를 찾지 못한 경우
                st.warning("⚠️ 바코드를 찾을 수 없습니다. 다시 시도해주세요.")
                
                # 재시도 버튼
                retry_col1, retry_col2, retry_col3 = st.columns([1, 1, 1])
                with retry_col2:
                    if st.button("🔄 다시 촬영", key="retry", use_container_width=True):
                        st.session_state.photo_taken = None
                        st.rerun()
                        
        except ImportError:
            st.error("""
            ⚠️ 바코드 인식 라이브러리가 설치되지 않았습니다.
            
            다음 명령어로 설치해주세요:
            ```bash
            pip install pyzbar
            # Linux: sudo apt-get install libzbar0
            # Mac: brew install zbar
            ```
            """)
            
            # 이미지만 표시
            st.image(image, caption="촬영된 이미지", use_column_width=True)
            
            # 돌아가기 버튼
            if st.button("↩ 돌아가기", key="return"):
                st.session_state.camera_active = False
                st.rerun()
        except Exception as e:
            st.error(f"오류 발생: {str(e)}")
            
            # 돌아가기 버튼
            if st.button("↩ 돌아가기", key="return_error"):
                st.session_state.camera_active = False
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# JavaScript로 추가 전체화면 제어 (선택사항)
if st.session_state.camera_active:
    st.markdown("""
    <script>
    // 카메라가 켜지면 자동으로 전체화면 시도
    setTimeout(() => {
        const elem = document.documentElement;
        if (elem.requestFullscreen && !document.fullscreenElement) {
            elem.requestFullscreen().catch(err => {
                console.log('전체화면 전환 실패:', err);
            });
        }
    }, 500);
    
    // ESC 키로 카메라 종료
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            // Streamlit의 close 버튼 클릭
            const closeBtn = document.querySelector('[data-testid="baseButton-secondary"]');
            if (closeBtn && closeBtn.textContent.includes('닫기')) {
                closeBtn.click();
            }
        }
    });
    </script>
    """, unsafe_allow_html=True)