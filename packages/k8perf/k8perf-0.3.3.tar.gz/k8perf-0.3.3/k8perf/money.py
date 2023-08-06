import pandas as pd

def main():
    df = pd.read_csv("/Users/andersspringborg/Downloads/Splitwise expenses Nov 30.csv")
    total_spent_by_person = df.groupby("Payer").sum()
    print(total_spent_by_person)



if __name__ == '__main__':
    main()