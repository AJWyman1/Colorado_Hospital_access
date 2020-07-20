import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def only_int(drf):
    pass

if __name__ == '__main__':
    beds_df = pd.read_excel('../data/co_hospital_beds.xlsx')
    wealth_and_health_df = pd.read_excel('../data/covid_cases.xlsx', sheet_name='Wealth and Health')
    hospital_loc = pd.read_csv('../data/hospital_location.csv')
    # census_df = pd.read_excel('../data/US_census_bureau_demographic.xlsx')
    #print (census_df.info())
    print(hospital_loc.info())
    # print(beds_df.info())
    wealth_and_health_df.drop([i for i in range(64, 70)], inplace=True)
    # print(wealth_and_health_df['COVID Cases'])
    wealth_and_health_df.astype({'COVID Cases': 'float64'}).dtypes
    # print(wealth_and_health_df.info())

    # age_covid = wealth_and_health_df[['COVID Cases', 'Life _Exp']].copy()
    # age_covid.sort_values(by='Life _Exp', inplace=True)
    # fig, ax = plt.subplots(1,1)
    # ax.scatter(wealth_and_health_df['COVID Cases'].select_dtypes(exclude=['str']), age_covid['Life _Exp'])
    # plt.show()
    #print(census_df.info())