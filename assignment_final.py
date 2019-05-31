from bs4 import BeautifulSoup
import requests
import csv

def sum1(l):  # function for cummulative sum
    from itertools import accumulate
    return list(accumulate(l))

# creates the heading row
heading = [0] * 51
heading[0] = 'Player Name'
heading[1] = 'Nationality'
for i in range(49):
    heading[i + 2] = 1971 + i
# opens csv file
csv_file = open('assignment_final_final_final.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(heading)

source = requests.get('http://www.espncricinfo.com/ci/content/player/index.html').text
result = BeautifulSoup(source, 'lxml')
country_list = [None] * 17
content = result.find('ul', class_="subnav_tier1 subnav-item-wrap")
count = 0
for link in content.find_all('li'):
    link = link.a['href']
    if not link == '/':
        country_list[count] = link
        count += 1
country_list = set(country_list)  # finding list of links of each country's players and removing repetition
country_list = list(country_list)

for link in country_list:
    country_id = link.split('?')[1]
    source = requests.get(f'http://www.espncricinfo.com/ci/content/player/caps.html?{country_id};class=2').text
    result = BeautifulSoup(source, 'lxml')
    country_name = result.head.title.text.split('|')[0].split('Player')[0]  # finds country name
    content = result.find('div', class_='ciPlayerbycapstable')

    for content_link in content.find_all('li', class_='ciPlayername'):
        player_name = content_link.a.text  # finds player name
        content_link = content_link.a['href']
        player_id = content_link.split('/')[4]
        player_id = player_id.split('.')[0]
        player_link = f'http://stats.espncricinfo.com/ci/engine/player/{player_id}.html?class=2;filter=advanced;orderby=default;template=results;type=batting'
        source_details = requests.get(player_link).text
        result_details = BeautifulSoup(source_details, 'lxml')  # returns html code of player's career summary batting analysis

        head = result_details.find_all('table')[2].thead.tr
        span_check = (head.find_all('th')[1].text == 'Span')  # checks whether span heading is there or not

        result_details = result_details.find_all('table')[3]
        result_details = result_details.find_all('tbody')[4]
        a = [0] * 51  # creating an list of 51 elements each 0
        a[0] = player_name  # first element of row is assigned player name
        a[1] = country_name  # second element of row is assigned country name
        for row in result_details.find_all('tr')[1:]:  # leaving the first element of list (line break)

            try:
                year = int(row.find('td', class_='left', nowrap='nowrap').b.text.split(' ')[1])

                if span_check:
                    if row.find_all('td')[5].text == '-':  # dash for no runs scored in that year
                        runs_in_year = 0
                    else:
                        runs_in_year = int(row.find_all('td')[5].text)
                else:
                    if row.find_all('td')[4].text == '-':
                        runs_in_year = 0
                    else:
                        runs_in_year = int(row.find_all('td')[4].text)

                a[year - 1971 + 2] = runs_in_year  # enter the runs in corresponding year in the list

            except Exception as e:
                pass
        a = sum1(a[2:])  # calculating the cumulative runs excluding first element(player name)
        a.insert(0, player_name)
        a.insert(1, country_name)
        csv_writer.writerow(a)
    csv_writer.writerow([None] * 51)  # leaving an empty row at end of each country's list

csv_file.close()
