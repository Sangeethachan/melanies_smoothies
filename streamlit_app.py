# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col



# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!
""")


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# If ingredients are selected
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    # Prepare insert statement
    my_insert_stmt = """insert into smoothies.public.orders
    values ('""" + ingredients_string + """')"""

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)  # Join fruits with spaces
    
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(name_on_order, ingredients)
        VALUES ('{name_on_order}', '{ingredients_string}')
    """

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

#    st.write(my_insert_stmt)
 #   st.stop()

    #time_to_insert = st.button('Submit Order')





