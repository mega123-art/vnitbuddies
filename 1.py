def day_of_week(day, month, year):
    # Adjust January and February to be months 13 and 14 of the previous year
    if month < 3:
        month += 12
        year -= 1
    
    # Apply Zeller's formula
    h = (day + (13 * (month + 1)) // 5 + year + year // 4 - year // 100 + year // 400) % 7
    
    # Map result to days of the week
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    return days[h]

# Example usage
print(day_of_week(20, 7, 1969))  # Should print Sunday

