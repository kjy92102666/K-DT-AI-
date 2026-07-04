import { Routes, Route, BrowserRouter } from "react-router-dom";
import HomePage from "./pages/HomePage.jsx";
import CompanyPage from "./pages/CompanyPage.jsx";
import LifePage from "./pages/LifePage.jsx";
import TodoPage from "./pages/TodoPage.jsx";
import "./css/global.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Home */}
        <Route path="/homepage" element={<HomePage />} />
        <Route path="/company" element={<CompanyPage />} />
        <Route path="/life" element={<LifePage />} />
        <Route path="/todo" element={<TodoPage />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
