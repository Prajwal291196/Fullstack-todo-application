import { useState, useEffect } from 'react'
import { getTodos, addTodo, updateTodo, deleteTodo } from "../api/todoApi";

const Todo = () => {
    const [todos, setTodos] = useState([])
    const [todo, setTodo] = useState('')
    const [error, setError] = useState(null);

    //Fetch todos from backend
    useEffect(() => {
        async function fetchData() {
            try {
                const data = await getTodos();
                setTodos(data);
            } catch (err) {
                setError('Failed to fetch todos. Please login again.');
                // Redirect to login if unauthorized
                if (err.response?.status === 401) {
                    window.location.href = '/login';
                }
            }
        }
        fetchData();
    }, []);
    // const handleDelete = (index) => {
    //     const newTodos = todos.filter((i) => i.index !== index)
    //     setTodos(newTodos)
    // }
    const handleDelete = async (id) => {
        try {
            await deleteTodo(id);
            setTodos(todos.filter((item) => item.id !== id));
        } catch (err) {
            setError('Failed to delete todo');
        }
    };
    // const handleAddTodo = (todo) => {
    //     setTodos([...todos, { 'index': todos.length + 1, 'value': todo }])
    //     setTodo('')
    // }
    // Add new todo
    const handleAddTodo = async () => {
        try {
            const newTodo = { title: todo, completed: false };
            const savedTodo = await addTodo(newTodo);
            setTodos([...todos, savedTodo]);
            setTodo("");
        } catch (err) {
            setError('Failed to add todo');
        }
    };
    return (
        <div>
            <h1>Todo List</h1>
            <p>Here you can manage your tasks.</p>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <input
                type="text"
                value={todo}
                onChange={(e) => setTodo(e.target.value)}
                placeholder="Add a new todo" />
            {todo && <button onClick={() => handleAddTodo()}>Add Todo</button>}
            <br /><br />
            <div>
                <h2>Current Todos</h2>
                {todos.map((item) => (
                    <div key={item.id}>
                        <span>{item.title}</span>
                        <button onClick={() => handleDelete(item.id)}>Delete</button>
                        <br />
                    </div>
                ))}
            </div>

        </div>
    )
}

export default Todo
