import pandas as pd
import matplotlib.pyplot as plt

# Data
data = {
    "Attribute": [
        "Confidentiality",
        "Authentication Strength",
        "Access Control Efficiency",
        "Key Management Security",
        "Audit & Activity Logging",
        "Data Integrity Assurance"
    ],
    "Existing System (%)": [62, 50, 55, 52, 48, 60],
    "Proposed System (%)": [90, 86, 88, 87, 85, 92]
}

df = pd.DataFrame(data)

# Create table image
fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('off')

table = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    cellLoc='center',
    loc='center'
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.6)

# Styling colors
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor("#BBDEFB")  # light blue header
        cell.set_text_props(weight='bold')
    else:
        cell.set_facecolor("#FCE4EC")  # light reddish-pink rows

plt.title("Table 5.1 Attribute Extraction Results", pad=20)
plt.savefig("Attribute_Extraction_Results_Table.png", dpi=300, bbox_inches='tight')
plt.show()


import matplotlib.pyplot as plt
import numpy as np

attributes = [
    "Confidentiality",
    "Authentication",
    "Access Control",
    "Key Management",
    "Audit Logging",
    "Data Integrity"
]

existing = [62, 50, 55, 52, 48, 60]
proposed = [90, 86, 88, 87, 85, 92]

x = np.arange(len(attributes))
width = 0.35

plt.figure(figsize=(9, 5))

plt.bar(x - width/2, existing, width,
        label="Existing System",
        color="#1E88E5")   # blue

plt.bar(x + width/2, proposed, width,
        label="Proposed System",
        color="#D81B60")   # reddish-pink

plt.xlabel("Performance Attributes")
plt.ylabel("Effectiveness (%)")
plt.title("Performance Metrics and Comparative Analysis")
plt.xticks(x, attributes, rotation=20)
plt.ylim(0, 100)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("Performance_Comparison_Bar_Graph.png", dpi=300)
plt.show()


import matplotlib.pyplot as plt
import numpy as np

attributes = [
    "Confidentiality",
    "Authentication",
    "Access Control",
    "Key Management",
    "Audit Logging",
    "Data Integrity"
]

existing = [62, 50, 55, 52, 48, 60]
proposed = [90, 86, 88, 87, 85, 92]

x = np.arange(len(attributes))

plt.figure(figsize=(9, 5))

plt.plot(x, existing, marker='o',
         linewidth=2,
         label="Existing System",
         color="#1565C0")  # blue

plt.plot(x, proposed, marker='o',
         linewidth=2,
         label="Proposed System",
         color="#C2185B")  # reddish-pink

plt.xlabel("Performance Attributes")
plt.ylabel("Effectiveness (%)")
plt.title("Performance Trend Analysis of Security Metrics")
plt.xticks(x, attributes, rotation=20)
plt.ylim(0, 100)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("Performance_Trend_Line_Graph.png", dpi=300)
plt.show()

