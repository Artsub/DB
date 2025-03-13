import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import api from "./ApiTokenInter";
import { Container, Card, Button, Spinner, Alert } from "react-bootstrap";

const VenueDetails = () => {
  // Параметр должен совпадать с тем, что указан в маршруте (например, /venues/:venue_id)
  const { venue_id } = useParams();
  const [venue, setVenue] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    console.log("Venue ID from useParams:", venue_id); // Проверка полученного параметра
    if (!venue_id) {
      setError("Invalid venue ID");
      setLoading(false);
      return;
    }

    api.get(`/venues/${venue_id}`)
      .then((response) => {
        setVenue(response.data);
        setLoading(false);
      })
      .catch((error) => {
        setError("Failed to load venue details");
        setLoading(false);
      });
  }, [venue_id]);

  if (loading) {
    return (
      <Container className="text-center mt-5">
        <Spinner animation="border" variant="primary" />
        <p>Loading venue details...</p>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="text-center mt-5">
        <Alert variant="danger">{error}</Alert>
        <Link to="/venues">
          <Button variant="secondary">Back to Venues</Button>
        </Link>
      </Container>
    );
  }

  return (
    <Container className="py-4">
      <Card className="shadow-sm">
        <Card.Body>
          <Card.Title className="mb-3">{venue.name}</Card.Title>
          <Card.Text>
            <strong>Address:</strong> {venue.address} <br />
            <strong>Capacity:</strong> {venue.capacity}
          </Card.Text>
          <Link to="/venues">
            <Button variant="secondary">Back to Venues</Button>
          </Link>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default VenueDetails;
