import streamlit as st

def template_showcase():
    st.header("Choose Theme & Output Type")
    themes = [
        {"id": "light", "name": "Light", "desc": "Clean and professional design."},
        {"id": "glassmorphism", "name": "Glassmorphism", "desc": "Modern, translucent aesthetic."},
        {"id": "terminal", "name": "Terminal", "desc": "Retro, command-line style."},
    ]
    output_types = [{"id": "html", "name": "HTML/CSS"}, {"id": "tailwind", "name": "TailwindCSS"}]
    
    st.subheader("Themes")
    cols = st.columns(3)
    theme = st.session_state.get("theme", "light")
    for i, t in enumerate(themes):
        with cols[i]:
            if st.button(t["name"], key=f"theme_{t['id']}"):
                st.session_state.theme = t["id"]
            st.markdown(f"<p>{t['desc']}</p>", unsafe_allow_html=True)
            if theme == t["id"]:
                st.markdown("<p class='selected'>Selected</p>", unsafe_allow_html=True)
    
    st.subheader("Output Type")
    cols = st.columns(2)
    output_type = st.session_state.get("output_type", "html")
    for i, ot in enumerate(output_types):
        with cols[i]:
            if st.button(ot["name"], key=f"output_{ot['id']}"):
                st.session_state.output_type = ot["id"]
            if output_type == ot["id"]:
                st.markdown("<p class='selected'>Selected</p>", unsafe_allow_html=True)
    
    return theme, output_type