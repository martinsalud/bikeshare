import time
import pandas as pd

CITY_DATA: dict[str, str] = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}
MONTHS: list[str] = [
    "all",
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
]
DAYS_OF_WEEK: list[str] = [
    "all",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def get_filters() -> tuple[str, str, str]:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("Hello! Let's explore some US bikeshare data!")

    while True:
        # get input for city choice
        try:
            city_input: int = int(
                input(
                    "Which city's bikeshare data do you want to explore? \nType 1 for Chicago, 2 for New York City or 3 for Washington: "
                )
            )
            if city_input not in (1, 2, 3):
                print("Please enter a number from 1 to 3.")

            else:
                city: str = list(CITY_DATA.keys())[city_input - 1]
                print("You have chosen {}.".format(city.title()))
                break
        except ValueError:
            print("Please input a number.")

    while True:
        # get input for month choice
        try:
            month_input: int = int(
                input(
                    "Which month's bikeshare data do you want to explore? Write the number corresponding to the month (e.g. 1 = January, 2 = February) or 0 for all months: "
                )
            )
            if month_input == 0:
                month = MONTHS[month_input]
                print("You have chosen data for all months.")
                break
            elif month_input < 0 or month_input > 6:
                print("Please enter a number from 0 to 6.")
            else:
                month = MONTHS[month_input]
                print("You have chosen data for {}.".format(month.title()))
                break
        except ValueError:
            print("Please input a number.")

    while True:
        # get input for day choice
        try:
            day_input: int = int(
                input(
                    "Which day's bikeshare data do you want to explore? Write the corresponding number (e.g. 1 = Monday, 2 = Tuesday) or 0 for all days: "
                )
            )
            if day_input == 0:
                day = DAYS_OF_WEEK[day_input]
                print("You have chosen data for all days.")
                break
            elif day_input < 0 or day_input > 7:
                print("Please enter a number from 0 to 7. Try again.")
            else:
                day = DAYS_OF_WEEK[day_input]
                print("You have chosen data for {}.".format(day.title()))
                break
        except ValueError:
            print("Please input a number.")

    print("-" * 40)

    return city, month, day


def load_data(city: str, month: str, day: str) -> pd.DataFrame:
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
    df: pd.DataFrame = pd.read_csv(CITY_DATA[city])
    df.rename(columns={"Unnamed: 0": "User ID"}, inplace=True)

    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df["Month"] = df["Start Time"].dt.month
    df["Day of Week"] = df["Start Time"].dt.dayofweek

    # filter by month if applicable
    if month != "all":
        df = df[df["Month"] == MONTHS.index(month)]

    # filter by day of week if applicable
    if day != "all":
        df = df[df["Day of Week"] == DAYS_OF_WEEK.index(day)]

    return df


def time_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating the most frequent times of travel...\n")
    start_time: float = time.time()

    # display the most common month
    most_common_month: pd.Series[int] = df["Month"].value_counts()
    most_common_month_name: str = MONTHS[most_common_month.idxmax()]
    most_common_month_freq: int = most_common_month.max()
    print(
        f"The most common month is {most_common_month_name.title()} with {most_common_month_freq} validations."
    )

    # display the most common day of week
    most_common_day: pd.Series[int] = df["Day of Week"].value_counts()
    most_common_day_name: str = DAYS_OF_WEEK[most_common_day.idxmax()]
    most_common_day_freq: int = most_common_day.max()
    print(
        f"The most common day of the week is {most_common_day_name.title()} with {most_common_day_freq} validations."
    )

    # display the most common start hour
    df["Hour"] = df["Start Time"].dt.hour
    most_common_hour: pd.Series[int] = df["Hour"].value_counts()
    most_common_hour_freq: int = most_common_hour.max()
    print(
        f"The most common hour of the day is {most_common_hour.idxmax()} with {most_common_hour_freq} validations."
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating the most popular stations and trip...\n")
    start_time: float = time.time()

    # display most commonly used start station
    most_used_start_station: pd.Series[int] = df["Start Station"].value_counts()
    most_used_start_station_name: str = most_used_start_station.idxmax()
    most_used_start_station_freq: int = most_used_start_station.max()

    print(
        f"The most used start station is {most_used_start_station_name} with {most_used_start_station_freq} validations."
    )

    # display most commonly used end station
    most_used_end_station: pd.Series[int] = df["End Station"].value_counts()
    most_used_end_station_name: str = most_used_end_station.idxmax()
    most_used_end_station_freq: int = most_used_end_station.max()

    print(
        f"The most used end station is {most_used_end_station_name} with {most_used_end_station_freq} validations."
    )

    # display most frequent combination of start station and end station trip
    most_used_station_combination: pd.DataFrame = (
        df.groupby(["Start Station", "End Station"]).size().reset_index(name="Count")
    )
    most_used_station_combination = most_used_station_combination.sort_values(
        by="Count", ascending=False
    )
    most_used_station_combination = most_used_station_combination.iloc[0]
    most_used_station_combination_names: str = (
        most_used_station_combination["Start Station"]
        + " "
        + most_used_station_combination["End Station"]
    )
    most_used_station_combination_freq: int = most_used_station_combination["Count"]

    print(
        f"The most used station combination is {most_used_station_combination_names} with {most_used_station_combination_freq} validations."
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating trip duration...\n")
    start_time: float = time.time()

    # display total travel time
    total_travel_time: int = df["Trip Duration"].sum()
    print(f"Total travel time for this period is {total_travel_time} minutes.")

    # display mean travel time
    mean_travel_time: int = df["Trip Duration"].mean()
    print(f"Mean travel time for this period is {mean_travel_time} minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df: pd.DataFrame) -> None:
    """Displays statistics on bikeshare users."""

    print("\nCalculating user stats...\n")
    start_time: float = time.time()

    # display counts of user types
    user_type_count: pd.Series[int] = df["User Type"].value_counts()
    print(f"Statistics for each user type:\n{user_type_count}\n")

    # display counts of gender
    try:
        gender_count: pd.Series[int] = df["Gender"].value_counts()
        print(f"Statistics for each gender:\n{gender_count}\n")

    except KeyError:
        print("Statistics for gender not available for this dataset.")

    # display earliest, most recent, and most common year of birth
    try:
        earliest_yob: int = int(df["Birth Year"].min())
        most_recent_yob: int = int(df["Birth Year"].max())
        most_common_yob: int = int((df["Birth Year"].value_counts()).idxmax())
        print(
            f"The earliest year of birth is {earliest_yob}.\nThe most recent is {most_recent_yob}.\nThe most common is {most_common_yob}."
        )

    except KeyError:
        print("Statistics for year of birth not available for this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def individual_data(df: pd.DataFrame) -> None:
    """Displays individual data on bikeshare users in batches of 5."""
    print("\nCalculating user stats...\n")

    start: int = 0
    while start < len(df):

        # ask for user input
        try:
            individual_data_input: int = int(
                input("Do you want to see (more) individual data? Type '1' if yes. ")
            )

            if individual_data_input != 1:
                break

            start_time: float = time.time()
            end: int = start + 5

            print(df.iloc[start:end].to_json(orient="records", lines=True))
            print("This took %s seconds." % (time.time() - start_time))
            print("-" * 40)

            start += 5

        except ValueError:
            break


def main() -> None:
    while True:
        city, month, day = get_filters()
        df: pd.DataFrame = load_data(city, month, day)
        if df.empty == True:
            print("No data exist for the parameters chosen.")

        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            individual_data(df)

        restart: str = input(
            "\nWould you like to end it here? Type any key to end or '1' to restart.\n"
        )
        if restart != "1":
            break


if __name__ == "__main__":
    main()
