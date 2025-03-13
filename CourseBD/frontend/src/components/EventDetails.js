import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Container, Card, ListGroup, Spinner, Alert, Button } from "react-bootstrap";
import api from "./ApiTokenInter";

const EventDetails = () => {
  const { id } = useParams();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [bookingMessage, setBookingMessage] = useState("");

  useEffect(() => {
    api.get(`/events/${id}`)
      .then((response) => {
        if (response.data.length > 0) {
          setEvent(response.data[0]);
        } else {
          setError("Event not found.");
        }
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to fetch event details.");
        setLoading(false);
      });
  }, [id]);

  const handleBooking = async () => {
    try {
      await api.post("/bookings/", {
        user_id: 0,
        event_id: id,
        booking_date: new Date().toISOString().replace("Z", ""),
        payment_status: false,
      });
      setBookingMessage("Booking successful!");
    } catch (error) {
      setBookingMessage("Booking failed. Please try again.");
    }
  };

  if (loading) {
    return (
      <Container className="text-center mt-5">
        <Spinner animation="border" />
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-5">
        <Alert variant="danger">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container className="mt-5">
      <Card>
        <Card.Body>
          <Card.Title className="mb-4">{event.event_title}</Card.Title>
          <Card.Subtitle className="mb-3 text-muted"><strong>Место проведения: </strong>
            {event.venue_name} 
          </Card.Subtitle>
          <Card.Subtitle className="mb-3 text-muted"> <strong>Дата проведения: </strong>{new Date(event.event_date).toLocaleString()}</Card.Subtitle>
          <Card.Text><strong>Подробное описание мероприятия: </strong>{event.event_description}</Card.Text>
          <ListGroup>
            <ListGroup.Item><strong>Категория:</strong> {event.category_name}</ListGroup.Item>
            <ListGroup.Item><strong>Спонсоры:</strong> {event.sponsors.length > 0 ? event.sponsors.join(", ") : "Без спонсоров"}</ListGroup.Item>
          </ListGroup>
          <Button variant="primary" className="mt-3" onClick={handleBooking}>
            Забронировать
          </Button>
          {bookingMessage && <Alert className="mt-3" variant={bookingMessage.includes("successful") ? "success" : "danger"}>{bookingMessage}</Alert>}
        </Card.Body>
      </Card>
    </Container>
  );
};

export default EventDetails;
