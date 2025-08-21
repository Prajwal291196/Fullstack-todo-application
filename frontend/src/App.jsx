import { useState } from 'react'
import './App.css'
import Todo from './components/Todo'
import Login from './components/Login'
import {
  createBrowserRouter,
  RouterProvider,
  Navigate,
} from "react-router-dom";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const router = createBrowserRouter([
    {
      path: "/",
      element: isLoggedIn ? (
        <Navigate to="/todo" replace />
      ) : (
        <Login onLogin={() => setIsLoggedIn(true)} />
      ),
    },
    {
      path: "/todo",
      element: isLoggedIn ? <Todo /> : <Navigate to="/" replace />,
    },
  ]);

  return <RouterProvider router={router} />;
}


export default App
