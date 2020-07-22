import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def scatter_ctynames(x, y, min_pop=300000):
    fig, ax = plt.subplots(1, 1)
    ax.scatter(wealth_and_health_df[x], wealth_and_health_df[y])
    for i in range(len(wealth_and_health_df)):
        if wealth_and_health_df['TOT_POP'][i] > min_pop:
            ax.annotate(wealth_and_health_df['CTYNAME'][i], (wealth_and_health_df[x][i], wealth_and_health_df[y][i]))
    ax.set_ylabel(y)
    ax.set_xlabel(x)
    plt.show()


def import_data():
    '''
        Load
    '''
    beds_df = pd.read_excel('../data/co_hospital_beds.xlsx')
    hospital_loc = pd.read_csv('../data/hospital_location.csv')
    wealth_and_health_df = pd.read_excel('../data/covid_cases.xlsx', sheet_name='Wealth and Health')
    census_18_df = pd.read_csv('../data/2018_census_est.csv')
    '''
        Clean up
    '''
    wealth_and_health_df.drop([i for i in range(64, 70)], inplace=True)
    hospital_loc.rename({"Unnamed: 0": "a"}, axis="columns", inplace=True)
    hospital_loc.drop(['a'], axis=1, inplace=True)
    wealth_and_health_df['COVID Cases'] = wealth_and_health_df['COVID Cases'].astype(int)
    wealth_and_health_df['CTYNAME'] = wealth_and_health_df['CTYNAME'].str.strip()

    return beds_df, wealth_and_health_df, hospital_loc, census_18_df


def save_census_year_df(year, path):
    '''
        inputs - year from 2010 - 2018
               - path to save csv
    '''
    census_df = pd.read_excel('../data/US_census_bureau_demographic.xlsx')
    year_num = year - 2007
    year_mask = census_df['YEAR'] == year_num
    census_year_df = census_df[year_mask]
    census_year_df.to_csv(path)

def get_percents(col):
    lst = []
    no_beds_col_tot = county_no_beds[col].sum()
    has_beds_col_tot = county_has_beds[col].sum()
    tot_pop = county_no_beds['TOT_POP'].sum() + county_has_beds['TOT_POP'].sum()
    lst.append(county_no_beds[col].sum()/county_no_beds['TOT_POP'].sum())
    lst.append((no_beds_col_tot + has_beds_col_tot)/tot_pop)
    lst.append(county_has_beds[col].sum()/county_has_beds['TOT_POP'].sum())
    return lst

def bar_plot_and_save(label, x, y, color):
    fig, ax = plt.subplots(1, 1)
    ax.bar(x, y, color=color)
    plt.xticks(fontsize=10)
    plt.title(label=label, fontsize=20)
    plt.show()

'''
Questions to be investigated:
    What are some of the patterns of counties without hospitals? Counties with hospitals?
    What are some of the characteristics of counties with high senior populations and no hospitals

    IS there a correlation between life expectancy and hospital access?
    What can we say about counties with greatest cases of covid and hospital access
    What can we say about hospital access and demographics?
'''
if __name__ == '__main__':
    plt.style.use('ggplot')
    #save_census_year_df(2018, '../data/2018_census_est.csv')
    beds_df, wealth_and_health_df, hospital_loc, census_18_df = import_data()

    



    # print(census_18_df.info())
    # print(wealth_and_health_df.info())
    # print(wealth_and_health_df.head())
    # print(wealth_and_health_df['COVID Cases'])
    # print(beds_df.info())
    # print(hospital_loc.info())
    hospitals_joined = beds_df.join(hospital_loc.set_index('Hospital'), on='Hospital Name')
    hospitals_joined.rename({'ICU Beds – 2018 Medicare Cost Report (ICU beds filed on the 2018 report)': "icu_beds"}, axis="columns", inplace=True)
    # print(hospitals_joined.info())
    # print(hospitals_joined.head())
    # print(hospitals_joined['county'].unique())

    countys = hospitals_joined.groupby(['county'])['Hospital Name'].count().reset_index()
    countys.rename({'Hospital Name': "tot_hosp"}, axis="columns", inplace=True)
    county_beds = hospitals_joined.groupby(['county'])['icu_beds'].sum().reset_index()
    # print(countys)
    # print(county_hospitals.head())
    health = wealth_and_health_df[['CTYNAME', 'COVID Cases', 'Life _Exp', 'Perc_Hispanic_Pop', 'GDP']].copy()

    # print(health)
    # print(health['CTYNAME'])
    health_hospitals = health.join(countys.set_index('county'), on='CTYNAME')
    # print(health_hospitals.head())
    beds_hospitals = health_hospitals.join(county_beds.set_index('county'), on='CTYNAME')
    # print(beds_hospitals.head())
    # health_beds = beds_hospitals.join(health_hospitals.set_index('county'))
    # print(health.head())
    # print(countys['county'])

    senior_mask = census_18_df['AGEGRP'] >= 14

    senior_citizen_df = census_18_df[senior_mask]

    senior_citizen_df['CTYNAME'] = senior_citizen_df['CTYNAME'].str.replace(' County', '').copy()

    senior_citizen_county = senior_citizen_df.groupby(['CTYNAME']).sum().reset_index()
    senior_citizen_county.sort_values(by=['TOT_POP'], inplace=True, ascending=False)
    senior_pop = senior_citizen_county[['CTYNAME', 'TOT_POP']]
    senior_pop['perc_senior'] = senior_pop['TOT_POP'] / senior_pop['TOT_POP'].sum()
    senior_pop.rename({"TOT_POP": "Senior"}, axis="columns", inplace=True)
    # print(senior_pop)

    # beds_hospitals.sort_values(by=['Perc_Hispanic_Pop'], inplace=True, ascending=False)
    fig, ax = plt.subplots(1, 1)
    # ax.set_title('Number of Hospitals and Percent Hispanic Population')
    # ax.bar(beds_hospitals['CTYNAME'], beds_hospitals['Perc_Hispanic_Pop'], color='blue')
    # ax.set_ylabel("Percent Hispanic Population", color='blue', fontsize=16)
    # plt.xticks(rotation='vertical')
    # ax2 = ax.twinx()

    # ax2.bar(beds_hospitals['CTYNAME'], beds_hospitals['icu_beds'], color='red',alpha=.5)
    # ax2.set_ylabel("Number of ICU Beds", fontsize=16, color='red')

    # plt.xticks(rotation='vertical')

    # plt.tight_layout()
    # plt.show()
    
    # print(census_df.info())
    # print(senior_citizen_county.head())
    # print(senior_citizen_df.info())


    hisp_pop_df = wealth_and_health_df[['CTYNAME', 'TOT_POP','COVID Cases', 'GDP', 'Perc_Hispanic_Pop','Hispanic', 'White']].copy()
    hisp_pop_df['Perc_White_Pop'] = hisp_pop_df['White'] / hisp_pop_df['TOT_POP']
 
    hisp_pop_df['perc_of_whites'] = hisp_pop_df['White'] / hisp_pop_df['White'].sum()
    hisp_pop_df['perc_of_his'] = hisp_pop_df['Hispanic'] / hisp_pop_df['Hispanic'].sum()
    hisp_pop_df = hisp_pop_df.join(county_beds.set_index('county'), on='CTYNAME')
    hisp_pop_df = hisp_pop_df.join(senior_pop.set_index('CTYNAME'), on='CTYNAME')
    hisp_pop_df['perc_of_beds'] = hisp_pop_df['icu_beds'] / hisp_pop_df['icu_beds'].sum()
    hisp_pop_df.sort_values(by=['perc_of_beds'], inplace=True, ascending=False)
    # print(hisp_pop_df.head(30), hisp_pop_df.tail(35))
    has_beds = hisp_pop_df['icu_beds'] > 0
    no_beds = hisp_pop_df['icu_beds'] == 0 
    na_beds = hisp_pop_df['icu_beds'].isna()
    county_has_beds = hisp_pop_df[has_beds]
    county_no_beds = hisp_pop_df[no_beds | na_beds]

    print(county_has_beds.sum())
    # print('--------------------------')
    print(county_no_beds.sum())


    total = hisp_pop_df['TOT_POP'].sum()
    cases_per_100k_no_beds = (county_no_beds['COVID Cases'].sum()/(county_no_beds['TOT_POP'].sum()/100000))
    cases_per_100k_CO = (hisp_pop_df['COVID Cases'].sum()/(hisp_pop_df['TOT_POP'].sum()/100000))
    cases_per_100k_w_beds = (county_has_beds['COVID Cases'].sum()/(county_has_beds['TOT_POP'].sum()/100000))

    counties = ('Counties \nwith ICU beds','Colorado Average', 'Counties \nwithout ICU beds')
    cases_per_100k = [cases_per_100k_w_beds, cases_per_100k_CO, cases_per_100k_no_beds]

    perc_white = get_percents('White')
    perc_hisp = get_percents('Hispanic')
    perc_senior = get_percents('Senior')

    # bar_plot_and_save('Percent Senior Population', counties, perc_senior, 'tab:cyan')
    bar_plot_and_save('Percent Hispanic Population', counties, perc_hisp, 'tab:purple')
    bar_plot_and_save('Percent White Population', counties, perc_white, 'tab:red')
    bar_plot_and_save('Cases of COVID-19 \nper 100,000', counties, cases_per_100k, 'tab:green')
