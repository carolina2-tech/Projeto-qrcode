import streamlit as st
import qrcode
import json
from PIL import Image
import io

st.set_page_config(page_title="Sistema QR Code", layout="wide")
st.title("📦 Sistema de QR Code - Armazenamento Inteligente")

# Abas
tab1, tab2 = st.tabs(["Cadastrar Produto", "Gerar QR Code"])

with tab1:
    st.header("Cadastrar Novo Produto")
    with st.form("product_form"):
        product_id = st.text_input("ID do Produto*")
        product_name = st.text_input("Nome do Produto*")
        product_category = st.selectbox("Categoria", ["", "Ferramentas", "Eletrônicos", "Móveis", "Alimentos", "Roupas"])
        product_quantity = st.number_input("Quantidade", min_value=0, value=1)
        product_location = st.text_input("Localização*")
        
        submitted = st.form_submit_button("Salvar Produto")
        
        if submitted:
            if not all([product_id, product_name, product_location]):
                st.error("Preencha os campos obrigatórios (*)")
            else:
                product_data = {
                    "id": product_id,
                    "name": product_name,
                    "category": product_category,
                    "quantity": product_quantity,
                    "location": product_location
                }
                st.session_state.product_data = product_data
                st.success("Produto salvo! Vá para a aba 'Gerar QR Code'")

with tab2:
    st.header("Gerar QR Code")
    if "product_data" not in st.session_state:
        st.warning("Cadastre um produto primeiro na aba 'Cadastrar Produto'")
    else:
        st.write("**Produto:**", st.session_state.product_data["name"])
        
        # Gerar QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(json.dumps(st.session_state.product_data))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Converter para bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        
        # Exibir QR Code
        st.image(img_bytes, width=300)
        
        # Botão de download
        st.download_button(
            label="Baixar QR Code",
            data=img_bytes,
            file_name=f"qrcode_{st.session_state.product_data['id']}.png",
            mime="image/png"
        )
