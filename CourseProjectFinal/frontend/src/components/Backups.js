import React, { useState } from 'react';
import api from "./ApiTokenInter";
import 'bootstrap/dist/css/bootstrap.min.css';

const Backups = () => {
  const [message, setMessage] = useState('');

  const handleBackup = async () => {
    try {
      const response = await api.post("/backups/backup");
      setMessage('Backup успешно выполнен!');
      console.log(response.data);
    } catch (error) {
      setMessage('Ошибка при выполнении Backup');
      console.error(error);
    }
  };

  const handleRestore = async () => {
    try {
      const response = await api.post("/backups/restore");
      setMessage('Restore успешно выполнен!');
      console.log(response.data);
    } catch (error) {
      setMessage('Ошибка при выполнении Restore');
      console.error(error);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col">
          <button className="btn btn-primary me-2" onClick={handleBackup}>
            Создать резервную копию
          </button>
          <button className="btn btn-success" onClick={handleRestore}>
            Восстановить резервную копию
          </button>
        </div>
      </div>
      {message && (
        <div className="row mt-3">
          <div className="col">
            <div className={`alert ${message.includes('Ошибка') ? 'alert-danger' : 'alert-success'}`}>
              {message}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Backups;