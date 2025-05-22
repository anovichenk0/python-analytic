import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path

path = Path(__file__).parent / 'data' / 'company_sales_data.csv'
data = pd.read_csv(path)

plt.figure()
plt.plot(data['month_number'], data['total_profit'], color='blue', linewidth=2)
plt.xlabel("Month number")
plt.ylabel("Profit in dollar")
plt.title("Company profit per month")
plt.ylim([100000, 500000])
plt.grid(True)
plt.savefig("task1.png")
plt.show()

plt.figure()
plt.plot(
    data['month_number'],
    data['total_units'],
    color='red',
    linestyle='--',
    linewidth=3,
    marker='o',
    markerfacecolor='black',
    label='Profit data of last year'
)
plt.xlabel("Month Number")
plt.ylabel("Units Sold")
plt.title("Company Sales data of last year")
plt.legend(loc='lower right')
plt.grid(True)
plt.savefig("task2.png")
plt.show()

plt.figure()
plt.plot(data['month_number'], data['facecream'], label='Face cream Sales Data', marker='o')
plt.plot(data['month_number'], data['facewash'], label='Face Wash Sales Data', marker='o')
plt.plot(data['month_number'], data['toothpaste'], label='ToothPaste Sales Data', marker='o')
plt.plot(data['month_number'], data['bathingsoap'], label='Bathingsoap Sales Data', marker='o')
plt.plot(data['month_number'], data['shampoo'], label='Shampoo Sales Data', marker='o')
plt.plot(data['month_number'], data['moisturizer'], label='Moisturizer Sales Data', marker='o')
plt.xlabel("Month Number")
plt.ylabel("Sales units in number")
plt.title("Sales data")
plt.legend()
plt.grid(True)
plt.savefig("task3_1.png")
plt.show()

fig = plt.figure()
plt.plot(data['month_number'], data['bathingsoap'], color='black', marker='o')
plt.title("Sales data of a Bathingsoap")
plt.xlabel("Month Number")
plt.ylabel("Sales units in number")
plt.grid(True)
fig.savefig("task3_2_bathingsoap.png")


fig = plt.figure()
plt.plot(data['month_number'], data['facewash'], color='red', marker='o')
plt.title("Sales data of a facewash")
plt.xlabel("Month Number")
plt.ylabel("Sales units in number")
plt.grid(True)
fig.savefig("task3_2_facewash.png")
plt.show()

plt.figure()
plt.scatter(data['month_number'], data['toothpaste'], label='Tooth paste Sales data', color='blue')
plt.xlabel("Month Number")
plt.ylabel("Number of units Sold")
plt.title("Tooth paste Sales data")
plt.grid(True, linestyle='--')
plt.legend()
plt.savefig("task4.png")
plt.show()


plt.figure()
bar_width = 0.4
months = data['month_number']
x_indexes = np.arange(len(months))

plt.bar(x_indexes - bar_width/2, data['facecream'], width=bar_width, label='Face Cream sales data', color='blue')
plt.bar(x_indexes + bar_width/2, data['facewash'], width=bar_width, label='Face Wash sales data', color='orange')

plt.xlabel("Month Number")
plt.ylabel("Sales units in number")
plt.title("Facewash and facecream sales data")
plt.xticks(ticks=x_indexes, labels=months)
plt.legend()
plt.grid(True, axis='y', linestyle='--')
plt.savefig("task5.png")
plt.show()


plt.figure()

product_labels = ['FaceCream', 'FaseWash', 'ToothPaste', 'Bathing soap', 'Shampoo', 'Moisturizer']
product_columns = ['facecream', 'facewash', 'toothpaste', 'bathingsoap', 'shampoo', 'moisturizer']
product_totals = [data[col].sum() for col in product_columns]

plt.pie(product_totals, labels=product_labels, autopct='%1.1f%%', startangle=90)
plt.title("SALES DATA")
plt.axis('equal') 
plt.legend(product_labels, loc='lower right')
plt.savefig("task6.png")
plt.show()

plt.figure()

months = data['month_number']
labels = ["face Cream", "Face wash", "Tooth paste", "Bathing soap", "Shampoo", "Moisturizer"]
colors = ['magenta', 'cyan', 'red', 'black', 'green', 'yellow']
stack_data = [data['facecream'], data['facewash'], data['toothpaste'],
              data['bathingsoap'], data['shampoo'], data['moisturizer']]

plt.stackplot(months, *stack_data, labels=labels, colors=colors)
plt.xlabel("Month Number")
plt.ylabel("Sales units in Number")
plt.title("Alll product sales data using stack plot")
plt.legend(loc='upper left')
plt.savefig("task7.png")
plt.show()

import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(16, 16))
gs = gridspec.GridSpec(4, 2, figure=fig)

for i in range(4):
    for j in range(2):
        ax = fig.add_subplot(gs[i, j])
        ax.set_title(f"{i * 2 + j + 1}")
        ax.axis('on')

fig.suptitle("Заготовочка", fontsize=22)
plt.tight_layout()
plt.savefig("task8.png")
plt.show()
