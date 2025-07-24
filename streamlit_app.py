# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

api_url = "https://my.smoothiefroot.com/api/fruit/watermelon"

try:
    response = requests.get(api_url, timeout=5)
    response.raise_for_status()
    try:
        data = response.json()
        st.success("✅ Successfully retrieved fruit data!")
        st.json(data)
    except ValueError:
        st.error("⚠️ API did not return valid JSON.")
        st.text(response.text[:500])  # limit to 500 characters to avoid dumping all HTML

except requests.exceptions.HTTPError as e:
    st.error(f"❌ HTTP Error: {response.status_code}")
    st.caption("The API returned an error page instead of JSON.")
    st.text(response.text[:500])  # show partial HTML
except requests.exceptions.Timeout:
    st.error("⏱️ Request timed out. Try again later.")
except requests.exceptions.RequestException as e:
    st.error(f"⚠️ Connection error: {e}")

# Write directly to the app
st.title(f":cup_with_straw: Cutomize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)
name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be:',name_on_order )

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("You selected:", option)


cnx= st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list= st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    ,max_selections=5)
if ingredients_list:
    # st.write("You selected:", ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string+= fruit_chosen +' '
    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")


       

    
