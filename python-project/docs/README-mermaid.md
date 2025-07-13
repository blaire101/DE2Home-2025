
# Cinemas Booking System

## 1. 📝 Detailed Design 

Contains the following sections:

**Module Responsibilities**

| Module | Responsibility |
|---|---|
| **SeatMap** | Manages 2D seat matrix, renders UI, **default and custom allocation**, free count query |
| **Booking** | Domain **entity** storing **booking ID** and **seat list** |
| **BookingManager** | Generates **unique IDs**, stores and retrieves `Booking` **instances** |
| **CinemaBookingSystem** | Command-line interface, input, menus, flows |


## 2. Class Diagram

```mermaid
classDiagram
    class CinemaBookingSystem {
        - string title
    }
    class SeatMap
    class BookingManager
    class Booking

    CinemaBookingSystem *-- SeatMap : has
    CinemaBookingSystem *-- BookingManager : has
    BookingManager --> Booking : creates
```

Detail Class Diagram

```mermaid
classDiagram
    class SeatMap {
      - int rows
      - int cols
      - bool[][] grid
      + __init__(rows:int, cols:int)
      + free_count() : int
      + allocate_default(n:int) : List[(int,int)]
      + allocate_custom(start:str, n:int) : List[(int,int)]
      + render(highlight:List[(int,int)]) : void
      - _find_intervals_in_row(row:int) : List[(int,int)]
      - _best_block_in_row(row:int, count:int) : int
    }

    class Booking {
      - string id
      - List[(int,int)] seats
      + __init__(id:str, seats:List[(int,int)])
    }

    class BookingManager {
      - int _counter
      - Dict[string,Booking] _bookings
      + new_id() : string
      + add(seats:List[(int,int)]) : string
      + get(id:string) : Booking
    }

    class CinemaBookingSystem {
      - string title
      - SeatMap map
      - BookingManager manager
      + __init__(title:str, rows:int, cols:int)
      + run() : void
      - book_flow() : void
      - check_flow() : void
    }

    %% Relationships
    CinemaBookingSystem --> SeatMap : uses (call its methods)
    CinemaBookingSystem --> BookingManager : controls it manages orders
    BookingManager o-- Booking : creates
    CinemaBookingSystem --> Booking : displays*
```

## 3. Sequence Diagram 

0. **Application Start** Sequence Diagram 
1. **Booking Tickets** Sequence Diagram 
2. **Check Bookings** Sequence Diagram 
3. **Exit** Sequence Diagram 

“0. **Application Start**” Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant S as CinemaBookingSystem

    U->>S: start application
    S->>U: prompt "Define movie title and seating map in [Title] [Rows] [SeatsPerRow]"
    U->>S: "Inception 8 10"
    S->>S: new SeatMap(rows=8, cols=10)
    S->>S: new BookingManager()
    S->>U: display main menu
    note right of U: Welcome to Cinemas\n[1] Book tickets for Inception (80 seats available)\n[2] Check bookings\n[3] Exit
```

“1. **Booking Tickets**” Sequence Diagram

```sql
User → CinemaBookingSystem → SeatMap → CinemaBookingSystem → BookingManager → User
```

```mermaid
sequenceDiagram
    participant U as User
    participant S as CinemaBookingSystem
    participant SM as SeatMap
    participant M as BookingManager

    U->>S: select “Book Tickets”
    S->>U: prompt “Enter number of tickets (or blank to cancel)”
    alt user cancels (blank)
        S->>U: return to main menu
    else user enters n
        S->>SM: allocate_default(n)
        SM-->>S: default_seats
        S->>U: render(default_seats) + “Enter blank to confirm or new start”
        alt user confirms
            S->>M: add(default_seats)
            M-->>S: booking_id
            S->>U: print “Booking ID … confirmed”
        else user enters startPos
            S->>SM: allocate_custom(startPos, n)
            SM-->>S: custom_seats
            S->>U: render(custom_seats) + “Enter blank to confirm”
            U->>S: confirm (blank)
            S->>M: add(custom_seats)
            M-->>S: booking_id
            S->>U: print “Booking ID … confirmed”
        end
    end
```

“2. **Check Bookings**” Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant S as CinemaBookingSystem
    participant M as BookingManager

    U->>S: select “Check bookings”
    S->>U: prompt “Enter booking id (or blank to cancel)”
    alt user enters blank
        S->>U: return to main menu
    else user enters id
        S->>M: get(id)
        alt found
            M-->>S: seats_list
            S->>U: render(seats_list)
        else not found
            M-->>S: None
            S->>U: print “Booking id not found”
        end
    end
```

“3. **Exit**” Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant S as CinemaBookingSystem

    U->>S: select “Exit”
    S->>U: print “Thank you… Bye!”
    S-->>S: shutdown
```

