import pandas as pd

filenames = ["Taipei-city", "NewTaipei-city", "Hsinchu-city", 
    "Hsinchu-county", "Taoyuan-city", "Taichung-city", "Changhua-county",
    "Tainan-city", "Kaohsiung-city"]
combined_csv = pd.concat( [ pd.read_csv("housePrice" + f + "/" +"housePrice" + f + ".csv", encoding="big5") for f in filenames ] )
combined_csv.to_csv( "combined_csv.csv", index=False )

print(combined_csv)