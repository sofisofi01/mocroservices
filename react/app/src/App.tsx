
import {Outlet, useNavigate} from "react-router-dom";
import {Button} from "@mui/material";
import {useAuth} from "./hooks/useAuth.ts";

function App() {

    const navigate = useNavigate();
    const { logout, isAuthenticated } = useAuth();

    const handleLogout = () => {
        logout();
        navigate("/");
    };

  return (
      <>
          {isAuthenticated ? (
              <>
                  <Button
                      onClick={() => navigate("/expenseslist")}
                  >
                      Список расходов
                  </Button>
                  <Button
                      onClick={() => navigate("/expenseslist/create")}
                  >
                      Создать расход
                  </Button>
                  <Button
                      color="error"
                      onClick={handleLogout}
                  >
                      Выйти
                  </Button>
              </>
          ) : (
              <>
                  <Button
                      onClick={() => navigate("/")}
                  >
                      Войти
                  </Button>
                  <Button
                      onClick={() => navigate("/register")}
                  >
                      Регистрация
                  </Button>
              </>
          )}
          <Outlet />
      </>
  )
}

export default App
