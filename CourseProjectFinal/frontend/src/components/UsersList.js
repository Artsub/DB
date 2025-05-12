import React, { useState, useEffect } from "react";
import api from "./ApiTokenInter";
import { Container, Card, Button, Row, Col,} from "react-bootstrap";

const UsersList = () => {
  const [users, setUsers] = useState([]);


  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = () => {
    api.get("/users/")
      .then((response) => setUsers(response.data))
      .catch((error) => console.error("Error fetching users:", error));
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Вы уверены, что хотите удалить этого пользователя?")) {
      return;
    }

    try {
      await api.delete(`/users/${id}`);
      setUsers(users.filter(user => user.id !== id));
    } catch (error) {
      console.error("Error deleting user:", error);
    }
  };

  const handleChangeRole = async (id) => {
    try {
      const response = await api.patch(`/users/${id}`);
      alert(response.data.message);
      setUsers(users.map(user =>
        user.id === id ? { ...user, role_id: user.role_id === 1 ? 2 : 1 } : user
      ));
    } catch (error) {
      console.error("Error changing user role:", error);
    }
  };


  return (
    <Container className="mt-4">
      <h2 className="mb-4">Список пользователей</h2>
      <Row>
        {users.map((user) => (
          <Col key={user.id} md={6} lg={4} className="mb-4">
            <Card className="shadow-lg p-3">
              <Card.Body>
                <Card.Title className="fs-4">{user.username}</Card.Title>
                <Card.Text>Роль пользователя: {user.role_id > 1 ? "Пользователь" : "Админ"}</Card.Text>
                <Button variant="danger" onClick={() => handleDelete(user.id)} className="me-2">
                  Удалить
                </Button>
                <Button variant="warning" onClick={() => handleChangeRole(user.id)} className="me-2">
                  Поменять роль
                </Button>
                
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

    
    </Container>
  );
};

export default UsersList;