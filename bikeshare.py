#    %cd ; %pwd ; %ls


import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
months = ["january", "february", "march", "april", "may", "june", "all"]
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday" , "all"]

"""
S1: make sure you can slice dictionary: CITY_DATA by list: cities.

city = 'new york city'
city_file = CITY_DATA[city]
print(city_file)
works
"""

"""
S2: make sure can read csv file in for each city


city = 'chicago'
# load data file into a dataframe
df = pd.read_csv(CITY_DATA[city])
#print(df.head())
print(df.columns)
"""

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Select a city to analyze: chicago -'the windy city', new york city - 'the big apple', washington - 'the capital'\n").lower()

    while city not in cities:
        print('Please select one of these 3 cities : chicago, new york city, washington')
        city = input("Select a city to analyze: chicago -'the windy city', new york city - 'the big apple', washington - 'the capital'\n").lower()
    print("You selected city : ", city)

    # get user input for month (january, february, ... , june, all)
    month = input("Select a month to analyze: january, february, march, april, may, june, or all").lower()
    while month not in months:
        print("Please correctly enter the month you would like to analyze ")
        month = input("Select a month to analyze: january, february, march, april, may, june, or all")
    print("You selected month : ", month)

    # get user input for day of week (monday, tuesday, ... sunday, all)
    day = input("Please select a day to analyze: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday").lower()
    while day not in days :
        print("Please correctly enter the day you would like to analyze: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday")
        day = input("Please select a day to analyze: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday")
    print("You selected day: ", day)

    print('-'*40)
    return city, month, day
    """
    Did the user input prompts for city,month,day properly execute:
    """


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    # print(df)
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #in time_stats(df,city) will need 'day_of_week' , 'hour' columns in df.
    #Just add them to df now since df in arg
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
    # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']== month]


    # filter by day of week if applicable
    if day != 'all':
    # filter by day of week to create the new dataframe
        df = df[df['day_of_week']== day.title()]

    return df


def time_stats(df,city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    highest_freq_month_numeric = df['Start Time'].dt.month.mode()[0]
    highest_freq_month = months[highest_freq_month_numeric-1].title()
    print("The month with the highest frequency of rides is : " , highest_freq_month)

    # display the most common day of week
    highest_freq_day = df['day_of_week'].mode()[0]
    print('The highest frequency day is : ', highest_freq_day)

    # display the most common start hour
    highest_freq_start_hour = df['hour'].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df,city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    highest_freq_start_station= df['Start Station'].mode()[0]
    highest_freq_start_station_count = df['Start Station'].value_counts()[0]
    print('the highest frequency start station in {} is {} with a rental count of {}.'.format(city, highest_freq_start_station, highest_freq_start_station_count))

    # display most commonly used end station
    highest_freq_end_station = df['End Station'].mode()[0]
    highest_freq_end_station_count = df['End Station'].value_counts()[0]
    print('the highest frequency end station in {} is {} with a rental count of {}.'.format(city, highest_freq_end_station, highest_freq_end_station))

    # display most frequent combination of start station and end station trip
    high_freq_start_end_station_combo = df.loc[:, 'Start Station': 'End Station'].mode()[0:]
    high_freq_start_end_station_combo_count = df.groupby(['Start Station', 'End Station']).size().max()
    print('The most popular start,stop combination is {} this combination occurred {} \
        times.'.format(high_freq_start_end_station_combo,high_freq_start_end_station_combo_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df,city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('total travel time : ', total_duration)
    #display total travel time in hours, min, sec
    #total_duration is the seconds unit
    m,s = divmod(total_duration, 60)
    h,m = divmod(m,60)
    d, h = divmod(h, 24)
    print('total travel time in units: ',"d = ", d "h = ", h , "m = ", m , "s = ", s)

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('the mean travel time was about: ', mean_duration)
    # display mean travel time in hours, min, sec
    #mean_duration is the seconds unit
    m,s = divmod(mean_duration, 60)
    h,m = divmod(m,60)
    print('mean travel time in units: ',"h = ", h , "m = ", m , "s = ", s )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The count and type of users in', city, 'are :\n', df['User Type'].value_counts())

    # Display counts of gender - NOT available for washington
    if city in ['new york city', 'chicago']:
        print('The amount and gender of users in', city, 'are :\n',df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth - NOT available for washington
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()

    elif city == 'washington':
        print('Sorry neither gender nor birth year data is available for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,city)
        station_stats(df,city)
        trip_duration_stats(df,city)
        user_stats(df,city)

        five_rows = input('\n Would you like to see 5 lines of raw data? Enter yes or no.\n')
        x = 0
        while five_rows.lower() == 'yes':
            print(df.iloc[x:x+5])
            #ask user if want to see subsequent5 rows
            five_rows = input('\n Would you like to see the next 5 lines of raw data? Enter yes or no.\n')
            # increment x by 5
            x += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
