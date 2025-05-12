import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Container, ListGroup, Button, Modal, Form, Row, Col } from "react-bootstrap";
import api from "./ApiTokenInter";
import "../styles/styles.css"

function EventList() {
  const [events, setEvents] = useState([]);
  const [role, setRole] = useState(null); // Роль пользователя
  const [showAddEventModal, setShowAddEventModal] = useState(false);
  const [venues, setVenues] = useState([]);
  const [newEvent, setNewEvent] = useState({
    title: "",
    description: "",
    date: "",
    venue_name: "",
    category_name: "Концерт",
  });

  useEffect(() => {
    api.get("/events/")
      .then((response) => setEvents(response.data))
      .catch((error) => console.error("Ошибка загрузки событий!", error));

    // Получаем роль пользователя из localStorage
    const storedRole = localStorage.getItem("role");
    setRole(storedRole);

    api.get("/venues")
      .then((response) => setVenues(response.data))
      .catch((error) => console.error("Ошибка загрузки площадок:", error));
  }, []);

  const handleShowAddEventModal = () => setShowAddEventModal(true);
  const handleCloseAddEventModal = () => setShowAddEventModal(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewEvent({ ...newEvent, [name]: value });
  };

  const handleAddEventSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/events", newEvent);
      setShowAddEventModal(false);
      alert("Мероприятие успешно добавлено!");
    } catch (error) {
      console.error("Ошибка добавления мероприятия:", error);
      alert("Ошибка добавления мероприятия. Попробуйте снова.");
    }
  };

  const handleDeleteEvent = async (eventId) => {
    if (window.confirm("Вы уверены, что хотите удалить это мероприятие?")) {
      try {
        await api.delete(`/events/${eventId}`);
        // Обновляем список мероприятий после удаления
        const updatedEvents = events.filter(event => event.id !== eventId);
        setEvents(updatedEvents);
        alert("Мероприятие успешно удалено!");
      } catch (error) {
        console.error("Ошибка удаления мероприятия:", error);
        alert("Не удалось удалить мероприятие. Попробуйте снова.");
      }
    }
  };

  return (
    
    <Container>
      <h2 className="my-4">Предстоящие мероприятия</h2>

      {/* Кнопка видна только если роль = 1 (админ) */}
      {role === "1" && (
        <Button variant="success" className="mb-3" onClick={handleShowAddEventModal}>
          Добавить новое мероприятие
        </Button>
      )}

      <ListGroup>
        {events.map((event) => (
          <div class="row gy-5">
          <ListGroup.Item key={event.id} className="d-flex justify-content-between align-items-center">
            <div>
              <h4>{event.event_title}</h4>
              <p>{event.event_description}</p>
              <p><strong>Дата:</strong> {new Date(event.event_date).toLocaleString()}</p>
            </div>
            <div>
              <Link to={`/events/${event.id}`}>
              {role && (<Button variant="primary">Подробнее</Button>)}
              </Link>
              {/* Кнопка удаления видна только для админа */}
              {role === "1" && (
                <Button 
                  variant="danger" 
                  onClick={() => handleDeleteEvent(event.id)}
                  className="ms-2"
                >
                  Удалить
                </Button>
              )}
            </div>
          </ListGroup.Item>
          </div>
        ))}
      </ListGroup>

      {/* Модальное окно для добавления мероприятия */}
      <Modal show={showAddEventModal} onHide={handleCloseAddEventModal}>
        <Modal.Header closeButton>
          <Modal.Title>Добавить новое мероприятие</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleAddEventSubmit}>
            <Row>
              <Col md={12}>
                <Form.Group className="mb-3">
                  <Form.Label>Название мероприятия</Form.Label>
                  <Form.Control type="text" name="title" value={newEvent.title} onChange={handleInputChange} required />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={12}>
                <Form.Group className="mb-3">
                  <Form.Label>Описание</Form.Label>
                  <Form.Control as="textarea" rows={3} name="description" value={newEvent.description} onChange={handleInputChange} required />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={12}>
                <Form.Group className="mb-3">
                  <Form.Label>Дата и время</Form.Label>
                  <Form.Control type="datetime-local" name="date" value={newEvent.date} onChange={handleInputChange} required />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={12}>
                <Form.Group className="mb-3">
                  <Form.Label>Площадка</Form.Label>
                  <Form.Select name="venue_name" value={newEvent.venue_name} onChange={handleInputChange} required>
                    <option value="">Выберите площадку</option>
                    {venues.map((venue) => (
                      <option key={venue.id} value={venue.name}>
                        {venue.name}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={12}>
                <Form.Group className="mb-3">
                  <Form.Label>Категория</Form.Label>
                  <Form.Select name="category_name" value={newEvent.category_name} onChange={handleInputChange} required>
                    <option value="Концерт">Концерт</option>
                    <option value="Фестиваль">Фестиваль</option>
                    <option value="Театр">Театр</option>
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Button variant="primary" type="submit">Добавить мероприятие</Button>
          </Form>
        </Modal.Body>
      </Modal>
    </Container>
    
  );
}

export default EventList;