import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { Navbar, Nav, Container } from "react-bootstrap";
import EventList from "./components/EventList";
import EventDetails from "./components/EventDetails";
import VenuesList from "./components/VenuesList";
import VenueDetails from "./components/VenueDetail";
import RegisterForm from "./components/RegisterForm";
import LoginForm from "./components/LoginForm";
import BookingsList from "./components/BookingsList";
import MyBookingsList from "./components/MyBookingsLists";
import Logout from "./components/Logout";
import UsersList from "./components/UsersList";
import LogsList from "./components/LogsList";
import Backups from "./components/Backups";
import logo from "./assets/logo.png"
import "./styles/styles.css"

function App() {
  const [role, setRole] = useState(null);

  useEffect(() => {
    const storedRole = localStorage.getItem("role");
    setRole(storedRole);
  }, []);
  
  return (
    <div className="Maroon">
    <Router >
      {/* Навигация */}
      <Navbar bg="dark" variant="dark" expand="lg" style={{ height: "80px" }}>
        <Container>
        <Navbar.Brand as={Link} to="/" className="d-flex align-items-center">
            <img
              src={logo}
              alt="Logo"
              style={{ height: "70px", width: "70px", marginRight: "80px" }}
            />
            Мероприятия
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              {(role === "1" || role === "2") && <Nav.Link as={Link} to="/venues">Список площадок</Nav.Link>}
              {role === "1" && (<Nav.Link as={Link} to="/bookings">Бронирования</Nav.Link>)}
              {role === "1" && (<Nav.Link as={Link} to="/users">Пользователи</Nav.Link>)}
              {(role === "1" || role === "2") && <Nav.Link as={Link} to={`/bookings/${localStorage.getItem("username")}`}>Мои Бронирования</Nav.Link>}
              {role === "1" && <Nav.Link as={Link} to="/logs">Логи БД</Nav.Link>}
              {role === "1" && <Nav.Link as={Link} to="/backups">Резервные копии</Nav.Link>}
              {!role && <Nav.Link as={Link} to="/login">Войти</Nav.Link>}
              {!role && <Nav.Link as={Link} to="/register">Зарегистрироваться</Nav.Link>}
              {role && <Nav.Link as={Link} to="/logout">Выйти</Nav.Link>}

            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {/* Контент */}
      <Container className="mt-4" >
        <Routes>
          <Route path="/" element={<EventList />} />
          <Route path="/events/:id" element={<EventDetails />} />
          <Route path="/venues" element={<VenuesList />} />
          <Route path="/venues/:venue_id" element={<VenueDetails  />} />
          <Route path="/bookings" element={<BookingsList />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/users" element={<UsersList />} />
          <Route path="/logs" element={<LogsList />} />
          <Route path="/login" element={<LoginForm setRole={setRole} />} />  
          <Route path="/logout" element={<Logout setRole={setRole} />} />    
          <Route path="/bookings/:username" element={<MyBookingsList />} />
          <Route path="/backups" element={<Backups />} />
        </Routes>
      </Container>
    </Router>
    </div>
  );
}

export default App;