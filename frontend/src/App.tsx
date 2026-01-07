import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Toaster } from "sonner";
import Login from "./pages/login/login";
import Dashboard from "./pages/dashboard/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import InternPage from "./pages/User/UserPage";

const App = () => {
  return (
    <Router>
      <Toaster
        position="top-right"
        richColors
        toastOptions={{
          style: {
            borderRadius: "12px",
          },
        }}
      />

      <Routes>
        <Route path="/" element={<Login />} />

        {/* Protected Routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route
            path="/dashboard/interns"
            element={<InternPage type="interns" />}
          />
          <Route
            path="/dashboard/teams"
            element={<InternPage type="teams" />}
          />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
