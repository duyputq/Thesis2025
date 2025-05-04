import matplotlib.pyplot as plt

# Danh sách các thuật toán còn lại
methods = ['AMLSDM-SVM', 'AMLSDM-NB', 'AMLSDM-LR', 'AMLSDM-RF']
# score tương ứng (đọc từ biểu đồ tại Number of Test Flows = 10000)
score = [0.904, 0.904, 0.911, 0.918]

# Vẽ biểu đồ
plt.figure(figsize=(8, 5))
bar_width = 0.4  # Giảm độ rộng của các cột
bars = plt.bar(methods, score, color='skyblue', edgecolor='black', width=bar_width)

# Thêm nhãn score trên mỗi cột
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.002, f'{yval:.3f}', ha='center', va='bottom')

# Cấu hình đồ thị
plt.title('score of ML Methods at 10000 Test Flows ', fontsize=12)
plt.xlabel('ML Method')
plt.ylabel('F1-score')
plt.ylim(0, 1)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
