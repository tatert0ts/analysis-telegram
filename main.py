import json
import streamlit as st
import warnings
from calculations import data_cal
from markdown import *
from PIL import Image
import io

st.set_page_config(layout="wide")
warnings.filterwarnings("ignore")

badge_url = "https://img.shields.io/badge/Star-Click%20Here-blue?logo=github&style=social"
repo_url = "https://github.com/tatert0ts/analysis-telegram"

with st.sidebar:
    st.title('Analyzing Telegram Conversations')
    st.write(text) 
    data = st.file_uploader('Upload Chat File:',type='json')
    picture = st.file_uploader('Upload Picture File:')

    # st.markdown(
    #     f'<a href="{repo_url}"><img src="{badge_url}" alt="Star" style="vertical-align: middle;"></a>',
    #     unsafe_allow_html=True
    # )

# Function to resize the image proportionately
def resize_image_proportionately(image_data, max_width, max_height):
    image = Image.open(io.BytesIO(image_data))
    image.thumbnail((max_width, max_height))  # This resizes the image proportionately
    return image

if data is not None: 
    data = json.load(data)

    data_results = data_cal(data)
    variable_names = [
        "date_start", "date_end", "num_parti", "num_msg", "emoji_common",
        "fig_msg", "fig_mediatype", "fig_avgday", "fig_avghour",
        "fig_words", "df_table", "df_pin_person", "df_pin_count", "df_phone_person", "df_phone_count",
        "avgnum_days", "fig_avg_mediatype", "activeday", "activehour", "activedf", "streakcount", "streakstart", "streakend"
    ]

    for i, result in enumerate(data_results):
        if variable_names[i]:
            globals()[variable_names[i]] = result

    ###### formatting the layout for each container
    def summary_layout():
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1 : 
            st.markdown(date_range_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {date_start}   
            to {date_end}
            ''')
        with col2:
            st.markdown(parti_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {num_parti}  
            ''')
        with col3:
            st.markdown(msg_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {num_msg}  
            ''')
        with col4:
            st.markdown(call_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {df_phone_count}  
            ''')
        with col5:
            st.markdown(pin_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {df_pin_count}  
            ''')
        with col6:
            st.markdown(sticker_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {emoji_common}  
            ''')
        with col7:
            st.markdown(streak_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {streakcount} days

            > {streakstart}  
            to {streakend}
            ''')

    def summary_layout_2():
        col1, col2, col3, col7 = st.columns(4)
        with col1 : 
            st.markdown(date_range_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {date_start}   
            to {date_end}
            ''')
        with col2:
            st.markdown(parti_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {num_parti}  
            ''')
        with col3:
            st.markdown(msg_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {num_msg}  
            ''')
        with col7:
            st.markdown(streak_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {streakcount} days

            > {streakstart}  
            to {streakend}
            ''')
        col4, col5, col6, col8 = st.columns(4)
        with col4:
            st.markdown(call_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {df_phone_count}  
            ''')
        with col5:
            st.markdown(pin_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {df_pin_count}  
            ''')
        with col6:
            st.markdown(sticker_title, unsafe_allow_html=True)
            st.markdown(f'''
            > {emoji_common}  
            ''')
        with col8:
            '' ''

    def main_layout():
        st.divider()
        maincol1, maincol2 = st.columns(2)
        with maincol1:
            st.markdown(fig_msg_title, unsafe_allow_html=True)
            fig_msg
            st.markdown(fig_avgmediatype_title, unsafe_allow_html=True)
            fig_avg_mediatype
            st.markdown(fig_words_title, unsafe_allow_html=True)
            fig_words
        with maincol2:
            st.markdown(fig_avgday_title, unsafe_allow_html=True)
            fig_avgday
            st.markdown(fig_avghour_title, unsafe_allow_html=True)
            fig_avghour
            st.markdown(active_title, unsafe_allow_html=True)
            activedf
            st.markdown(firstconvo_title, unsafe_allow_html=True)
            st.table(df_table)
            

    ###### formatting the layout for each container depending on picture
    if picture is None:
        summary_layout()
        main_layout()

    if picture is not None:
        col1, col2 = st.columns([1, 2])
        with col1:
            bytes_data = picture.getvalue()
            resized_image = resize_image_proportionately(bytes_data, max_width=300, max_height=300)
            st.image(resized_image)
        with col2:
            summary_layout_2() 
        main_layout()