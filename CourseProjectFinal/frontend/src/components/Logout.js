import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "./ApiTokenInter";

const Logout = ({ setRole }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const logout = async () => {
      try {
        const token = localStorage.getItem("token");
        if (token) {
          await api.post("/logout", {}, {
            headers: { Authorization: `Bearer ${token}` }
          });
        }
      } catch (error) {
        console.error("Logout failed:", error);
      }
      
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      localStorage.removeItem("username");

      setRole(null);
      navigate("/");
    };

    logout();
  }, [navigate, setRole]);
  
  return null;
};

export default Logout;
