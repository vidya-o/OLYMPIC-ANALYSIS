import numpy as np
from streamlit import columns


def fetch_medal_tally(df, Year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'region', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if Year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if Year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if Year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(Year)]
    if Year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == Year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df, col):

    nations_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return nations_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    return (temp_df['Name'].value_counts().head(15).reset_index(name='MedalCount')
            .merge(df[['Name', 'Sport', 'region']], on='Name').drop_duplicates('Name'))


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    return (temp_df['Name'].value_counts().head(10).reset_index(name='Medals')
            .merge(df[['Name', 'Sport']], on='Name').drop_duplicates('Name'))


def weight_v_height(df, sport):
    # Drop duplicates
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Replace NaN values in the 'Medal' column with 'No Medal'
    athlete_df['Medal'] = athlete_df['Medal'].fillna('No Medal')

    # Filter by sport if not 'Overall'
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    # Drop duplicates
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Count the number of male athletes by year
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year')['Name'].count().reset_index()

    # Count the number of female athletes by year
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year')['Name'].count().reset_index()

    # Merge the counts of male and female athletes by year
    final = men.merge(women, on='Year', how='left')

    # Rename columns to 'Male' and 'Female'
    final = final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'})

    # Replace NaN values with 0
    final['Female'] = final['Female'].fillna(0)

    return final
