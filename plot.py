import matplotlib.pyplot as plt
import numpy as np

# Dữ liệu
labels = ['Accuracy', 'Miss Rate', 'Recall', 'F1-score']
values = [96.8, 2.8, 96.4, 96.8]

x = np.arange(len(labels))  # vị trí cột
width = 0.5

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(x, values, width, color='orange')

# Nhãn trục và tiêu đề
ax.set_ylabel('Percentage')
ax.set_title('Performance Metrics of SVM Classifier')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylim(0, 105)

# Hiển thị giá trị trên đầu cột
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # dịch lên 3px
                textcoords="offset points",
                ha='center', va='bottom')

plt.tight_layout()
plt.show()
