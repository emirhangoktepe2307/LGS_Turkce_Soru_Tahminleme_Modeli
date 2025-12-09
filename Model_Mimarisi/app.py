"""
LGS Türkçe Soru Üretici - Streamlit Arayüzü
Ana uygulama dosyası - Web tabanlı kullanıcı arayüzü
"""

import streamlit as st
from streamlit_option_menu import option_menu
import json
from datetime import datetime

# Proje modüllerini içe aktar
from config import (
    TURKCE_KONULARI, 
    ALT_KONULAR, 
    ZORLUK_SEVIYELERI,
    KARSILAMA_MESAJI,
    GEMINI_API_KEY
)
from gemini_rag import TurkceRAG
from soru_uretici import SoruYoneticisi
from turkce_chroma_setup import (
    create_chroma_client, 
    get_embedding_function,
    setup_collection,
    load_questions_from_json,
    add_questions_to_collection,
    query_similar_questions
)

# Sayfa yapılandırması
st.set_page_config(
    page_title="LGS Türkçe Soru Üretici",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS
st.markdown("""
<style>
    /* Ana tema renkleri */
    :root {
        --primary-color: #1e3a5f;
        --secondary-color: #4a90d9;
        --accent-color: #f39c12;
        --background-dark: #0e1117;
        --text-light: #fafafa;
    }
    
    /* Başlık stili */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #4a90d9 100%);
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
    
    /* Kart stili */
    .question-card {
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #4a90d9;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(74, 144, 217, 0.2);
    }
    
    .stats-card {
        background: linear-gradient(145deg, #0f3460 0%, #1a1a2e 100%);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #4a90d9;
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
    
    /* Soru kutusu */
    .soru-box {
        background: #1a1a2e;
        border-left: 4px solid #f39c12;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
    
    /* Cevap butonu */
    .cevap-dogru {
        background-color: #27ae60 !important;
        color: white !important;
    }
    
    .cevap-yanlis {
        background-color: #e74c3c !important;
        color: white !important;
    }
    
    /* Sidebar stili */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #0e1117 100%);
    }
    
    /* Buton stili */
    .stButton > button {
        background: linear-gradient(135deg, #4a90d9 0%, #1e3a5f 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(74, 144, 217, 0.4);
    }
    
    /* Expander stili */
    .streamlit-expanderHeader {
        background: #1a1a2e;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_system():
    """Sistemi başlatır ve önbelleğe alır."""
    try:
        # ChromaDB kurulumu
        client = create_chroma_client()
        embedding_function = get_embedding_function()
        collection = setup_collection(client, embedding_function)
        
        # Mevcut soruları yükle
        try:
            from config import DATA_FILE
            from pathlib import Path
            if Path(DATA_FILE).exists():
                data = load_questions_from_json(DATA_FILE)
                add_questions_to_collection(collection, data)
        except Exception as e:
            st.warning(f"Veri yükleme uyarısı: {e}")
        
        # RAG sistemi
        rag = TurkceRAG(collection=collection)
        
        # Soru yöneticisi
        soru_yoneticisi = SoruYoneticisi()
        
        return rag, soru_yoneticisi, collection
    
    except Exception as e:
        st.error(f"Sistem başlatma hatası: {e}")
        return None, None, None


def show_header():
    """Ana başlığı gösterir."""
    st.markdown("""
    <div class="main-header">
        <h1>📚 LGS Türkçe Soru Üretici</h1>
        <p>Yapay Zeka Destekli Soru Üretim ve Çalışma Platformu</p>
    </div>
    """, unsafe_allow_html=True)


def show_stats(soru_yoneticisi):
    """İstatistikleri gösterir."""
    stats = soru_yoneticisi.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stats['toplam_soru']}</div>
            <div class="stats-label">Toplam Soru</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stats['ai_uretimi']}</div>
            <div class="stats-label">AI Üretimi</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stats['gercek_sinav']}</div>
            <div class="stats-label">Gerçek Sınav</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{len(TURKCE_KONULARI)}</div>
            <div class="stats-label">Konu Sayısı</div>
        </div>
        """, unsafe_allow_html=True)


def soru_uret_sayfasi(rag, soru_yoneticisi):
    """Soru üretme sayfası."""
    st.header("🎯 Yeni Soru Üret")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📝 Ayarlar")
        
        # Konu seçimi
        konu = st.selectbox(
            "Konu Seçin",
            options=TURKCE_KONULARI,
            index=0
        )
        
        # Alt konu seçimi
        alt_konular = ALT_KONULAR.get(konu, ["Genel"])
        alt_konu = st.selectbox(
            "Alt Konu Seçin",
            options=alt_konular,
            index=0
        )
        
        # Zorluk seçimi
        zorluk = st.select_slider(
            "Zorluk Seviyesi",
            options=ZORLUK_SEVIYELERI,
            value="Orta"
        )
        
        # Soru sayısı
        adet = st.slider(
            "Soru Sayısı",
            min_value=1,
            max_value=10,
            value=3
        )
        
        # Üret butonu
        if st.button("🚀 Soruları Üret", use_container_width=True):
            with st.spinner("Sorular üretiliyor..."):
                try:
                    response = rag.generate_questions(
                        konu=konu,
                        alt_konu=alt_konu,
                        zorluk=zorluk,
                        adet=adet
                    )
                    st.session_state['generated_questions'] = response
                    st.session_state['current_konu'] = konu
                    st.session_state['current_alt_konu'] = alt_konu
                    st.session_state['current_zorluk'] = zorluk
                except Exception as e:
                    st.error(f"Soru üretme hatası: {e}")
    
    with col2:
        st.subheader("📄 Üretilen Sorular")
        
        if 'generated_questions' in st.session_state:
            st.markdown(st.session_state['generated_questions'])
            
            # Kaydet butonu
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("💾 Veritabanına Kaydet", use_container_width=True):
                    # Soruları ayrıştır ve kaydet
                    parsed = soru_yoneticisi.parse_generated_question(
                        st.session_state['generated_questions']
                    )
                    
                    if parsed:
                        ids = soru_yoneticisi.add_questions_batch(
                            parsed,
                            konu=st.session_state.get('current_konu', 'Genel'),
                            alt_konu=st.session_state.get('current_alt_konu', ''),
                            zorluk=st.session_state.get('current_zorluk', 'Orta')
                        )
                        st.success(f"✅ {len(ids)} soru veritabanına kaydedildi!")
                    else:
                        st.warning("Sorular ayrıştırılamadı. Manuel kayıt gerekebilir.")
            
            with col_b:
                if st.button("🗑️ Temizle", use_container_width=True):
                    del st.session_state['generated_questions']
                    st.rerun()
        else:
            st.info("👆 Sol panelden ayarları yapın ve 'Soruları Üret' butonuna tıklayın.")


def chatbot_sayfasi(rag):
    """Sohbet botu sayfası."""
    st.header("💬 Türkçe Asistanı")
    
    # Sohbet geçmişi
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Geçmiş mesajları göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Kullanıcı girişi
    if prompt := st.chat_input("Türkçe dersiyle ilgili bir soru sorun..."):
        # Kullanıcı mesajını ekle
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Asistan yanıtı
        with st.chat_message("assistant"):
            with st.spinner("Düşünüyorum..."):
                response = rag.generate_response(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Temizle butonu
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()


def soru_bankasi_sayfasi(soru_yoneticisi):
    """Soru bankası sayfası."""
    st.header("📖 Soru Bankası")
    
    # Filtreler
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_konu = st.selectbox(
            "Konuya Göre Filtrele",
            options=["Tümü"] + TURKCE_KONULARI
        )
    
    with col2:
        filter_zorluk = st.selectbox(
            "Zorluğa Göre Filtrele",
            options=["Tümü"] + ZORLUK_SEVIYELERI
        )
    
    with col3:
        filter_kaynak = st.selectbox(
            "Kaynağa Göre Filtrele",
            options=["Tümü", "Gerçek Sınav", "AI Üretimi"]
        )
    
    # Soruları getir
    all_questions = soru_yoneticisi.data.get("sorular", [])
    
    # Filtrele
    filtered = all_questions
    
    if filter_konu != "Tümü":
        filtered = [q for q in filtered if q.get("konu") == filter_konu]
    
    if filter_zorluk != "Tümü":
        filtered = [q for q in filtered if q.get("zorluk") == filter_zorluk]
    
    if filter_kaynak == "Gerçek Sınav":
        filtered = [q for q in filtered if q.get("yil") != "AI-Üretimi"]
    elif filter_kaynak == "AI Üretimi":
        filtered = [q for q in filtered if q.get("yil") == "AI-Üretimi"]
    
    st.write(f"📊 Toplam {len(filtered)} soru bulundu.")
    
    # Soruları göster
    for i, soru in enumerate(filtered):
        with st.expander(f"Soru {i+1}: {soru.get('konu', 'Bilinmiyor')} - {soru.get('alt_konu', '')}"):
            st.markdown(f"**Zorluk:** {soru.get('zorluk', 'Bilinmiyor')} | **Yıl:** {soru.get('yil', 'Bilinmiyor')}")
            st.markdown("---")
            st.markdown(soru.get('soru_metni', ''))
            
            # Cevap göster/gizle
            if st.checkbox(f"Cevabı Göster", key=f"cevap_{i}"):
                st.success(f"**Doğru Cevap:** {soru.get('dogru_cevap', '')}")
                st.info(f"**Açıklama:** {soru.get('cevap_aciklamasi', '')}")


def quiz_sayfasi(soru_yoneticisi):
    """Quiz (sınav) sayfası."""
    st.header("📝 Quiz Modu")
    
    # Quiz başlatma
    if 'quiz_active' not in st.session_state:
        st.session_state.quiz_active = False
        st.session_state.quiz_questions = []
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
    
    if not st.session_state.quiz_active:
        st.subheader("🎮 Yeni Quiz Başlat")
        
        col1, col2 = st.columns(2)
        
        with col1:
            quiz_konu = st.selectbox(
                "Konu Seçin",
                options=["Karışık"] + TURKCE_KONULARI
            )
        
        with col2:
            quiz_adet = st.slider(
                "Soru Sayısı",
                min_value=5,
                max_value=20,
                value=10
            )
        
        if st.button("🚀 Quiz Başlat", use_container_width=True):
            konu = None if quiz_konu == "Karışık" else quiz_konu
            sorular = soru_yoneticisi.get_random_questions(adet=quiz_adet, konu=konu)
            
            if len(sorular) < quiz_adet:
                st.warning(f"Yeterli soru bulunamadı. {len(sorular)} soru ile devam ediliyor.")
            
            if sorular:
                st.session_state.quiz_questions = sorular
                st.session_state.quiz_active = True
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()
            else:
                st.error("Bu konuda hiç soru bulunamadı!")
    
    else:
        # Quiz devam ediyor
        if not st.session_state.quiz_submitted:
            st.info(f"📝 {len(st.session_state.quiz_questions)} soruluk quiz")
            
            for i, soru in enumerate(st.session_state.quiz_questions):
                st.markdown(f"### Soru {i+1}")
                st.markdown(soru.get('soru_metni', ''))
                
                answer = st.radio(
                    "Cevabınız:",
                    options=["A", "B", "C", "D"],
                    key=f"quiz_q_{i}",
                    horizontal=True
                )
                st.session_state.quiz_answers[i] = answer
                st.markdown("---")
            
            if st.button("✅ Sınavı Bitir", use_container_width=True):
                st.session_state.quiz_submitted = True
                st.rerun()
        
        else:
            # Sonuçlar
            st.subheader("📊 Sonuçlar")
            
            dogru = 0
            for i, soru in enumerate(st.session_state.quiz_questions):
                user_answer = st.session_state.quiz_answers.get(i, "")
                correct_answer = soru.get('dogru_cevap', '')
                
                is_correct = user_answer == correct_answer
                if is_correct:
                    dogru += 1
                
                with st.expander(
                    f"{'✅' if is_correct else '❌'} Soru {i+1}: {soru.get('konu', '')}"
                ):
                    st.markdown(soru.get('soru_metni', ''))
                    st.markdown(f"**Sizin Cevabınız:** {user_answer}")
                    st.markdown(f"**Doğru Cevap:** {correct_answer}")
                    st.info(f"**Açıklama:** {soru.get('cevap_aciklamasi', '')}")
            
            # Skor
            toplam = len(st.session_state.quiz_questions)
            puan = (dogru / toplam) * 100 if toplam > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Doğru", dogru)
            with col2:
                st.metric("Yanlış", toplam - dogru)
            with col3:
                st.metric("Puan", f"%{puan:.1f}")
            
            if st.button("🔄 Yeni Quiz", use_container_width=True):
                st.session_state.quiz_active = False
                st.session_state.quiz_submitted = False
                st.rerun()


def konu_anlatimi_sayfasi(rag):
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
            response = rag.explain_topic(konu_text)
            st.markdown(response)


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
    
    # Sistemi başlat
    rag, soru_yoneticisi, collection = initialize_system()
    
    if rag is None:
        st.error("Sistem başlatılamadı! Lütfen hata mesajlarını kontrol edin.")
        st.stop()
    
    # Başlık
    show_header()
    
    # Sidebar menü
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/books.png", width=80)
        st.title("Menü")
        
        selected = option_menu(
            menu_title=None,
            options=[
                "Ana Sayfa",
                "Soru Üret",
                "Sohbet Botu",
                "Soru Bankası",
                "Quiz",
                "Konu Anlatımı"
            ],
            icons=[
                "house",
                "magic",
                "chat-dots",
                "journal-text",
                "question-circle",
                "book"
            ],
            default_index=0,
            styles={
                "container": {"background-color": "#1a1a2e"},
                "icon": {"color": "#4a90d9"},
                "nav-link": {
                    "color": "#fafafa",
                    "font-size": "1rem",
                    "--hover-color": "#16213e"
                },
                "nav-link-selected": {
                    "background-color": "#4a90d9"
                }
            }
        )
        
        st.markdown("---")
        st.markdown("### 📊 Hızlı İstatistikler")
        stats = soru_yoneticisi.get_statistics()
        st.write(f"📚 Toplam: {stats['toplam_soru']} soru")
        st.write(f"🤖 AI: {stats['ai_uretimi']} soru")
    
    # Sayfa yönlendirme
    if selected == "Ana Sayfa":
        show_stats(soru_yoneticisi)
        st.markdown("---")
        st.markdown(KARSILAMA_MESAJI)
    
    elif selected == "Soru Üret":
        soru_uret_sayfasi(rag, soru_yoneticisi)
    
    elif selected == "Sohbet Botu":
        chatbot_sayfasi(rag)
    
    elif selected == "Soru Bankası":
        soru_bankasi_sayfasi(soru_yoneticisi)
    
    elif selected == "Quiz":
        quiz_sayfasi(soru_yoneticisi)
    
    elif selected == "Konu Anlatımı":
        konu_anlatimi_sayfasi(rag)


if __name__ == "__main__":
    main()

