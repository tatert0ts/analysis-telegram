import pandas as pd
import spacy
import string
import plotly.express as px

# Load the English language model
sp = spacy.load('en_core_web_sm')
# Access the default set of stopwords provided by spaCy
spacy_stopwords = sp.Defaults.stop_words

def data_cal(data):
    msgs = data["messages"]
    df = pd.DataFrame(msgs)
    df['date'] = pd.to_datetime(df['date'])

    df1 = df[df['type'] != 'unsupported']
    df1['text'] = df1['text'].astype(str)
    df1['text'] = df1['text'].str.lower()
    df1['date_only'] = df1['date'].dt.date
    df1['date_weekdays'] = df1['date'].dt.day_name()
    df1['date_hour'] = df1['date'].dt.hour
    
    # total days conversation
    num_days = len(df1['date'].dt.date.unique())

    # most pinned msgs
    if 'action' in df1.columns and 'pin_message' in df1['action'].values:
        df_pin = df1[df1['action'] == 'pin_message'] 
        df_pin = df_pin['actor'].value_counts()
        df_pin_person = df_pin.idxmax()
        df_pin_count = df_pin.max()
    else:
        df_pin_person = None
        df_pin_count = 0

    # most phone call
    if 'action' in df1.columns and 'phone_call' in df1['action'].values:
        df_phone = df[df['action'] == 'phone_call']
        df_phone = df_phone['actor'].value_counts()
        df_phone_person = df_phone.idxmax()
        df_phone_count = df_phone.max()
    else:
        df_phone_person = None
        df_phone_count = 0

    # top sticker emoji 
    if 'sticker_emoji' in df1.columns:
        emoji_counts = df1['sticker_emoji'].value_counts()
        emoji_common = emoji_counts.idxmax()
    else: 
        emoji_common = None

    # by media types (video messages, bubble)
    df_media = df1[df1['media_type'].notnull()]
    df_media = df_media.groupby(['from','media_type']).size()
    df_media = pd.DataFrame(df_media).reset_index()
    df_media.columns.values[2] = 'count'
    # dictionary for renaming values
    rename_dict = {'video_file': 'video', 'video_message': 'bubble', 'voice_message': 'voice', 'animation': 'gif'} 
    # replace values using the dictionary
    df_media['media_type'] = df_media['media_type'].replace(rename_dict)
    df_media['avg'] = round(df_media['count']/num_days,1)
    fig_avg_mediatype = px.bar(df_media, x = 'media_type', y = 'avg',
                            color = 'from',
                            color_discrete_sequence = px.colors.sequential.Aggrnyl,
                            text_auto = True,
                            hover_data = {#'from':False,
                                           'media_type': False},
                            title = None
                            )
    fig_avg_mediatype.update_layout(hovermode="x", xaxis_title = None, yaxis_title = None, barmode = 'group',       
                            legend_title = None,
                            legend = dict(yanchor = "top", y = 0.98, xanchor = "right", x = 0.9)
                            )

    fig_mediatype = px.bar(df_media, x = 'media_type', y = 'count',
                            color = 'from',
                            color_discrete_sequence = px.colors.sequential.Aggrnyl,
                            text_auto = True,
                            hover_data = {'from':True, 'media_type': False},
                            # hover_name = 'from'
                            )
    fig_mediatype.update_layout(hovermode="x",
                            xaxis_title = None,
                            xaxis = {'categoryorder':'total descending'},
                            yaxis = dict(visible=False),
                            margin = dict(l = 50, r = 40, t = 50, b = 30),
                            legend_title = None,
                            legend = dict(yanchor = "top", y = 0.98, xanchor = "right", x = 0.9)
                            )


    # further cleaning to extract only text messages
    if 'forwarded_from' in df1.columns:
        df2 = df1[(df1['from'].notnull()) & (df1['media_type'].isnull()) & (df1['file'].isnull() & (df1['forwarded_from'].isnull()) & df1['text'].notnull())]
    else: 
        df2 = df1[(df1['from'].notnull()) & (df1['media_type'].isnull()) & (df1['file'].isnull() & df1['text'].notnull())]

    # timeframe
    date_start = min(df2.date).date().strftime("%B %d, %Y")
    date_end = max(df2.date).date().strftime("%B %d, %Y")

    # number of participants
    parti = df2['from'].unique()
    num_parti = len(parti)

    # number of texts
    num_msg = df2.shape[0]

    # average number of texts per day
    avgnum_days = round(num_msg/len(df2['date'].dt.date.unique()))

    date_unique = pd.DataFrame({'date': df2.date_only.unique()})
    date_unique = date_unique.sort_values(by='date')
    # difference between consecutive dates
    date_unique['diff'] = date_unique['date'].diff()

    # longest consecutive date sequence
    max_consecutive_dates = date_unique.groupby((date_unique['diff'] != pd.Timedelta(days=1)).cumsum())['date'].agg(['count', 'min', 'max'])
    longest_consecutive_dates = max_consecutive_dates.loc[max_consecutive_dates['count'].idxmax()]
    'longest streak is {} days, from {} to {}'.format(longest_consecutive_dates['count'], longest_consecutive_dates['min'], longest_consecutive_dates['max'])
    streakcount = longest_consecutive_dates['count']
    streakstart = longest_consecutive_dates['min'].strftime("%B %d, %Y")
    streakend = longest_consecutive_dates['max'].strftime("%B %d, %Y")

    # total number of messages
    fig_msg = px.pie(df2, names = "from", color = "from", color_discrete_sequence = px.colors.sequential.Aggrnyl)
    fig_msg.update_layout(legend_title = None,
                        legend = dict(yanchor = "top", y = 0.98, xanchor = "right", x = 0.9))
    fig_msg.update_traces(hovertemplate='from=%{label}<br>count=%{value}<extra></extra>')

    weekday_order = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }

    # average number of msgs per weekday
    df_avgday = (df2.groupby(['from','date_weekdays'])['date_only'].count()/df2.groupby(['from','date_weekdays'])['date_only'].nunique()).round().astype(int)
    df_avgday = pd.DataFrame(df_avgday).reset_index()
    # Map the weekday names to their corresponding numbers
    df_avgday['weekday_order'] = df_avgday['date_weekdays'].map(weekday_order)
    df_avgday.rename(columns={'date_only': 'count'}, inplace=True)
    # Sort the DataFrame by the weekday order
    df_avgday = df_avgday.sort_values(by='weekday_order')
    # Drop the 'weekday_order' column if no longer needed
    df_avgday = df_avgday.drop(columns=['weekday_order'])
    fig_avgday = px.line(df_avgday, x = 'date_weekdays', y = 'count',
                        color = 'from',
                        color_discrete_sequence = px.colors.sequential.Aggrnyl,
                        hover_data = {'date_weekdays': False},
                        # labels = {'date_only': 'count'}
                        )
    # fig_avgday.update_traces(textposition = "bottom")
    fig_avgday.update_layout(hovermode = "x",
                        yaxis_title = None,
                        xaxis_title = None,
                        xaxis = dict(showgrid = False),
                        yaxis = dict(showgrid = False),
                        margin = dict(l = 50, r = 40, t = 50, b = 30),
                        legend_title = None,
                        legend = dict(yanchor = "top", y = 0.98, xanchor = "right", x = 0.99)
                        )

    # average number of msgs per hour
    df_avghour = (df1.groupby(['from','date_hour'])['id'].count()/df1.groupby(['from','date_hour'])['date_only'].nunique()).round().astype(int)
    df_avghour = pd.DataFrame(df_avghour).reset_index()
    df_avghour.rename(columns={0: 'count'}, inplace=True)
    fig_avghour = px.line(df_avghour, x = 'date_hour', y = 'count',
                        color = 'from',
                        color_discrete_sequence = px.colors.sequential.Aggrnyl,
                        hover_data = {'date_hour': False},
                        labels = {'date_only': 'count'}
                        )
    fig_avghour.update_layout(hovermode = "x",
                            yaxis_title = None,
                            xaxis_title = None,
                            xaxis = dict(showgrid = False),
                            yaxis = dict(showgrid = False),
                            margin = dict(l = 50, r = 40, t = 50, b = 30),
                            legend_title = None,
                            legend = dict(yanchor = "top", y = 0.98, xanchor = "right", x = 0.99)
                            )
    
    # most active day
    idx = df_avgday.groupby('from')['count'].idxmax()
        # extract the hour from the index
    activeday = df_avgday.loc[idx, ['from', 'date_weekdays']]
    # most active hour
    idx = df_avghour.groupby('from')['count'].idxmax()
        # extract the hour from the index
    activehour = df_avghour.loc[idx, ['from', 'date_hour']]
    # most active time period
    activedf = pd.merge(activeday, activehour, on = "from")
    activedf = activedf.rename(columns={"date_hour": "hour", "date_weekdays": "day"})

    # frequent words
    df_text = df1[df1['text']!='']
    df_text['text'] = df_text['text'].fillna('')
    stop_words = spacy_stopwords
    stop_words.update([
        # singlish
        'ah', 'oh', 'la', 'sia', 'eh', 'lah', 'de', 'bah', 'leh',
        # variations of stopwords
        'u', 'ya', 'im', 'thn', 'lol', 'go', 'got',
        # variations of haha
        'hahahah', 'hahah', 'hahaha', 'hahahahah', 'haha', 'hahahaha', 'hahahaha',
        # variations of ok
        'okie', 'okay', 'ok'
        ])
    custom_punctuation = string.punctuation + '‘’“”–—' 
    # into a single string text, with each review separated by a space
    text = " ".join(review for review in df_text.text)
    # remove all punctuation characters from the text
    text = text.translate(str.maketrans('', '', custom_punctuation))
    # removing any extra whitespace and ensuring that the list only contains non-empty words
    cleaned_words = [word for word in text.split() if word.strip()]
    # convert into lowercase & checking words against stopwords
    cleaned_words = [word.lower() for word in cleaned_words if word.lower() not in stop_words]
    word_freq = pd.Series(cleaned_words).value_counts()
    common_words = pd.DataFrame(word_freq).head(15)
    common_words.reset_index(inplace=True)
    common_words.rename(columns={common_words.columns[0]: "word" }, inplace = True)
    fig_words = px.treemap(common_words, path=['word'],
                 values = 'count',
                 color_discrete_sequence = px.colors.sequential.Aggrnyl
                 )
    fig_words.update_traces(hovertemplate='<br>count=%{value}<extra></extra>')
    # fig_words.update_layout(title_x = 0.5)

    # first convo
    df_table = pd.DataFrame(df2[['from', 'text']].head(10)).reset_index(drop=True)

    return date_start, date_end, num_parti, num_msg, emoji_common, fig_msg, fig_mediatype, fig_avgday, fig_avghour, fig_words, df_table, df_pin_person, df_pin_count, df_phone_person, df_phone_count, avgnum_days, fig_avg_mediatype, activeday, activehour, activedf, streakcount, streakstart, streakend