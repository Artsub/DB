import React, { useState, useEffect } from "react";
import api from "./ApiTokenInter";
import { Container, Card, Button, Row, Col, Form, Modal } from "react-bootstrap";

const VenuesList = () => {
  const [venues, setVenues] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [currentVenue, setCurrentVenue] = useState({ id: null, name: "", address: "", capacity: 0 });
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newVenue, setNewVenue] = useState({ name: "", address: "", capacity: "" });
  const [role, setRole] = useState(null);

  useEffect(() => {
    fetchVenues();
    const storedRole = localStorage.getItem("role");
    setRole(storedRole);
  }, []);

  const fetchVenues = () => {
    api.get("/venues/")
      .then((response) => {
        setVenues(response.data);
      })
      .catch((error) => {
        console.error("Error fetching venues:", error);
      });
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Вы уверены, что хотите удалить эту площадку?")) {
      return;
    }

    try {
      await api.delete(`/venues/${id}`);
      setVenues(venues.filter(venue => venue.id !== id));
    } catch (error) {
      console.error("Error deleting venue:", error);
    }
  };

  const handleEditClick = (venue) => {
    setCurrentVenue(venue);
    setShowModal(true);
  };

  const handleUpdate = async () => {
    try {
      await api.put(`/venues/${currentVenue.id}`, {
        name: currentVenue.name,
        address: currentVenue.address,
        capacity: currentVenue.capacity,
      });
      setShowModal(false);
      fetchVenues();
    } catch (error) {
      console.error("Error updating venue:", error);
    }
  };

  const handleCreate = async () => {
    if (newVenue.capacity <= 0) {
      alert("Вместимость должна быть положительным числом.");
      return;
    }
    try {
      await api.post("/venues/", newVenue);
      setShowCreateModal(false);
      setNewVenue({ name: "", address: "", capacity: "" });
      fetchVenues();
    } catch (error) {
      console.error("Error creating venue:", error);
    }
  };

  return (
    <Container className="mt-4">
      <h2 className="mb-4">Список площадок</h2>
      {role === "1" && (
        <Button variant="success" className="mb-3" onClick={() => setShowCreateModal(true)}>
          Добавить площадку
        </Button>
      )}
      <Row>
        {venues.map((venue) => (
          <Col key={venue.id} md={6} lg={4} className="mb-4">
            <Card className="shadow-lg p-3">
              <Card.Body>
                <Card.Title className="fs-4">{venue.name}</Card.Title>
                <Card.Text>Местоположение: {venue.address}</Card.Text>
                <Card.Text>Вместимость: {venue.capacity}</Card.Text>
                {role === "1" && (
                  <div>
                    <Button variant="primary" className="me-2" onClick={() => handleEditClick(venue)}>
                      Изменить
                    </Button>
                    <Button variant="danger" onClick={() => handleDelete(venue.id)}>
                      Удалить
                    </Button>
                  </div>
                )}
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Редактировать площадку</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Название</Form.Label>
              <Form.Control
                type="text"
                value={currentVenue.name}
                onChange={(e) => setCurrentVenue({ ...currentVenue, name: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Местоположение</Form.Label>
              <Form.Control
                type="text"
                value={currentVenue.address}
                onChange={(e) => setCurrentVenue({ ...currentVenue, address: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Вместимость</Form.Label>
              <Form.Control
                type="number"
                value={currentVenue.capacity}
                onChange={(e) => setCurrentVenue({ ...currentVenue, capacity: parseInt(e.target.value) })}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>Закрыть</Button>
          <Button variant="success" onClick={handleUpdate}>Сохранить</Button>
        </Modal.Footer>
      </Modal>

      <Modal show={showCreateModal} onHide={() => setShowCreateModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Создать новую площадку</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Название</Form.Label>
              <Form.Control
                type="text"
                value={newVenue.name}
                onChange={(e) => setNewVenue({ ...newVenue, name: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Местоположение</Form.Label>
              <Form.Control
                type="text"
                value={newVenue.address}
                onChange={(e) => setNewVenue({ ...newVenue, address: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Вместимость</Form.Label>
              <Form.Control
                type="number"
                value={newVenue.capacity}
                onChange={(e) => setNewVenue({ ...newVenue, capacity: e.target.value })}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowCreateModal(false)}>Закрыть</Button>
          <Button variant="success" onClick={handleCreate}>Создать</Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default VenuesList;
