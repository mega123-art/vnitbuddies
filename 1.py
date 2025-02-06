def is_leap_year(year):
    return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

def days_in_given_year(year):
    return 366 if is_leap_year(year) else 365

def find_day_of_week(day, month, year):
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if is_leap_year(year):
        days_in_month[1] = 29

    total_days = day - 1

    total_days += sum(days_in_month[:month - 1])

    for y in range(1, abs(year)):
        total_days += days_in_given_year(y) if year > 0 else -days_in_given_year(-y)

    return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][total_days % 7]


day = int(input("Enter day: "))
month = int(input("Enter month: "))
year = int(input("Enter year: "))
print(f"The day is {find_day_of_week(day, month, year)}.")