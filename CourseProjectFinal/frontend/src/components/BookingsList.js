import React, { useEffect, useState } from "react";
import api from "./ApiTokenInter";
import { Container, ListGroup, Alert } from "react-bootstrap";

const BookingsList = () => {
  const [bookings, setBookings] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const response = await api.get("/bookings/");
        setBookings(response.data);
      } catch (err) {
        setError("Ошибка загрузки бронирований");
      }
    };

    fetchBookings();
  }, []);

  return (
    <Container>
      <h2 className="my-4">Список бронирований</h2>
      {error ? (
        <Alert variant="danger">{error}</Alert>
      ) : bookings.length > 0 ? (
        <ListGroup>
          {bookings.map((booking) => (
            <ListGroup.Item key={booking.id} className="d-flex justify-content-between align-items-center">
              <div>
                <h4>{booking.title}</h4>
                <p><strong>Пользователь:</strong> {booking.username}</p>
                <p><strong>Дата:</strong> {new Date(booking.booking_date).toLocaleDateString()}</p>
              </div>
              <strong style={{ color: booking.payment_status ? "green" : "red" }}>
                {booking.payment_status ? "Оплачено" : "Не оплачено"}
              </strong>
            </ListGroup.Item>
          ))}
        </ListGroup>
      ) : (
        <Alert variant="info">Нет бронирований.</Alert>
      )}
    </Container>
  );
};

export default BookingsList;
