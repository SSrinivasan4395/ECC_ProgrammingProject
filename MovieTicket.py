"""
Movie Theater Ticket System
---------------------------
This project shows list of movies show in the theaters.
Once the user selects a movie, shows the choice of the day that user want to purchase for.
Based on user's choice of the day, shows the show times. For the current day it will display only future shows times that are left for the day.
Get the number of tickets that the user wants under each category Adult/Child/Senior, calculates the price and reduce the number of available seats in the system.
Calculate price based on Peak day or Normal day (10% more from base price), Child 30% discount and Senior 25% discount and 6% tax on the total order.
Monday-Thursday are normal days. Friday, Saturday and Sunday are Peak rate days.
Finally it will display movie ticket summary on the screen.
"""

import datetime

# Dictionary to store movie and ticket price information
movies = {
    "1": {"title": "Spider-Man: No Way Home", "price": 16.50},
    "2": {"title": "Thunderbolts", "price": 20.00},
    "3": {"title": "Snow White", "price": 5.00},
    "4": {"title": "Avengers:Endgame", "price": 15.50}
}

# List to store showtimes per day 
showtimes = ["9:00 AM", "11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"]

# Tuple for peak rate days (Friday, Saturday, Sunday)
peak_rate_days = ("Friday", "Saturday", "Sunday")

# list to store theater seats for the entire week for all the theaters
# Each movie has shows for 7 days × number of showtimes
# We'll calculate the index for seat as: movie_index * (days * showtimes) + day_index * showtimes + showtime_index
theater_seats = []
total_seats = 50
num_days = 7

# We need to initialize seats using a simple list. So variable for calculation
num_movies = len(movies)
num_showtimes = len(showtimes)

#Therefore number of shows for the week foll all the theaters is
total_shows = num_movies * num_showtimes * num_days

#One theater has 50 seats. Therefore for all the shows for all the movies for all the seven days is
for i in range(total_shows):
    theater_seats.append(total_seats)

#function to calculate seat index based on user's choice for movie, day and showtime
def get_seat_index(movie_num, day_index, showtime_index):
    """Calculate the index in theater_seats list"""
    # movie_num is 1-4, we need 0-3 for calculation
    shows_per_movie = num_days * num_showtimes
    return (movie_num - 1) * shows_per_movie + day_index * num_showtimes + showtime_index

#function to get next seven days based current system date.
def get_next_seven_days():
    """Get list of next seven days starting from today"""
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    next_seven_days = []
    
    today = datetime.date.today()
    current_day_num = today.weekday()  # Monday is 0, Sunday is 6
    
    # Convert weekday (Mon=0) to our format (Sun=0)
    if current_day_num == 6:
        current_day_num = 0
    else:
        current_day_num = current_day_num + 1
    
    # Create list of next 7 days
    for i in range(7):
        day_index = (current_day_num + i) % 7
        if i == 0:
            next_seven_days.append("Today")
        elif i == 1:
            next_seven_days.append("Tomorrow")
        else:
            next_seven_days.append(days_of_week[day_index])
    
    return next_seven_days, current_day_num

#Shows available movies to the user
def display_movies():
    print("\n=== MOVIE SELECTION ===")
    for key, movie_info in movies.items():
        print(f"{key}. {movie_info['title']} - ${movie_info['price']}")
    print("5. Exit")

#Ask user to pick a day and handles the selection
def get_day_choice():
    result = get_next_seven_days()
    days_list = result[0]
    today_index = result[1]
    
    print("\nWhat day do you want to watch the movie?")
    for i, day in enumerate(days_list, 1):
        print(f"{i}. {day}")
    print("8. Back to movie selection")
    
    choice = input("Enter choice (1-8): ")
    
    if choice == "8":
        return None, None, None
    elif choice in ["1", "2", "3", "4", "5", "6", "7"]:
        choice = int(choice)
        
        # Calculate actual date
        today = datetime.date.today()
        selected_date = today + datetime.timedelta(days=choice-1)
        
        # Get day name
        days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        actual_day_index = (today_index + choice - 1) % 7
        actual_day_name = days_of_week[actual_day_index]
        
        # Format date string
        date_string = selected_date.strftime("%A, %B %d, %Y")
        
        return choice - 1, actual_day_name, date_string
    else:
        print("Invalid choice. Please try again.")
        return None, None, None

#Filter function to filter out shows that have already passed for today
def filter_future_shows(is_today):

    if not is_today:
        return showtimes
    
    # Get current time
    now = datetime.datetime.now()
    current_hour = now.hour
    
    future_shows = []
    for time in showtimes:
        # Extract hour from showtime (e.g., "9:30 AM" -> 9)
        hour_str = time.split(":")[0]
        hour = int(hour_str)
        
        # Convert to 24-hour format if PM
        if "PM" in time and hour != 12:
            hour += 12
        elif "AM" in time and hour == 12:
            hour = 0
        
        # If showtime hour is greater than current hour, include it
        if hour > current_hour:
            future_shows.append(time)
    
    return future_shows

#Display Shows available, showtimes and handles selection
def display_showtimes(actual_day_name, is_today):
    # Filter out past shows for today
    available_times = filter_future_shows(is_today)
    
    if len(available_times) == 0:
        print("\nNo more shows available today.")
        return None
    
    print("\nAvailable showtimes:")
    for i, time in enumerate(available_times, 1):
        # Check if peak rate day
        if actual_day_name in peak_rate_days:
            print(f"{i}. {time} (Peak day - 10% extra)")
        else:
            print(f"{i}. {time}")
    
    print(f"{len(available_times) + 1}. Back to day selection")
    
    choice = input(f"\nSelect showtime (1-{len(available_times) + 1}): ")
    
    if choice == str(len(available_times) + 1):
        return None
    elif choice.isdigit() and 1 <= int(choice) <= len(available_times):
        return available_times[int(choice) - 1]
    else:
        print("Invalid choice.")
        return None

#Calculates price based on if it is peak rate or normal rate
def calculate_price(base_price, day_name):
    if day_name in peak_rate_days:
        return base_price * 1.10
    else:
        return base_price

#Get user's choice for number of tickets under each category: Adult/Child/Senior
def get_tickets(show_price):
    """Get number of tickets"""
    print("\nTicket Prices:")
    print(f"Adult: ${round(show_price, 2)}")
    print(f"Child (under 12): ${round(show_price * 0.7, 2)}")
    print(f"Senior (65+): ${round(show_price * 0.75, 2)}")
    print("\nEnter 0 for all to go back to showtime selection")
    
    adults = int(input("\nHow many adult tickets? "))
    children = int(input("How many child tickets? "))
    seniors = int(input("How many senior tickets? "))
    
    # Check if user wants to go back
    if adults == 0 and children == 0 and seniors == 0:
        return None
    else:
        total_tickets = adults + children + seniors
        
        # Calculate total cost
        total_cost = (adults * show_price + 
                      children * show_price * 0.7 + 
                      seniors * show_price * 0.75)
        #Calcuate 6% tax              
        total_cost = total_cost * (1.06)
        # Return tuple with ticket information
        return (adults, children, seniors, total_tickets, round(total_cost, 2))

#Checks if enough seats are available
def check_seats_available(movie_num, day_index, showtime_index, num_tickets):
    index = get_seat_index(movie_num, day_index, showtime_index)
    available = theater_seats[index]
    
    if available >= num_tickets:
        # Update available seats
        theater_seats[index] = available - num_tickets
        return True
    else:
        return False

#Print the movie ticket using dictionary for ticket information
def print_ticket(ticket_info):
    print("\n" + "*" * 40)
    print("       MOVIE TICKET")
    print("*" * 40)
    print(f"Name: {ticket_info['name']}")
    print(f"Movie: {ticket_info['movie']}")
    print(f"Theater: {ticket_info['theater']}")
    print(f"Day: {ticket_info['day']}")
    
    if ticket_info['is_peak']:
        print(f"Time: {ticket_info['time']} - Peak rate applies")
    else:
        print(f"Time: {ticket_info['time']}")
    
    print(f"Number of tickets: {ticket_info['num_tickets']}")
    print(f"Total cost with tax: ${ticket_info['total_cost']}")
    print("*" * 40)
    print("Thank you! Enjoy your movie!")
    print("*" * 40)

#Show how many seats are left
def display_seats_remaining(movie_num, day_index, showtime_index):
    index = get_seat_index(movie_num, day_index, showtime_index)
    remaining = theater_seats[index]
    print(f"\nSeats remaining for this show: {remaining}/{total_seats}")

def main():
    """Main program"""
    print("Welcome to Movie Theater Booking System!")
    print("---------------------------------------")
    
    # Show current time
    current_time = datetime.datetime.now()
    print(f"Current time: {current_time.strftime('%I:%M %p')}")
    
    # Main loop
    while True:
        display_movies()
        
        choice = input("\nWhich movie do you want to watch? (1-5): ")
        
        if choice == "5":
            print("\nThank you for using our system. Goodbye!")
            break
        elif choice in ["1", "2", "3", "4"]:
            # Get movie details from dictionary
            selected_movie = movies[choice]
            movie_title = selected_movie['title']
            base_price = selected_movie['price']
            theater_num = int(choice)
            
            # Get day
            result = get_day_choice()
            if result[0] is None:  # User chose to go back
                continue

            day_index = result[0]
            actual_day_name = result[1]
            date_string = result[2]
            
            
            # Get showtime
            is_today = (day_index == 0)
            selected_time = display_showtimes(actual_day_name, is_today)
            
            if selected_time is None:  # User chose to go back or no shows
                continue
            
            # Find showtime index
            showtime_index = showtimes.index(selected_time)
            
            # Calculate ticket price
            ticket_price = calculate_price(base_price, actual_day_name)
            
            # Check if peak rate day
            is_peak = actual_day_name in peak_rate_days
            
            # Get customer name
            name = input("\nEnter your name: ")
            
            # Get tickets
            ticket_result = get_tickets(ticket_price)
            
            if ticket_result is None:  # User chose to go back
                continue
            
            adults = ticket_result[0]
            children = ticket_result[1]
            seniors = ticket_result[2]
            total_tickets = ticket_result[3]
            total_cost = ticket_result[4]
            
            # Check if seats available
            if check_seats_available(theater_num, day_index, showtime_index, total_tickets):
                # Create ticket information dictionary
                ticket_info = {
                    'name': name,
                    'movie': movie_title,
                    'theater': theater_num,
                    'day': date_string,
                    'time': selected_time,
                    'num_tickets': total_tickets,
                    'total_cost': total_cost,
                    'is_peak': is_peak
                }
                
                # Print ticket
                print_ticket(ticket_info)
                
                # Show remaining seats
                display_seats_remaining(theater_num, day_index, showtime_index)
                
                # Ask if user wants to book another ticket
                another = input("\nBook another ticket? (y/n): ")
                if another.lower() != 'y':
                    print("\nThank you for using our system!")
                    break
            else:
                print("\nSorry! Not enough seats available for this show.")
                print("Please choose a different showtime.")
        else:
            print("Invalid choice. Please try again.")

# Start the program
if __name__ == "__main__":
    main()
