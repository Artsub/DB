import React, { useState, useEffect } from "react";
import api from "./ApiTokenInter";
import { Container, Table, Spinner, Alert } from "react-bootstrap";

const LogsList = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/logs/")
      .then((response) => {
        setLogs(response.data);
        setLoading(false);
      })
      .catch((error) => {
        setError("Failed to load logs");
        setLoading(false);
        console.error("Error fetching logs:", error);
      });
  }, []);

  if (loading) {
    return (
      <Container className="text-center mt-5">
        <Spinner animation="border" variant="primary" />
        <p>Loading logs...</p>
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
    <Container className="mt-4">
      <h2 className="mb-4">Логи базы данных</h2>
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>ID</th>
            <th>Действие</th>
            <th>Броннирование ID</th>
            <th>Таблица</th>
            <th>Время</th>
            <th>Новые данные</th>
            <th>Старые данные</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log) => (
            <tr key={log.id}>
              <td>{log.id}</td>
              <td>{log.action_type}</td>
              <td>{log.record_id}</td>
              <td>{log.table_name}</td>
              <td>{new Date(log.action_time).toLocaleString()}</td>
              <td><pre>{JSON.stringify(log.new_data, null, 2)}</pre></td>
              <td><pre>{JSON.stringify(log.old_data, null, 2)}</pre></td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Container>
  );
};

export default LogsList;
