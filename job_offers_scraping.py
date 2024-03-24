import requests as r
import bs4
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np


def input_iteration(n, prompt):
    answer_list = []
    for n in range(n):
        answer = input(prompt)
        answer_list.append(answer)
    return answer_list


def ask_for_length(prompt):
    n = int(input(prompt))
    return n


level_dict = {'Intern': '&et=1', 'Junior': '&et=17', 'Mid': '&et=4', 'Senior': '&et=18',
              'Manager': '&et=20', 'Director': '&et=6', 'Expert': '&et=19'}


nt = ask_for_length('How many technologies do you want to check? >')
nc = ask_for_length('In how many cities do you want to check offers? >')
nl = ask_for_length('How many job levels do you want to check? >')

tech = input_iteration(nt, 'Write technology to check >')
city = input_iteration(nc, 'Write city to check >')
print('Here are level options to choose:',' '.join([key for key in level_dict.keys()]))
level = input_iteration(nl, 'Write level to check >')

df = pd.DataFrame(columns=["technology", "city", "level", "offers"])

print('Wait for results to be imported...')

for k in range(nl):
    for j in range(nc):
        for i in range(nt):
            url_items = ['https://www.pracuj.pl/praca/', tech[i], ';kw/', city[j], ';wp?rd=30', level_dict[level[k]]]
            separator = ''
            url = separator.join(url_items)
            page = r.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            element = soup.find('span', class_="listing_jnf3car")
            if type(element) is not bs4.element.Tag:
                row = [tech[i], city[j], level[k], 0]
                df_length = len(df)
                df.loc[df_length] = row
            else:
                row = [tech[i], city[j], level[k], int(element.text.split(' ')[0])]
                df_length = len(df)
                df.loc[df_length] = row


plt.figure(figsize=(10, 6))

grouped_df = df.groupby(['technology', 'level']).sum().reset_index()
levels = grouped_df['level'].unique()

color_dict = {'Intern': 'purple', 'Junior': 'red', 'Mid': 'green', 'Senior': 'blue',
              'Manager': 'lime', 'Director': 'yellow', 'Expert': 'teal'}

bar_width = 0.2
index = np.arange(len(grouped_df['technology'].unique()))

for i, level in enumerate(levels):
    level_df = grouped_df[grouped_df['level'] == level]
    bars = plt.bar(index + i * bar_width, level_df['offers'], color=color_dict[level], width=bar_width, label=level)

    # Adding data labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, '%d' % int(height), ha='center', va='bottom')

plt.xlabel('Technology')
plt.ylabel('Total Offers')
plt.title('Sum of Offers by Technology and Level')
plt.xticks(index + bar_width, grouped_df['technology'].unique())
plt.legend(title='Level')
plt.show()