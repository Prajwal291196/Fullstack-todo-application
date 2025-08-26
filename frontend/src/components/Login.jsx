import { useState } from "react";

export default function Login() {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const endpoint = isLogin ? "/login" : "/register";

    const res = await fetch(`http://127.0.0.1:8000${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }), // add email if register
    });

    const data = await res.json();
    console.log(data);
  };

  const handleUserName = (e) => {
    setUserName(e.target.value);
  }

  const handlePassword = (e) => {
    setPassword(e.target.value);
  }
  console.log(username, password);
  return (
    <div>
      <h2>{isLogin ? "Login" : "Register"}</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Username" onChange={(e)=>handleUserName(e)} required />
        {!isLogin && <input type="email" placeholder="Email" />}
        <input type="password" placeholder="Password" onChange={(e)=>handlePassword(e)} required />
        <button type="submit">{isLogin ? "Login" : "Register"}</button>
      </form>
      <p>
        {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
        <button onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? "Register here" : "Login here"}
        </button>
      </p>
    </div>
  );
}
