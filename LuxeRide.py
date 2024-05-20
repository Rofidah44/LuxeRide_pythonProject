import csv
from datetime import datetime

# Global variables
available_cars = {"Mercedes-Benz C-Class": 5, "Aston Martin Vantage": 3, "Range Rover Vogue": 2, "Bentley Continental GT Convertible" : 4}
rental_records = {}

rental_file = "rental_records.csv"
rental_columns = ["Name", "ID", "Car", "Quantity", "Rental Start Time", "Rental Mode"]


# Function to display available cars
def display_available_cars(admin_mode=False):
    print("Available Cars:")
    if admin_mode:
        for car, stock in available_cars.items():
            print(f"{car}: {stock}")
    else:
        for car in available_cars.keys():
            print(car)
 
# Function to rent a car
def rent_car(name, id_input, rental_mode):
    display_available_cars()
    selected_cars = []
    num_cars = int(input("Enter the total number of cars you want to rent: "))

    for i in range(num_cars):
        car = input("Enter the name of car {}: ".format(i + 1))
        if car in available_cars and available_cars[car] > 0:
            selected_cars.append(car)
            available_cars[car] -= 1
        else:
            print("Car '{}' is not available. Please choose another car.".format(car))

    if len(selected_cars) == num_cars:
        now = datetime.now()
        rental_start_time = now.strftime("%Y-%m-%d %H:%M:%S")
        for car in selected_cars:
            rental_records[car] = (1, rental_start_time, rental_mode, name, id_input)
            save_rental_records()
        print("Cars rented successfully!")

        # Display booking summary
        print("Booking Summary:")
        print("Name: {}".format(name))
        print("ID: {}".format(id_input))
        print("Rental Start Time: {}".format(rental_start_time))
        print("Rental Mode: {}".format(rental_mode))
        print("Cars Rented:")
        for car in selected_cars:
            print("- {}".format(car))

    else:
        print("Failed to rent the cars. Please check availability.")

def save_rental_records():
    with open(rental_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(rental_columns)
        for car, record in rental_records.items():
            # Reorder the record to match the column order
            reordered_record = [record[3], record[4], car, record[0], record[1], record[2]]
            writer.writerow(reordered_record)

# Function to load rental records from a file
def load_rental_records():
    try:
        with open(rental_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                car = row[0]
                record = tuple(row[1:])
                rental_records[car] = record
    except FileNotFoundError:
        pass

# Function to calculate rental period
def calculate_rental_period(start_time, end_time, rental_mode):
    start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    if rental_mode == "hourly":
        rental_period = (end_datetime - start_datetime).seconds / 3600
    elif rental_mode == "daily":
        rental_period = (end_datetime - start_datetime).days
    elif rental_mode == "weekly":
        rental_period = (end_datetime - start_datetime).days / 7
    return rental_period

# Function to return a car and generate bill
def return_car(car):
    if car in rental_records:
        num_cars, rental_start_time, rental_mode, name, id_input = rental_records[car]
        del rental_records[car]
        now = datetime.now()#get the current time
        rental_end_time = now.strftime("%Y-%m-%d %H:%M:%S")#convert the current time into string format
        rental_period = calculate_rental_period(rental_start_time, rental_end_time, rental_mode)
        bill_amount = calculate_bill(car, num_cars, rental_mode, rental_period)
        available_cars[car] += num_cars
        save_rental_records()
        print("Bill Amount: ${}".format(bill_amount))
        print("Car return successfully Thank You! ")
    else:
        print("Car not rented.")

# Function to calculate bill amount
def calculate_bill(car, num_cars, rental_mode, rental_period):
    car_rates = {"hourly": 10, "daily": 50, "weekly": 200}
    if rental_mode in car_rates:
        return car_rates[rental_mode] * num_cars * rental_period
    else:
        return 0

# Function to display menu for customer
def customer_menu():
    print("\n1. Display Available Cars")
    print("2. Rent a Car")
    print("3. Return a Car")
    print("4. Exit")


# Function to display menu for admin
def admin_menu():
    print("\n1. Display Available Cars")
    print("2. Add Cars to Inventory")
    print("3. View Booking Details")
    print("4. Exit")

# Function to display booking details for admin

def view_booking_details():
    print("\nBooking Details:")
    for car, record in rental_records.items():
        print(f"User: {record[3]}, Car: {car}, Number of Cars: {record[0]}")


# Main function
def main():
    load_rental_records()
    while True:
        access_level = input("Enter your access level (customer/admin/exit): ").lower()

        if access_level == "customer":
            customer_menu()
            choice = int(input("Enter your choice: "))
            if choice == 1:
                display_available_cars(admin_mode=False)
            elif choice == 2:
                name = input("Enter your name: ")
                id_input = input("Enter your ID: ")
                rental_mode = input("Enter rental mode (hourly/daily/weekly): ")
                rent_car(name, id_input, rental_mode)
            elif choice == 3:
                car = input("Enter the name of the car you want to return: ")
                return_car(car)
            elif choice == 4:
                break
            else:
                print("Invalid choice. Please try again.")

        elif access_level == "admin":
            admin_menu()
            choice = int(input("Enter your choice: "))

            if choice == 1:
                display_available_cars(admin_mode=True)
            elif choice == 2:
                car = input("Enter the name of the car you want to add: ")
                num_cars = int(input("Enter the number of cars you want to add: "))
                if car in available_cars:
                    available_cars[car] += num_cars
                else:
                    available_cars[car] = num_cars
                print("Cars added to inventory successfully!")
            elif choice == 3:
                view_booking_details()
            elif choice == 4:
                break
            else:
                print("Invalid choice. Please try again.")

        elif access_level == "exit":
            print("Exiting the program...")
            break

        else:
            print("Invalid access level. Please enter 'customer', 'admin', or 'exit'.")
            
if __name__ == "__main__":
    main()