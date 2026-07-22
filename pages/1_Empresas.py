import pandas as pd
import streamlit as st

from config import CURRENCIES
from core.database import init_db, create_company, list_companies
from utils.styles import apply_styles

st.set_page_config(page_title="Empresas", page_icon="🏢", layout="wide")
apply_styles()
init_db()

st.title("Empresas")

with st.form("company_form"):
    st.subheader("Registrar empresa")
    c1, c2 = st.columns(2)
    name = c1.text_input("Nombre comercial *")
    legal_name = c2.text_input("Razón social")
    tax_id = c1.text_input("Identificación fiscal")
    country = c2.text_input("País")
    city = c1.text_input("Ciudad")
    sector = c2.text_input("Sector")
    business_model = st.text_area("Modelo de negocio")
    c3, c4, c5 = st.columns(3)
    employees = c3.number_input("Empleados", min_value=0, step=1)
    annual_revenue = c4.number_input("Facturación anual aproximada", min_value=0.0)
    currency = c5.selectbox("Moneda", CURRENCIES)
    website = st.text_input("Sitio web")
    main_problem = st.text_area("Problema principal percibido por dirección")
    save = st.form_submit_button("Guardar empresa")

    if save:
        if not name.strip():
            st.error("El nombre comercial es obligatorio.")
        else:
            create_company({
                "name": name.strip(),
                "legal_name": legal_name.strip(),
                "tax_id": tax_id.strip(),
                "country": country.strip(),
                "city": city.strip(),
                "sector": sector.strip(),
                "business_model": business_model.strip(),
                "employees": int(employees),
                "annual_revenue": float(annual_revenue),
                "currency": currency,
                "website": website.strip(),
                "main_problem": main_problem.strip(),
            })
            st.success("Empresa registrada.")
            st.rerun()

companies = list_companies()
st.subheader("Directorio")
if companies:
    st.dataframe(pd.DataFrame(companies), use_container_width=True, hide_index=True)
else:
    st.info("No hay empresas registradas.")
