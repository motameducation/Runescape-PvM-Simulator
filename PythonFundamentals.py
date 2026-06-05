def generate_trip_instructions(location):
    print(f"Looks like you are going to {location}")
    print(f"You can use the public subway to get to {location}")

#generate_trip_instructions("London")


def calculate_expenses(plane_ticket_price, car_rental_rate, hotel_rate, trip_time):
    car_rental_total = car_rental_rate * trip_time
    hotel_total = hotel_rate * trip_time - 10
    trip_total = car_rental_total + hotel_total + plane_ticket_price
    print(f"Total expenses: {trip_total}")
    return trip_total


#print(calculate_expenses(200, 100, 100, 5))

def trip_planner(first_destination, second_destination, final_destination="Codecademy HQ"):
    print("Here is what your trip will look like!")
    print(f'First, we will stop in {first_destination}, then {second_destination}, and lastly {final_destination}')


#trip_planner("France", "Germany", "Denmark")
#trip_planner("Denmark", "France", "Germany")
#trip_planner("Iceland", "Germany", "India")

def exponents(base,power):
    new_list = [basenum**powernum for basenum in base for powernum in power]
    return new_list

#print(exponents([2, 3], [2, 3]))

def over_nine_thousand(lst):
    sum = 0
    for number in lst:
        sum += number
        if (sum > 9000):
            break
    return sum

#print(over_nine_thousand([8000, 900, 120, 5000]))

def max_num(nums):
    maximum = nums[0]
    for number in nums:
        if number > maximum:
            maximum = number
    return maximum

#print(max_num([50, -10, 0, 75, 20]))

def same_values(lst1, lst2):
    new_list = []
    for i in range(len(lst1)):
        if lst1[i] == lst2[i]:
            new_list.append(i)
    return new_list

#print(same_values([5, 1, -10, 3, 3], [5, 10, -10, 3, 5]))

def reversed_list(lst1, lst2):
    for i in range(len(lst1)):
        if lst1[i] != lst2[len(lst2) - 1 - i]:
            return False
    return True

#print(reversed_list([1, 2, 3], [3, 2, 1]))
#print(reversed_list([1, 5, 3], [3, 2, 1]))

def lots_of_math(a, b, c, d):
    first = a + b
    second = c - d
    third = first * second
    fourth = third % a
    print(first)
    print(second)
    print(third)
    return fourth

print(lots_of_math(1, 2, 3, 4))