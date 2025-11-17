import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Paths
ROOT = os.path.dirname(os.path.dirname(__file__)) if __file__.endswith('generate_plots.py') else '.'
CSV_PATH = os.path.join(ROOT, 'president_heights.csv')
IMG_DIR = os.path.join(ROOT, 'images')
os.makedirs(IMG_DIR, exist_ok=True)

# Load data
data = pd.read_csv(CSV_PATH)
height_cm = np.array(data['height(cm)'])
height_inches = height_cm * 0.393701

# Styling
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

# 1) 2x2 panel: histogram, boxplot, violinplot, QQ-plot
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('The Height of Power: Visualizing Presidential Stature', fontsize=16, fontweight='bold', y=0.98)

# Histogram
axes[0, 0].hist(height_inches, bins=12, alpha=0.85, color='#2E86AB', edgecolor='white', linewidth=1.2)
axes[0, 0].axvline(height_inches.mean(), color='#A23B72', linestyle='--', linewidth=2,
                   label=f"Average: {int(height_inches.mean() // 12)}'{height_inches.mean() % 12:.1f}\"")
axes[0, 0].axvline(np.median(height_inches), color='#F18F01', linestyle='--', linewidth=2,
                   label=f"Median: {int(np.median(height_inches) // 12)}'{np.median(height_inches) % 12:.1f}\"")
axes[0, 0].set_title('The Presidential Height Bell Curve', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Height (inches)')
axes[0, 0].set_ylabel('Number of Presidents')
axes[0, 0].legend(fontsize=9)
axes[0, 0].grid(True, alpha=0.25)

# Boxplot
box_plot = axes[0, 1].boxplot(height_inches, patch_artist=True, widths=0.6)
box_plot['boxes'][0].set_facecolor('#2E86AB')
box_plot['boxes'][0].set_alpha(0.85)
axes[0, 1].set_title('Height Distribution: The Statistical View', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Height (inches)')
axes[0, 1].grid(True, alpha=0.25)

# Violinplot (matplotlib)
parts = axes[1, 0].violinplot(height_inches, showmeans=False, showmedians=True)
for pc in parts['bodies']:
        pc.set_facecolor('#A23B72')
        pc.set_edgecolor('black')
        pc.set_alpha(0.85)
axes[1, 0].set_title('Height Density: Where Presidents Cluster', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Height (inches)')
axes[1, 0].grid(True, alpha=0.25)

# QQ-plot (normality)
stats.probplot(height_inches, dist="norm", plot=axes[1, 1])
axes[1, 1].set_title('Normality Test: How Normal Are Presidential Heights?', fontsize=12, fontweight='bold')
axes[1, 1].grid(True, alpha=0.25)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
panel_path = os.path.join(IMG_DIR, 'height_panels.png')
fig.savefig(panel_path, dpi=150)
plt.close(fig)

# 2) Timeline scatter + trend
fig2, ax = plt.subplots(figsize=(14, 6))
order = data['order'] if 'order' in data.columns else np.arange(1, len(data) + 1)
ax.scatter(order, height_inches, alpha=0.85, s=110, c='#2E86AB', edgecolors='white', linewidth=1.5)
ax.plot(order, height_inches, alpha=0.6, color='#A23B72', linewidth=1.5)
z = np.polyfit(order, height_inches, 1)
p = np.poly1d(z)
ax.plot(order, p(order), '--', alpha=0.9, linewidth=2, color='#F18F01',
        label=f'Trend ({z[0]:.3f}" per president)')

# Average US male reference
us_male_avg_cm = 175.3
us_male_avg_inches = us_male_avg_cm * 0.393701
ax.axhline(y=us_male_avg_inches, color='red', linestyle=':', linewidth=2, alpha=0.8,
           label=f'Average US Male ({us_male_avg_inches:.1f}" )')

# Highlight extremes
tallest_idx = np.argmax(height_inches)
shortest_idx = np.argmin(height_inches)
ax.scatter(order.iloc[tallest_idx] if hasattr(order, 'iloc') else order[tallest_idx], height_inches[tallest_idx],
           color='#A23B72', s=220, marker='^', edgecolors='white', linewidth=2)
ax.scatter(order.iloc[shortest_idx] if hasattr(order, 'iloc') else order[shortest_idx], height_inches[shortest_idx],
           color='#2E86AB', s=220, marker='v', edgecolors='white', linewidth=2)

ax.set_title('The Evolution of Presidential Height: 1789 to Present', fontsize=14, fontweight='bold')
ax.set_xlabel('Presidential Order (1 = Washington)')
ax.set_ylabel('Height (inches)')
ax.grid(True, alpha=0.25)
ax.legend(fontsize=10)

plt.tight_layout()
timeline_path = os.path.join(IMG_DIR, 'timeline.png')
fig2.savefig(timeline_path, dpi=150)
plt.close(fig2)

print(f"Saved plots:\n - {panel_path}\n - {timeline_path}")
