import { useState, useEffect } from 'react'
import { getTodos, addTodo, updateTodo, deleteTodo } from "../api/todoApi";

const Todo = () => {
    const [todos, setTodos] = useState([])
    const [todo, setTodo] = useState('')

    //Fetch todos from backend
    useEffect(() => {
        async function fetchData() {
            const data = await getTodos();
            setTodos(data);
        }
        fetchData();
    }, []);
    // const handleDelete = (index) => {
    //     const newTodos = todos.filter((i) => i.index !== index)
    //     setTodos(newTodos)
    // }
    const handleDelete = async (id) => {
        await deleteTodo(id);
        setTodos(todos.filter((item) => item.id !== id));
    };
    // const handleAddTodo = (todo) => {
    //     setTodos([...todos, { 'index': todos.length + 1, 'value': todo }])
    //     setTodo('')
    // }
    // Add new todo
    const handleAddTodo = async () => {
        const newTodo = { title: todo, completed: false };
        const savedTodo = await addTodo(newTodo);
        setTodos([...todos, savedTodo]);
        setTodo("");
    };
    return (
        <div>
            <h1>Todo List</h1>
            <p>Here you can manage your tasks.</p>
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
