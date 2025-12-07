import datetime
import random

# lists containing month numbers
list_month_31 = {1, 3, 5, 7, 8, 10, 12}
list_month_30 = {4, 6, 9, 11}
list_month_28_29 = {2}

# Function draws city and area code from input list
def select_polish_city(provincial_cities_list,excluded_cities_list):
    city_selected = False
    i = 0
    while not city_selected:
        i = random.randint(0, len(provincial_cities_list) - 1)
        city_selected_name = provincial_cities_list[i][:provincial_cities_list[i].find("|")]

        if city_selected_name not in excluded_cities_list:
            city_selected = True
    return provincial_cities_list[i]


# Function drawing number of months
def draw_number_of_months():
    number_months = random.randint(1, 12)
    return number_months


# Function adding number of months to current month and returs number of future month
def calculate_target_month(n_months):
    current_dt = datetime.datetime.now()
    current_mth = current_dt.month
    calc_mth = (current_mth + n_months) % 12
    if calc_mth == 0:
        calc_mth = 12
    return calc_mth


# Function calculating future year
def calculate_target_year(n_months):
    current_dt = datetime.datetime.now()
    current_mth = current_dt.month
    current_year = current_dt.year
    if current_mth + n_months > 12:
        current_year = current_year + 1
    return current_year


# Function calculating last Saturday in month
def calculate_last_saturday_date(tg_month, tg_year):
    if tg_month in list_month_31:
        month_days = 31
    elif tg_month in list_month_30:
        month_days = 30
    elif tg_month in list_month_28_29 and tg_year % 4 == 0:
        month_days = 29
    else:
        month_days = 28

    saturday_found = False
    while saturday_found == False:
        dt = datetime.datetime(tg_year, tg_month, month_days)
        if dt.weekday() == 5:
            saturday_found = True
        else:
            month_days = month_days - 1

    return month_days


# Reading external file big-cities.txt containing list of Polish big cities
bigcities = open("/Users/arkadiuszgalas/Documents/python/eighteencities/available/provincial-cities.txt", encoding="utf8")
data = bigcities.read()
bigcities_list = data.split("\n")
bigcities.close()

# Reading external file special-city.txt containing name of special (last) city
special_city = open("/Users/arkadiuszgalas/Documents/python/eighteencities/available/special-city.txt")
data_special = special_city.read()
data_special_list = data_special.split("\n")
special_city.close()

# Reading length bigcities_list list
len_bigcities = len(bigcities_list)

# Reading external file restricted-cities.txt with list of cities excluded from drawing
restricted_cities = open("/Users/arkadiuszgalas/Documents/python/eighteencities/restricted/restricted-cities.txt")
data_restricted = restricted_cities.read()
restricted_cities_list = data_restricted.split("\n")
restricted_cities.close()

# Reading length of restricted_cities_list list
len_restricted_cities = len(restricted_cities_list) - 1

# Decision logic what file to select city
city_sel_name = ''
area_sel_name = ''
if len_bigcities > len_restricted_cities:
    bigcity_selected = select_polish_city(bigcities_list, restricted_cities_list)
    city_sel_name = bigcity_selected[0:bigcity_selected.find("|")]
    area_sel_name = bigcity_selected[bigcity_selected.find("|") + 1:len(bigcity_selected)]
elif len_bigcities == len_restricted_cities:
    bigcity_selected = select_polish_city(data_special_list, restricted_cities_list)
    city_sel_name = bigcity_selected[0:bigcity_selected.find("|")]
    area_sel_name = bigcity_selected[bigcity_selected.find("|") + 1:len(bigcity_selected)]

# Calculating last Saturday in the month
month_shift = draw_number_of_months()
month_selected = calculate_target_month(month_shift)
year_selected = calculate_target_year(month_shift)
last_day_selected = calculate_last_saturday_date(month_selected, year_selected)

# Writing information about selected city to selected-cities.txt
current_dttm = datetime.datetime.now()
current_dttm_fm = current_dttm.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
date_selected = datetime.datetime(year_selected, month_selected, last_day_selected)

# Decision logic what information save in selected-cities.txt and in restricted-cities.txt
if len_bigcities >= len_restricted_cities:
    cities_selected = open("/Users/arkadiuszgalas/Documents/python/eighteencities/selected/selected-cities.txt", "a")
    cities_selected.write(
        current_dttm_fm + str(" ") + date_selected.strftime("%d.%m.%Y") + str(" ") + str(city_sel_name) + str(
            " ") + str(area_sel_name) + "\n")
    cities_selected.close()

    # Writing information about selected city to restricted-cities.txt
    cities_restricted = open("/Users/arkadiuszgalas/Documents/python/eighteencities/restricted/restricted-cities.txt", "a")
    cities_restricted.write(str(city_sel_name) + "\n")
    cities_restricted.close()
else:
    cities_selected = open("/Users/arkadiuszgalas/Documents/python/eighteencities/selected/selected-cities.txt", "a")
    cities_selected.write(
        current_dttm_fm + str(" ") + str("No more cities on the list. I hope you had a great time." + "\n"))
    cities_selected.close()
    print("No more cities on the list. I hope you had a great time.")
