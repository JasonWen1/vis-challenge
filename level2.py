# coding:utf-8
from level1_data import *
import matplotlib.pyplot as plt

# Level 2 data
max_total_data = np.zeros(shape=(len(years), len(months), 31))
min_total_data = np.zeros(shape=(len(years), len(months), 31))
for _index, _row in temp_data.iterrows():
    _year, _month, _day = _row.get('year'), _row.get('month'), _row.get('day')
    max_total_data[_year - min(years), _month - min(months), _day - 1] = _row.get('max_temp')
    min_total_data[_year - min(years), _month - min(months), _day - 1] = _row.get('min_temp')

fig = plt.figure()
x_gap = 0.05
y_gap = 0.05
height = 0.2
width = 0.2
cmap = plt.get_cmap('YlOrRd')

axs_bg = fig.add_axes([0, 0, (width + x_gap) * len(months), (height + y_gap) * len(years)])
axs_bg.spines['top'].set_visible(False)
axs_bg.spines['right'].set_visible(False)
axs_bg.set_xlabel('Month')
axs_bg.set_ylabel('Year')

common_x = list(range(1, 32))
for _year in years:
    for _month in months:
        axs_unit = fig.add_axes(
            [x_gap+(_month-min(months))*(width+x_gap), y_gap+(_year-min(years))*(height+y_gap), height, width]
        )
        axs_unit.axis(xmin=1, xmax=31, ymin=0, ymax=40)
        axs_unit.set_xticks([])
        axs_unit.set_yticks([])
        axs_unit.spines.clear()

        axs_unit.set_facecolor(cmap(6 * max_temp[_month - min(months), _year - min(years)]))

        axs_unit.plot(
            common_x, max_total_data[_year-min(years), _month-min(months)], '#2E8B57',
            common_x, min_total_data[_year-min(years), _month-min(months)], '#A9A9A9',
        )

xticks = (np.array(months) - min(months)) * (width + x_gap) + x_gap + width / 2
yticks = (np.array(years) - min(years)) * (height + y_gap) + y_gap + height / 2

axs_bg.set_xticks([0] + xticks.tolist() + [(width+x_gap)*len(months)])
axs_bg.set_yticks([0] + yticks.tolist() + [(height+y_gap)*len(years)])

axs_bg.set_xticklabels([''] + months.to_list() + [''])
axs_bg.set_yticklabels([''] + years.to_list() + [''])


plt.savefig(fname='level2.svg', format='svg', bbox_inches='tight')
plt.savefig(fname='level2.png', format='png', bbox_inches='tight')