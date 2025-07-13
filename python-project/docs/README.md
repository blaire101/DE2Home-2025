
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

<div align="center">
  <img src="Cinema-ClassDiagram.png" alt="Class Diagram" width="400">
</div>

Detail Class Diagram

<div align="center">
  <img src="Mermaid-detail-class-design-1.png" alt="Detail Class Diagram" width="800">
</div>

## 3. Sequence Diagram 

- **Application Start** Sequence Diagram    
- **Booking Tickets** Sequence Diagram    
- **Check Bookings** Sequence Diagram    
- **Exit** Sequence Diagram  

“**Application Start**” Sequence Diagram

<div align="center">
  <img src="Mermaid-ApplicationStart-SeqDiagram.png" alt="Application Start Sequence Diagram" width="800">
</div>

“**Booking Tickets**” Sequence Diagram

<div align="center">
  <img src="Mermaid-BookTickets-SeqDiagram.png" alt="Booking Tickets Sequence Diagram" width="800">
</div>

“**Check Bookings**” Sequence Diagram

<div align="center">
  <img src="Mermaid-CheckBookings-SeqDiagram.png" alt="Check Bookings Sequence Diagram" width="800">
</div>

“**Exit**” Sequence Diagram  

<div align="center">
  <img src="Mermaid-Exit-SeqDiagram.png" alt="Exit Sequence Diagram" width="500">
</div>


