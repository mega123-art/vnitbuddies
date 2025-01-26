def day_of_week(day, month, year):
    # If the date is in January or February, treat it as part of the previous year
    if month < 3:
        month += 12
        year -= 1
    
    # Apply the Zeller's formula
    h = (day + (13 * (month + 1)) // 5 + year + year // 4 - year // 100 + year // 400) % 7
    
    # Map the number to a day of the week
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    return days[h]

# Get the date from the user
day = int(input("Enter the day of the month (e.g., 20): "))
month = int(input("Enter the month (1 for January, 2 for February, etc.): "))
year = int(input("Enter the year (e.g., 1969): "))

# Call the function and display the result
print(f"The day of the week on {month}/{day}/{year} was {day_of_week(day, month, year)}.")
