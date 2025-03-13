import React, { useEffect, useState } from "react";
import api from "./ApiTokenInter";
import { Container, ListGroup, Button, Alert, Modal, Form } from "react-bootstrap";

const MyBookingsList = () => {
  const [bookings, setBookings] = useState([]);
  const [error, setError] = useState("");
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [currentBookingId, setCurrentBookingId] = useState(null);
  const [cardDetails, setCardDetails] = useState({ cardNumber: "", expiry: "", cvv: "" });

  const username = localStorage.getItem("username");

  useEffect(() => {
    if (!username) {
      setError("User not authenticated");
      return;
    }

    api
      .get(`/bookings/${username}`)
      .then((response) => setBookings(response.data))
      .catch((error) => {
        const errorMessage =
          typeof error.response?.data?.detail === "string"
            ? error.response.data.detail
            : "Failed to load bookings";
        setError(errorMessage);
      });
  }, [username]);

  const handleDeleteBooking = async (bookingId) => {
    if (!bookingId) {
      setError("Ошибка: ID бронирования отсутствует.");
      return;
    }

    try {
      await api.delete(`/bookings/${bookingId}`);
      setBookings((prevBookings) => prevBookings.filter((booking) => booking.id !== bookingId));
    } catch (error) {
      const errorMessage =
        typeof error.response?.data?.detail === "string"
          ? error.response.data.detail
          : "Не удалось удалить бронирование";
      setError(errorMessage);
    }
  };

  const handleOpenPaymentModal = (bookingId) => {
    setCurrentBookingId(bookingId);
    setCardDetails({ cardNumber: "", expiry: "", cvv: "" });
    setShowPaymentModal(true);
  };

  const handleClosePaymentModal = () => {
    setShowPaymentModal(false);
    setCurrentBookingId(null);
  };

  const handleCardDetailChange = (e) => {
    const { name, value } = e.target;
    setCardDetails((prev) => ({ ...prev, [name]: value }));
  };

  const validateCardDetails = () => {
    const { cardNumber, expiry, cvv } = cardDetails;
    const cardNumberRegex = /^\d{16}$/;
    const expiryRegex = /^(0[1-9]|1[0-2])\/\d{2}$/; // формат MM/YY
    const cvvRegex = /^\d{3}$/;

    if (!cardNumberRegex.test(cardNumber)) {
      alert("Номер карты должен состоять из 16 цифр.");
      return false;
    }
    if (!expiryRegex.test(expiry)) {
      alert("Срок действия должен быть в формате MM/YY.");
      return false;
    }
    if (!cvvRegex.test(cvv)) {
      alert("CVV должен состоять из 3 цифр.");
      return false;
    }
    return true;
  };

  const handlePaymentSubmit = async (e) => {
    e.preventDefault();
    if (!validateCardDetails()) return;

    try {
      await api.patch(`/bookings/${currentBookingId}`, { payment_status: true });
      setBookings((prev) =>
        prev.map((b) => (b.id === currentBookingId ? { ...b, payment_status: true } : b))
      );
      setShowPaymentModal(false);
      alert("Оплата прошла успешно!");
    } catch (error) {
      alert("Оплата не удалась. Попробуйте снова.");
      console.error("Error updating payment status:", error);
    }
  };

  return (
    <Container>
      <h2 className="my-4">Мои бронирования</h2>
      {error && <Alert variant="danger">{error}</Alert>}
      {bookings.length > 0 ? (
        <ListGroup>
          {bookings.map((booking) => (
            <ListGroup.Item key={booking.id} className="d-flex justify-content-between align-items-center">
              <div>
                <h4>{booking.title}</h4>
                <p>
                  <strong>Дата бронирования:</strong> {new Date(booking.booking_date).toLocaleDateString()}
                </p>
              </div>
              <div>
                <Button
                  variant={booking.payment_status ? "success" : "warning"}
                  className="me-2"
                  onClick={() => !booking.payment_status && handleOpenPaymentModal(booking.id)}
                >
                  {booking.payment_status ? "Оплачено" : "Не оплачено"}
                </Button>
                <Button variant="danger" onClick={() => handleDeleteBooking(booking.id)}>
                  Удалить
                </Button>
              </div>
            </ListGroup.Item>
          ))}
        </ListGroup>
      ) : (
        <Alert variant="info">Еще нет бронирований.</Alert>
      )}

      {/* Модальное окно для оплаты */}
      <Modal show={showPaymentModal} onHide={handleClosePaymentModal}>
        <Modal.Header closeButton>
          <Modal.Title>Оплата бронирования</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handlePaymentSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Номер карты</Form.Label>
              <Form.Control
                type="text"
                name="cardNumber"
                value={cardDetails.cardNumber}
                onChange={handleCardDetailChange}
                placeholder="Введите номер карты"
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Срок действия (MM/YY)</Form.Label>
              <Form.Control
                type="text"
                name="expiry"
                value={cardDetails.expiry}
                onChange={handleCardDetailChange}
                placeholder="MM/YY"
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>CVV</Form.Label>
              <Form.Control
                type="text"
                name="cvv"
                value={cardDetails.cvv}
                onChange={handleCardDetailChange}
                placeholder="Введите CVV"
                required
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Оплатить
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </Container>
  );
};

export default MyBookingsList;
