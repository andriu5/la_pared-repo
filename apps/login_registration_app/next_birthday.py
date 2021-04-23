import datetime

# fecha = '1988-04-20'

# fechaNacimientoUsuario = {
#     "year": fecha[0:4],
#     "month": fecha[5:7],
#     "day": fecha[8:10]
# }
# print(fechaNacimientoUsuario)
# print(int(fechaNacimientoUsuario['year']),int(fechaNacimientoUsuario['month']),int(fechaNacimientoUsuario['day']))

def calculate_days_left_for_next_birthday(**fecha):
    birth = datetime.date(int(fecha['year']),int(fecha['month']),int(fecha['day']))
    print("Birth: ", birth)

    today = datetime.date.today()
    print("Today: ", today)

    if today.month == birth.month and today.day >= birth.day or today.month > birth.month:
        if today.day == birth.day:
            print("Today is the User's Birthday!")
            return 0
        nextBirthdayYear = today.year + 1  # the birthday is the next year!
    else:
        nextBirthdayYear = today.year  # the birthday is this year!
    # Calculate the Next Birthday
    nextBirthday = datetime.date(nextBirthdayYear, birth.month, birth.day)
    print("Next Birthday: ", nextBirthday)
    # Calculate the next birthday - today
    diff = nextBirthday - today
    #print("Days left for the next birthday: ", diff.days)
    return diff.days

# print("Days left for the next birthday: ", calculate_days_left_for_next_birthday(**fechaNacimientoUsuario))