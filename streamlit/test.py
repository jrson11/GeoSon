import streamlit as st

password = st.sidebar.text_input("Password:", value="")

# select our text input field and make it into a password input
js = "el = document.querySelectorAll('.sidebar-content input')[0]; el.type = 'password';"

# passing js code to the onerror handler of an img tag with no src
# triggers an error and allows automatically running our code
html = f'<img src onerror="{js}">'

# in contrast to st.write, this seems to allow passing javascript
div = Div(text=html)
st.bokeh_chart(div)

if password != os.environ["PASSWORD"]:
    st.error("the password you entered is incorrect")

