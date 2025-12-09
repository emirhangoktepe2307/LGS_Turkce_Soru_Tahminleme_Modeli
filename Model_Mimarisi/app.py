"""
LGS Türkçe Soru Tahminleme Modeli - Streamlit Arayüzü
LLM tabanlı soru üretim ve tahminleme sistemi
"""

import streamlit as st
from streamlit_option_menu import option_menu
import json
from datetime import datetime

from config import (
    TURKCE_KONULARI,
    ALT_KONULAR,
    ZORLUK_SEVIYELERI,
    KARSILAMA_MESAJI,
    GEMINI_API_KEY
)
from llm_model import LGSTurkceModel
from data_processor import DataProcessor

# Sayfa yapılandırması
st.set_page_config(
    page_title="LGS Türkçe Soru Tahminleme",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS
st.markdown("""
<style>
    :root {
        --primary-color: #1e3a5f;
        --secondary-color: #4a90d9;
        --accent-color: #f39c12;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #e0e0e0;
        font-size: 1.1rem;
    }
    
    .stats-card {
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #4a90d9;
        margin: 0.5rem 0;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4a90d9;
    }
    
    .stats-label {
        color: #a0a0a0;
        font-size: 0.9rem;
    }
    
    .question-box {
        background: linear-gradient(145deg, #1a1a2e 0%, #0f0f1a 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0 12px 12px 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid #667eea;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_model():
    """Modeli başlatır ve önbelleğe alır."""
    try:
        model = LGSTurkceModel()
        processor = DataProcessor()
        return model, processor
    except Exception as e:
        st.error(f"Model başlatma hatası: {e}")
        return None, None


def show_header():
    """Ana başlığı gösterir."""
    st.markdown("""
    <div class="main-header">
        <h1>📚 LGS Türkçe Soru Tahminleme Modeli</h1>
        <p>LLM Tabanlı Yapay Zeka Soru Üretim Sistemi</p>
    </div>
    """, unsafe_allow_html=True)


def show_stats(model):
    """İstatistikleri gösterir."""
    stats = model.get_model_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stats['toplam_soru']}</div>
            <div class="stats-label">Eğitim Verisi</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{len(TURKCE_KONULARI)}</div>
            <div class="stats-label">Konu Sayısı</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stats['uretim_sayisi']}</div>
            <div class="stats-label">Üretilen Soru</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">🤖</div>
            <div class="stats-label">{stats['model']}</div>
        </div>
        """, unsafe_allow_html=True)


def soru_uret_sayfasi(model):
    """Soru üretme sayfası."""
    st.header("🎯 Yeni Soru Üret")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📝 Ayarlar")
        
        konu = st.selectbox(
            "Konu Seçin",
            options=TURKCE_KONULARI,
            index=0
        )
        
        alt_konular = ALT_KONULAR.get(konu, ["Genel"])
        alt_konu = st.selectbox(
            "Alt Konu Seçin",
            options=["Genel"] + alt_konular,
            index=0
        )
        
        zorluk = st.select_slider(
            "Zorluk Seviyesi",
            options=ZORLUK_SEVIYELERI,
            value="Orta"
        )
        
        adet = st.slider(
            "Soru Sayısı",
            min_value=1,
            max_value=10,
            value=3
        )
        
        if st.button("🚀 Soruları Üret", use_container_width=True):
            with st.spinner("🤖 Model sorular üretiyor..."):
                try:
                    alt_konu_param = None if alt_konu == "Genel" else alt_konu
                    response = model.generate_questions(
                        konu=konu,
                        zorluk=zorluk,
                        adet=adet,
                        alt_konu=alt_konu_param
                    )
                    st.session_state['generated_questions'] = response
                except Exception as e:
                    st.error(f"Soru üretme hatası: {e}")
    
    with col2:
        st.subheader("📄 Üretilen Sorular")
        
        if 'generated_questions' in st.session_state:
            st.markdown(st.session_state['generated_questions'])
            
            if st.button("🗑️ Temizle", use_container_width=True):
                del st.session_state['generated_questions']
                st.rerun()
        else:
            st.info("👆 Sol panelden ayarları yapın ve 'Soruları Üret' butonuna tıklayın.")


def konu_tahmini_sayfasi(model):
    """Konu tahmini sayfası."""
    st.header("🔍 Konu Tahmini")
    
    st.markdown("""
    Bir Türkçe sorusu girin, model bu sorunun hangi konuya ait olduğunu tahmin etsin.
    """)
    
    soru_metni = st.text_area(
        "Soru Metnini Girin:",
        height=150,
        placeholder="Örnek: Aşağıdaki cümlelerin hangisinde zıt anlamlı sözcükler bir arada kullanılmıştır?"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎯 Konuyu Tahmin Et", use_container_width=True):
            if soru_metni.strip():
                with st.spinner("Analiz ediliyor..."):
                    tahmin = model.predict_topic(soru_metni)
                    st.session_state['topic_prediction'] = tahmin
            else:
                st.warning("Lütfen bir soru girin!")
    
    with col2:
        if st.button("📊 Detaylı Analiz", use_container_width=True):
            if soru_metni.strip():
                with st.spinner("Detaylı analiz yapılıyor..."):
                    analiz = model.analyze_question(soru_metni)
                    st.session_state['question_analysis'] = analiz
            else:
                st.warning("Lütfen bir soru girin!")
    
    if 'topic_prediction' in st.session_state:
        st.success(f"**Tahmin Edilen Konu:** {st.session_state['topic_prediction']}")
    
    if 'question_analysis' in st.session_state:
        analiz = st.session_state['question_analysis']
        if 'error' not in analiz:
            st.markdown("### 📋 Detaylı Analiz")
            st.markdown(analiz.get('analiz', ''))


def chatbot_sayfasi(model):
    """Sohbet botu sayfası."""
    st.header("💬 Türkçe Asistanı")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Türkçe dersiyle ilgili bir soru sorun..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Düşünüyorum..."):
                response = model.chat(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()


def konu_anlatimi_sayfasi(model):
    """Konu anlatımı sayfası."""
    st.header("📖 Konu Anlatımı")
    
    konu = st.selectbox(
        "Anlatılmasını istediğiniz konuyu seçin:",
        options=TURKCE_KONULARI
    )
    
    alt_konular = ALT_KONULAR.get(konu, [])
    if alt_konular:
        alt_konu = st.selectbox(
            "Alt konu seçin (isteğe bağlı):",
            options=["Genel"] + alt_konular
        )
    else:
        alt_konu = "Genel"
    
    if st.button("📚 Konuyu Anlat", use_container_width=True):
        with st.spinner("Konu anlatımı hazırlanıyor..."):
            konu_text = konu if alt_konu == "Genel" else f"{konu} - {alt_konu}"
            response = model.explain_topic(konu_text)
            st.markdown(response)


def veri_istatistikleri_sayfasi(processor):
    """Veri istatistikleri sayfası."""
    st.header("📊 Veri İstatistikleri")
    
    stats = processor.get_statistics()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Konulara Göre Dağılım")
        if stats['konulara_gore']:
            import pandas as pd
            df = pd.DataFrame(
                list(stats['konulara_gore'].items()),
                columns=['Konu', 'Soru Sayısı']
            )
            st.bar_chart(df.set_index('Konu'))
    
    with col2:
        st.subheader("Zorluklara Göre Dağılım")
        if stats['zorluklara_gore']:
            import pandas as pd
            df = pd.DataFrame(
                list(stats['zorluklara_gore'].items()),
                columns=['Zorluk', 'Soru Sayısı']
            )
            st.bar_chart(df.set_index('Zorluk'))
    
    st.markdown("---")
    st.subheader("📋 Özet Bilgiler")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Toplam Soru", stats['toplam_soru'])
    with col2:
        st.metric("Konu Sayısı", len(stats['konulara_gore']))
    with col3:
        st.metric("Zorluk Seviyesi", len(stats['zorluklara_gore']))


def main():
    """Ana uygulama fonksiyonu."""
    # API key kontrolü
    if GEMINI_API_KEY == "BURAYA_API_ANAHTARINIZI_GIRIN":
        st.error("""
        ⚠️ **Gemini API Anahtarı Ayarlanmamış!**
        
        Lütfen `config.py` dosyasındaki `GEMINI_API_KEY` değerini ayarlayın.
        
        API anahtarı almak için: https://makersuite.google.com/app/apikey
        """)
        st.stop()
    
    # Modeli başlat
    model, processor = initialize_model()
    
    if model is None:
        st.error("Model başlatılamadı!")
        st.stop()
    
    # Başlık
    show_header()
    
    # Sidebar menü
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=80)
        st.title("Menü")
        
        selected = option_menu(
            menu_title=None,
            options=[
                "Ana Sayfa",
                "Soru Üret",
                "Konu Tahmini",
                "Sohbet Botu",
                "Konu Anlatımı",
                "İstatistikler"
            ],
            icons=[
                "house",
                "magic",
                "search",
                "chat-dots",
                "book",
                "bar-chart"
            ],
            default_index=0,
            styles={
                "container": {"background-color": "#1a1a2e"},
                "icon": {"color": "#667eea"},
                "nav-link": {
                    "color": "#fafafa",
                    "font-size": "1rem",
                    "--hover-color": "#16213e"
                },
                "nav-link-selected": {
                    "background-color": "#667eea"
                }
            }
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Hakkında")
        st.markdown("""
        Bu sistem LLM tabanlı soru 
        tahminleme modeli kullanır.
        
        **Sadece Türkçe dersi** için
        tasarlanmıştır.
        """)
    
    # Sayfa yönlendirme
    if selected == "Ana Sayfa":
        show_stats(model)
        st.markdown("---")
        st.markdown(KARSILAMA_MESAJI)
    
    elif selected == "Soru Üret":
        soru_uret_sayfasi(model)
    
    elif selected == "Konu Tahmini":
        konu_tahmini_sayfasi(model)
    
    elif selected == "Sohbet Botu":
        chatbot_sayfasi(model)
    
    elif selected == "Konu Anlatımı":
        konu_anlatimi_sayfasi(model)
    
    elif selected == "İstatistikler":
        veri_istatistikleri_sayfasi(processor)


if __name__ == "__main__":
    main()
