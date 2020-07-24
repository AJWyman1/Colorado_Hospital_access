import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def scatter_ctynames(df, x, y, s, county='CTYNAME', annotater='TOT_POP', min_pop=300000):
    fig, ax = plt.subplots(1, 1)
    ax.scatter(df[x], df[y], s=df[s],color='orange',alpha=.5)
    for i in range(len(df)):
        if df[annotater][i] < min_pop:
            ax.annotate(df[county][i], (df[x][i], df[y][i]), color='blue', fontsize=10)
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

def get_percents(df1, df2, col):
    # Input a collumn to get averages for counties with and without icu beds
    # Returns a list[average for counties without ICU beds, average for all of Colorado, average for counties with ICU beds]
    lst = []
    no_beds_col_tot = df1[col].sum()
    has_beds_col_tot = df2[col].sum()
    tot_pop = df1['TOT_POP'].sum() + df2['TOT_POP'].sum()
    lst.append(df2[col].sum()/df2['TOT_POP'].sum() * 100)
    lst.append((no_beds_col_tot + has_beds_col_tot)/tot_pop * 100)
    lst.append(df1[col].sum()/df1['TOT_POP'].sum()*100)
    return lst

def get_average(df1, df2, col):
    lst = []
    no_beds_col_avg = df1[col].sum()/df1[col].count()
    has_beds_col_avg = df2[col].sum()/df2[col].count()
    tot_avg = (df1[col].sum() + df2[col].sum())/(df2[col].count() + df1[col].count())
    lst.append(has_beds_col_avg)
    lst.append(tot_avg)
    lst.append(no_beds_col_avg)
    return lst

def bar_plot_and_save(label, x, y, color, path, percent=False):
    fig, ax = plt.subplots(1, 1)
    if percent:
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.bar([x[0],x[2]], [y[0],y[2]], color=color)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=12)
    plt.title(label=label, fontsize=20)
    # plt.hlines(y[1],-.5,1.5, linestyles='dashed', label=str(x[1]))
    ax.axhline(y[1],-.5,1.5, linestyle='--', label=str(x[1]), color='black')
    plt.legend(loc='lower left')
    plt.tight_layout()
    plt.savefig(path)
    plt.show()

def create_all_bar_charts(df1, df2, titles, save_as):
    perc_white = get_percents(df1, df2, 'White')
    perc_hisp = get_percents(df1, df2, 'Hispanic')
    perc_senior = get_percents(df1, df2, 'Senior')
    avg_gdp = get_average(df1, df2,'GDP Per capita')
    avg_med_hh_income = get_average(df1, df2, 'Median HH Income')
    avg_life_exp = get_average(df1, df2, 'Life _Exp')
    avg_icu_beds = get_average(df1, df2, 'icu_beds')

    cases_per_100k_df1 = (df1['COVID Cases'].sum()/(df1['TOT_POP'].sum()/100000))
    cases_per_100k_CO = (hisp_pop_df['COVID Cases'].sum()/(hisp_pop_df['TOT_POP'].sum()/100000))
    cases_per_100k_df2 = (df2['COVID Cases'].sum()/(df2['TOT_POP'].sum()/100000))
    cases_per_100k = [cases_per_100k_df2, cases_per_100k_CO, cases_per_100k_df1]


    # Make and save bar charts
    bar_plot_and_save('Average Number of ICU Beds', titles, avg_icu_beds, 'tab:orange', f'../img/avg_icu_beds_{save_as}.png')
    bar_plot_and_save('Average Life Expectancy', titles, avg_life_exp, 'tab:pink', f'../img/avg_life_exp_{save_as}.png')
    bar_plot_and_save('Average Median Household Income', titles, avg_med_hh_income, 'tab:brown', f'../img/med_avg_hh_income_{save_as}.png')
    bar_plot_and_save('Average GDP per capita', titles, avg_gdp, 'tab:olive', f'../img/avg_gdp_{save_as}.png')
    bar_plot_and_save('Percent Senior Population', titles, perc_senior, 'tab:cyan', f'../img/perc_senior_pop_{save_as}.png', percent=True)
    bar_plot_and_save('Percent Hispanic Population', titles, perc_hisp, 'tab:purple', f'../img/perc_hispanic_pop_{save_as}.png', percent=True)
    bar_plot_and_save('Percent White Population', titles, perc_white, 'tab:red', f'../img/perc_white_pop_{save_as}.png', percent=True)
    bar_plot_and_save('Cases of COVID-19 \nper 100,000', titles, cases_per_100k, 'tab:green', f'../img/covid_per_100k_{save_as}.png')
    pass

    '''
Questions to be investigated:
    What are some of the patterns of counties without hospitals? Counties with hospitals?
    What are some of the characteristics of counties with high senior populations and no hospitals

    IS there a correlation between life expectancy and hospital access?
    What can we say about counties with greatest cases of covid and hospital access
    What can we say about hospital access and demographics? Done
'''
if __name__ == '__main__':
    plt.style.use('ggplot')
    #save_census_year_df(2018, '../data/2018_census_est.csv')
    beds_df, wealth_and_health_df, hospital_loc, census_18_df = import_data()

    hospitals_joined = beds_df.join(hospital_loc.set_index('Hospital'), on='Hospital Name')
    hospitals_joined.rename({'ICU Beds – 2018 Medicare Cost Report (ICU beds filed on the 2018 report)': "icu_beds"}, axis="columns", inplace=True)

    countys = hospitals_joined.groupby(['county'])['Hospital Name'].count().reset_index()
    countys.rename({'Hospital Name': "tot_hosp"}, axis="columns", inplace=True)
    county_beds = hospitals_joined.groupby(['county'])['icu_beds'].sum().reset_index()

    health = wealth_and_health_df[['CTYNAME', 'COVID Cases', 'Life _Exp', 'Perc_Hispanic_Pop', 'GDP']].copy()

    health_hospitals = health.join(countys.set_index('county'), on='CTYNAME')
    beds_hospitals = health_hospitals.join(county_beds.set_index('county'), on='CTYNAME')


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
    


    hisp_pop_df = wealth_and_health_df[['CTYNAME', 'TOT_POP','COVID Cases', 'Life _Exp','Median HH Income', 'GDP','GDP Per capita', 'Perc_Hispanic_Pop','Hispanic', 'White']].copy()
    hisp_pop_df['Perc_White_Pop'] = hisp_pop_df['White'] / hisp_pop_df['TOT_POP']
 
    #hisp_pop_df['perc_of_whites'] = hisp_pop_df['White'] / hisp_pop_df['White'].sum()
    #hisp_pop_df['perc_of_his'] = hisp_pop_df['Hispanic'] / hisp_pop_df['Hispanic'].sum()
    hisp_pop_df = hisp_pop_df.join(county_beds.set_index('county'), on='CTYNAME')
    hisp_pop_df = hisp_pop_df.join(senior_pop.set_index('CTYNAME'), on='CTYNAME')
    #hisp_pop_df['perc_of_beds'] = hisp_pop_df['icu_beds'] / hisp_pop_df['icu_beds'].sum()
    hisp_pop_df.sort_values(by=['Life _Exp'], inplace=True, ascending=True)



    print((hisp_pop_df['Life _Exp'].sum())/(len(hisp_pop_df[hisp_pop_df['Life _Exp'].notnull()])))

    #print(hisp_pop_df.tail(20))
    low_avg_exp_mask = hisp_pop_df['Life _Exp'] < 80.77
    above_avg_exp_mask = hisp_pop_df['Life _Exp'] >= 80.77
    low_exp_df = hisp_pop_df[low_avg_exp_mask]
    above_avg_exp_df = hisp_pop_df[above_avg_exp_mask]
    
    life_exp_titles = ('Counties with above \naverage life expectancy','Colorado Average', 'Counties with below \naverage life expectancy')

    cases_per_100k_low_exp = (low_exp_df['COVID Cases'].sum()/(low_exp_df['TOT_POP'].sum()/100000))
    #print((cases_per_100k_low_exp-541.2)/(541.2))

    create_all_bar_charts(low_exp_df, above_avg_exp_df, life_exp_titles, 'by_life_exp')

    # print(hisp_pop_df.head(30), hisp_pop_df.tail(35))
    has_beds = hisp_pop_df['icu_beds'] > 0
    no_beds = hisp_pop_df['icu_beds'] == 0 
    na_beds = hisp_pop_df['icu_beds'].isna()
    county_has_beds = hisp_pop_df[has_beds]
    county_no_beds = hisp_pop_df[no_beds | na_beds]

    print(county_has_beds.count())
    print('--------------------------')
    print(county_no_beds.count())


    total = hisp_pop_df['TOT_POP'].sum()
    cases_per_100k_no_beds = (county_no_beds['COVID Cases'].sum()/(county_no_beds['TOT_POP'].sum()/100000))
    cases_per_100k_CO = (hisp_pop_df['COVID Cases'].sum()/(hisp_pop_df['TOT_POP'].sum()/100000))
    cases_per_100k_w_beds = (county_has_beds['COVID Cases'].sum()/(county_has_beds['TOT_POP'].sum()/100000))

    counties = ('Counties \nwith ICU beds','Colorado Average', 'Counties \nwithout ICU beds')
    cases_per_100k = [cases_per_100k_w_beds, cases_per_100k_CO, cases_per_100k_no_beds]
    print(cases_per_100k)
    perc_white = get_percents(county_no_beds, county_has_beds, 'White')
    perc_hisp = get_percents(county_no_beds ,county_has_beds, 'Hispanic')
    perc_senior = get_percents(county_no_beds ,county_has_beds, 'Senior')
    print(county_has_beds.describe())
    print(county_no_beds.describe())

    avg_gdp = get_average(county_no_beds, county_has_beds, 'GDP Per capita')
    avg_med_hh_income = get_average(county_no_beds, county_has_beds, 'Median HH Income')
    bar_plot_and_save('Average Median Household Income', counties, avg_med_hh_income, 'tab:brown', '../img/med_avg_hh_income.png')
    print(avg_gdp)
    avg_life_exp = get_average(county_no_beds, county_has_beds, 'Life _Exp')
    
    # bar_plot_and_save('Average Life Expectancy', counties, avg_life_exp, 'tab:pink', '../img/avg_life_exp.png')
    
    # # Make and save bar charts
    # bar_plot_and_save('Average GDP per capita', counties, avg_gdp, 'tab:olive', '../img/avg_gdp.png')
    # bar_plot_and_save('Percent Senior Population', counties, perc_senior, 'tab:cyan', '../img/perc_senior_pop_beds.png', percent=True)
    # bar_plot_and_save('Percent Hispanic Population', counties, perc_hisp, 'tab:purple', '../img/perc_hispanic_pop_beds.png', percent=True)
    # bar_plot_and_save('Percent White Population', counties, perc_white, 'tab:red', '../img/perc_white_pop_beds.png', percent=True)
    # bar_plot_and_save('Cases of COVID-19 \nper 100,000', counties, cases_per_100k, 'tab:green', '../img/covid_per_100k.png')
    
    print(low_exp_df.head(20))
    print(low_exp_df.tail(20))
    print(above_avg_exp_df.describe())
    print(low_exp_df.describe())
    