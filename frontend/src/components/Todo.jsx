import { useState } from 'react'

const Todo = () => {
    const [todos, setTodos] = useState([])
    const [todo, setTodo] = useState('')

    const handleDelete = (index) => () => {
        const newTodos = todos.filter((i) => i.index !== index)
        setTodos(newTodos)
    }
    return (
        <div>
            <h1>Todo List</h1>
            <p>Here you can manage your tasks.</p>
            <input
                type="text"
                value={todo}
                onChange={(e) => setTodo(e.target.value)}
                placeholder="Add a new todo" />
            {todo && <button onClick={() => {
                setTodos([...todos, { 'index': todos.length + 1, 'value': todo }])
                setTodo('')
            }}>Add Todo</button>}
            <br /><br />
            <div>
                <h2>Current Todos</h2>
                {todos.map((item) => (
                    <>
                        <span key={item.index}>{item.value}</span>
                        <button onClick={handleDelete(item.index)}>Delete</button>
                        <br />
                    </>
                ))}
            </div>

        </div>
    )
}

export default Todo
