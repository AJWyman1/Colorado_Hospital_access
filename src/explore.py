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
    print(senior_pop)

    # beds_hospitals.sort_values(by=['Perc_Hispanic_Pop'], inplace=True, ascending=False)
    # fig, ax = plt.subplots(1, 1)
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


    hisp_pop_df = wealth_and_health_df[['CTYNAME', 'Perc_Hispanic_Pop','Hispanic']].copy()
    hisp_pop_df.sort_values(by=['Hispanic'], inplace=True, ascending=False)
    hisp_pop_df['perc_his_pop'] = hisp_pop_df['Hispanic'] / hisp_pop_df['Hispanic'].sum()
    hisp_pop_df = hisp_pop_df.join(county_beds.set_index('county'), on='CTYNAME')
    # print(hisp_pop_df.head(30), hisp_pop_df.tail(35))
    top_3 = hisp_pop_df.iloc[:4]
    top_3.drop(['CTYNAME'], axis=1, inplace=True)
    bottom = hisp_pop_df.iloc[4:]
    # print(top_3.sum())
    # print(bottom.sum())
    fig, ax = plt.subplots(1, 1)
    

