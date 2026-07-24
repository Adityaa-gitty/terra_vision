import pandas as pd
import sqlite3
import os

print("🔄 Reading 'final merged.xlsx' dataset...")
excel_path = 'final merged.xlsx'

if not os.path.exists(excel_path):
    print(f"❌ Error: '{excel_path}' file not found in the directory!")
else:
    # Read excel file safely
    xls = pd.ExcelFile(excel_path)
    print(f"📂 Available sheets in Excel: {xls.sheet_names}")
    
    df = pd.read_excel(excel_path, sheet_name=xls.sheet_names[0])
    
    # Connect to SQLite database
    conn = sqlite3.connect('trek_database.db')
    cursor = conn.cursor()
    
    # Drop old table to ensure clean schema with all columns matching Nitin & Sumit's dataset
    cursor.execute('DROP TABLE IF EXISTS trails_table')
    
    # Create table with correct schema including Temperature, Wind_Speed, etc.
    cursor.execute('''
        CREATE TABLE trails_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Trail_Name TEXT,
            Location TEXT,
            Distance REAL,
            Elevation_Gain INTEGER,
            Difficulty_Level TEXT,
            Temperature REAL,
            Wind_Speed REAL,
            Rainfall REAL,
            Average_Rating REAL,
            Estimated_Time REAL,
            AQI INTEGER,
            Air_Quality_Category TEXT,
            Tags TEXT,
            Image_Url TEXT,
            AllTrails_Link TEXT
        )
    ''')
    conn.commit()
    
    # Insert rows cleanly into SQLite database
    inserted_count = 0
    for index, row in df.iterrows():
        cursor.execute('''
            INSERT INTO trails_table (
                Trail_Name, Location, Distance, Elevation_Gain, Difficulty_Level,
                Temperature, Wind_Speed, Rainfall, Average_Rating, Estimated_Time,
                AQI, Air_Quality_Category, Tags, Image_Url, AllTrails_Link
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['trail_name'],
            row['location_city'],
            float(row['length_km']),
            int(row['elevation']),
            row['difficulty'],
            float(row['tavg']),
            float(row['wind_speed']),
            float(row['rainfall']),
            float(row['average_rating']),
            float(row['est_time']),
            int(row['AQI']),
            row['Air_Quality_Category'],
            str(row['tags']),
            str(row['image']),
            str(row['link_alltrails'])
        ))
        inserted_count += 1

    conn.commit()
    conn.close()
    print(f"✅ Success! {inserted_count} trail records successfully synced into 'trek_database.db' with all columns!")