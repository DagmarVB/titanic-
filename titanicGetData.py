import pandas as pd

def getData(gender, age1, age2, age3, age4, ageU, classvar):

    """
    Input: variables holding the passenger specifications as selected by the user in the tkinter GUI.
    Functionality: filters the "titanicDataset" file according to the specifications, writes the filtered data into a new file.
    Output: filtered dataset in a pandas dataframe, number of survivors, number of fatalities.
    """

    # write the selected passenger specifications into lists using the wording of the file column entries
    gender = ["female", "male"] if gender == "all" else [gender]
    age = []
    if age1 == 1: age.append("<16")
    if age2 == 1: age.append("16-35")
    if age3 == 1: age.append("36-55")
    if age4 == 1: age.append(">55")
    if ageU == 1: age.append("U")
    classvar = [1, 2, 3] if classvar == "all" else [int(classvar)]

    # for testing and better control, print specifications:
    print(f"Gender:  {gender}\nAge:     {age}\nClass:   {classvar}\n")

    # read data from file "Dataset.csv" and filter according to specifications:
    data = pd.read_csv("titanicDataset.csv", delimiter = ";")
    filtered = data[(data["Sex"].isin(gender)) &
                    (data["AgeCat"].isin(age)) &
                    (data["Pclass"].isin(classvar))]

    # write filtered data into a new file:
    filtered.to_csv("titanicDatasetFiltered.csv")

    # count survivors and fatalities in filtered data
    survivors = len(filtered[filtered["Survived"]==1])
    fatalities = len(filtered[filtered["Survived"]==0])

    # return filtered dataset, number of survivors and number of fatalities
    return filtered, survivors, fatalities

# for testing and during development, call function getData directly:
#getData("all",1,1,1,1,1,"all") # all data
#getData("female",1,0,0,0,0,"3") # female, underage and unknown age, 3rd class