import { useState } from "react";
import { signUp } from "../api";

export default function SignUp() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await signUp(form);
      setMsg(res.data.message);
    } catch (err) {
      setMsg(err.response.data.detail || "Error occurred");
    }
  };

  return (
    <div>
      <h2>Client Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" placeholder="Email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <input type="password" placeholder="Password" onChange={(e) => setForm({ ...form, password: e.target.value })} />
        <button type="submit">Sign Up</button>
      </form>
      <p>{msg}</p>
    </div>
  );
}
