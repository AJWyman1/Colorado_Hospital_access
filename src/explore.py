import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def only_int(df):
    pass

def scatter_ctynames(x, y, min_pop = 300000):
    ax.scatter(wealth_and_health_df[x], wealth_and_health_df[y] )
    for i in range(len(wealth_and_health_df)):
        if age_covid['TOT_POP'][i] > min_pop:
            ax.annotate(wealth_and_health_df['CTYNAME'][i], (wealth_and_health_df[x][i], wealth_and_health_df[y][i]))
    plt.show()

def import_data(census = False):
    beds_df = pd.read_excel('../data/co_hospital_beds.xlsx')
    wealth_and_health_df = pd.read_excel('../data/covid_cases.xlsx', sheet_name='Wealth and Health')
    wealth_and_health_df.drop([i for i in range(64, 70)], inplace=True)
    hospital_loc = pd.read_csv('../data/hospital_location.csv')
    hospital_loc.rename({"Unnamed: 0":"a"}, axis="columns", inplace=True)
    hospital_loc.drop(['a'], axis=1, inplace=True)
    if census:
        census_df = pd.read_excel('../data/US_census_bureau_demographic.xlsx')
        return beds_df, wealth_and_health_df, hospital_loc, census_df
    else:
        return beds_df, wealth_and_health_df, hospital_loc


if __name__ == '__main__':
    beds_df, wealth_and_health_df, hospital_loc = import_data()

    
    # print(hospital_loc.info())
    # print(beds_df.info())

    # print(beds_df.info())
    
    # print(wealth_and_health_df['COVID Cases'])
    wealth_and_health_df['COVID Cases'] = wealth_and_health_df['COVID Cases'].astype(str).astype(int)
    print(wealth_and_health_df.head())
    # print(wealth_and_health_df['COVID Cases'])
    age_covid = wealth_and_health_df[['COVID Cases', 'Life _Exp', 'Hispanic', 'TOT_POP', 'CTYNAME', 'Perc_Hispanic_Pop']].copy()
    age_covid.sort_values(by='COVID Cases', inplace=True)
    print(age_covid)
    fig, ax = plt.subplots(1,1)
    #ax.scatter(age_covid['Hispanic'], age_covid['COVID Cases'] )
    # ax.scatter(age_covid['TOT_POP'], age_covid['COVID Cases'] )
    # for i in range(len(age_covid)):

    #     if age_covid['TOT_POP'][i] > 300000:
    #         ax.annotate(age_covid['CTYNAME'][i], (age_covid['TOT_POP'][i], age_covid['COVID Cases'][i]))
    # plt.show()
    scatter_ctynames('GDP Per capita' , 'Life _Exp')
    # print(census_df.info())