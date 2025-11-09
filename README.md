# 🎓 Advanced Visualization and Storytelling (ADVST) 

## 📘 Project Title
### **1️⃣ Trends and Patterns of Fatalities in the Israel-Palestine Conflict (Power BI)**
### **2️⃣ Visualizing Preferential Attachment in Scale-Free Networks (Manim Animation)**

---

## 🧩 Overview

This project showcases advanced data visualization and storytelling techniques using **Power BI** and **Manim Animation**.

It is divided into two key parts:
- **Part 1 (Power BI Dashboard):**  
  An analytical visualization of fatalities in the **Gaza Strip** region, based on B’Tselem’s publicly available datasets.
- **Part 2 (Manim Animation):**  
  A visual demonstration of the **Preferential Attachment Model**, explaining how real-world networks evolve into **scale-free structures**.

---

## 🕵️ Part 1: Power BI Dashboard  
### 🎯 Objective  
To analyze trends, demographics, and patterns of fatalities in the **Israel-Palestine conflict**, focusing specifically on the **Gaza Strip**.

---

### 🧾 Dataset Information  

**Source:**  
[B’Tselem Fatalities Dataset](https://statistics.btselem.org/en/all-fatalities/by-date-of-incident?section=overall&tab=overview)

**Files Downloaded (Gaza Strip Only):**
1. `Israeli_civilians_killed_by_palestinians.xlsx`
2. `Israeli_forces_killed_by_palestinians.xlsx`
3. `Palestinians_killed_by_israeli_forces.xlsx`
4. `Palestinians_killed_by_israeli_civilians.xlsx`

**Reason for choosing Gaza Strip:**
- Central to recent wars and blockades.
- Maintains data consistency (different dynamics from West Bank).
- Smaller dataset improves **Power BI performance** and clarity.

---

### ⚙️ Data Preprocessing Steps

1. **Load Data:** Import all 4 Excel files into Power BI Query Editor.  
2. **Clean Data:**
   - Rename columns for consistency.
   - Change data types (dates, numbers, text).
   - Replace or handle missing values.
3. **Add a “Source” Column:** Identify which dataset each record belongs to.
4. **Merge Data:** Create a combined table `Main_table` using **Append Queries**.
5. **Apply Changes:** Click *Close & Apply* to load data into Power BI Desktop.

---

### 📊 Visualizations and Insights

#### 1️⃣ Fatality Trends Over Time
- **Type:** Line Chart  
- **Question:** How have fatalities changed over time for Palestinians and Israelis?  
- **Fields:** `Date of event`, `Source`, `Count of fatalities`  
- **Measure:**
  '''DAX'''
  Count_of_Fatalities = COUNTROWS('Main_table')

#### 2️⃣ Distribution by Age Groups
- **Type:** Bar Chart / Histogram
- **Question:** What is the age distribution of fatalities?
- **Fields:** Age, Count of fatalities
- **Measures:**
  '''DAX'''
  Palestinian_Fatalities = CALCULATE(
      COUNTROWS('Main_table'),
      'Main_table'[Source] IN {"Palestinians_killed_by_israeli_forces", "Palestinians_killed_by_israeli_civilians"}
  )

  Israeli_Fatalities = CALCULATE(
      COUNTROWS('Main_table'),
      'Main_table'[Source] IN {"Israeli_civilians_killed_by_palestinians", "Israeli_forces_killed_by_Palestinians"}
  )

#### 3️⃣ Geographical Spread of Fatalities
- **Type:** Map
- **Question:** Where did most fatalities occur?
- **Fields:** Event location, Event district, Count of fatalities

#### 4️⃣ Participation in Hostilities
- **Type:** Pie / Stacked Bar Chart
- **Question:** How many victims took part in hostilities?
- **Fields:** Took part in hostilities (Yes/No), Count of fatalities

#### 5️⃣ Gender Distribution of Fatalities
- **Type:** Pie Chart
- **Question:** What is the gender distribution?
- **Fields:** Gender, Count of fatalities

#### 6️⃣ Cause of Death (Type of Injury & Ammunition Used)
- **Type:** Stacked Bar Chart
- **Question:** What were the most common causes of death?
- **Fields:** Type of injury, Ammunition, Count of fatalities

#### 7️⃣ Responsible Party Analysis
- **Type:** Stacked Bar Chart
- **Question:** Who was responsible for fatalities?
- **Fields:** Killed_by, Source, Count of fatalities

#### 8️⃣ Fatalities by Event District
- **Type:** Scatter Plot
- **Question:** Were victims killed in their place of residence or elsewhere?
- **Fields:** Event district, Count of fatalities

#### 9️⃣ KPI (Key Performance Indicator)
- **Measure:**
'''DAX'''
Most_Affected_District =
VAR MaxDistrict = MAXX(
    TOPN(1, SUMMARIZE('Main_table', 'Main_table'[Event_District],
    "FatalityCount", COUNTROWS('Main_table')),
    [FatalityCount], DESC),
    'Main_table'[Event_District]
)
RETURN MaxDistrict

#### 🔟 Filter (Slicer)
- **Field:** Date Range (Event Date)
- Enables interactive filtering for specific time periods.

#### 🖼️ Dashboard Outcome
The dashboard provides:
  Yearly trends of fatalities.
  Demographic insights by gender and age.
  District-level spatial mapping.
  Hostility participation ratios.
  Type and cause of deaths.
  KPI for the most affected region.

## 🎬 Part 2: Manim Animation
### Visualizing Preferential Attachment in Scale-Free Networks

#### 🎯 Objective
To create a Manim animation illustrating how Preferential Attachment leads to Scale-Free Network formation.

#### 🧠 Conceptual Summary
- **Preferential Attachment:**
New nodes prefer to connect to already well-connected nodes.
→ “The rich get richer” phenomenon.

- **Scale-Free Networks:**
A few nodes (hubs) have many connections, while most have few.
Examples include:
  Social media networks (Twitter, Facebook)
  Citation networks
  Biological and neural networks

- **Degree Distribution:**
  Follows a Power Law. On a log-log plot, it appears as a straight line.

#### ⚙️ Environment Setup (Using Anaconda) 
'''bash'''
###### **Step 1:** Open Anaconda Prompt (Run as Administrator)
###### **Step 2:** Create a new environment
conda create -n manim-env python=3.10 -y
###### **Step 3:** Activate environment
conda activate manim-env
###### **Step 4:** Install Manim
conda install -c conda-forge manim
###### **Step 5:** Verify installation
manim --version
###### **Step 6:** Install FFmpeg for video rendering
conda install -c conda-forge ffmpeg
###### **Step 7:** Verify FFmpeg installation
ffmpeg -version

#### 🧾 Running the Animation
Save the animation code as PA2.py.
Run the following command:
'''bash'''
manim -pql PA2.py PreferentialAttachment
  PA2.py → Python file name
  PreferentialAttachment → Scene class name

#### 📈 Animation Flow
1) Introduction: Explanation of real-world examples (social networks, web links).
2) Seed Network Creation: A few initial nodes appear.
3) Node Addition: New nodes attach preferentially to higher-degree nodes.
4) Color Encoding: Nodes change color based on degree (connectivity).
5) Legend: Highlights meaning of node colors.
6) Degree Distribution Plot: Displayed in log-log scale, showing power-law behavior.
7) Conclusion: Animation ends with a summary and “Thank You” note.

#### 💡 Concept Summary
Preferential attachment explains how networks self-organize into scale-free structures.
A few nodes dominate connectivity — similar to how influencers dominate social media.
Degree distribution follows a power law, visible as a straight line on a log-log plot.

#### 📂 Repository Structure
ADVST_Assignment_01/
├── PowerBI/
│   ├── Israeli_civilians_killed_by_palestinians.xlsx
│   ├── Israeli_forces_killed_by_palestinians.xlsx
│   ├── Palestinians_killed_by_israeli_forces.xlsx
│   ├── Palestinians_killed_by_israeli_civilians.xlsx
│   └── PowerBI_Report.pbix
│
├── Manim/
│   ├── PA2.py
│   └── output_video.mp4
│
└── README.md

#### 🧑‍💻 Author Information
- **Name:** Anchal Gupta
- **Course:** Advanced Visualization and Storytelling (ADVST)
- **Institution:** Vidyashilp University, Bangalore 
- **Date:** November 2025

#### 🧾 References & Acknowledgments
- **Dataset:** B’Tselem – The Israeli Information Center for Human Rights in the Occupied Territories
- **Tools Used:** Power BI, Python (Manim), FFmpeg, Anaconda



