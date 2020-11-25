import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("app-dev/style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

icon("search")
selected = st.text_input("", "Search...")
button_clicked = st.button("🔍")



st.subheader("Design")
bgcolor = st.color_picker("Pick a Background color", "#95D6A4")
fontcolor = st.color_picker("Pick a Font Color","#fff")
html_temp = """
<div style="background-color:{};padding:10px">
<h1 style="color:{};text-align:center;">Streamlit Simple CSS Shape Generator </h1>
</div>
"""
st.markdown(html_temp.format(bgcolor,fontcolor),unsafe_allow_html=True)
st.markdown("<div><p style='color:{}'>Hello Streamlit</p></div>".format(bgcolor),unsafe_allow_html=True)
st.subheader("Modify Shape")
bgcolor2 = st.sidebar.color_picker("Pick a Bckground color")
height = st.sidebar.slider('Height Size',50,200,50)
width = st.sidebar.slider("Width Size",50,200,50)

# border = st.slider("Border Radius",10,60,10)
top_left_border = st.sidebar.number_input('Top Left Border',10,50,10)
top_right_border = st.sidebar.number_input('Top Right Border',10,50,10)
bottom_left_border = st.sidebar.number_input('Bottom Left Border',10,50,10)
bottom_right_border = st.sidebar.number_input('Bottom Right Border',10,50,10)
border_style = st.sidebar.selectbox("Border Style",["dotted","dashed","solid","double","groove","ridge","inset","outset","none","hidden"])
border_color = st.sidebar.color_picker("Pick a Border Color","#654FEF")
st.markdown(html_design.format(height,width,bgcolor2,top_left_border,top_right_border,bottom_left_border,bottom_right_border,border_style,border_color),unsafe_allow_html=True)
