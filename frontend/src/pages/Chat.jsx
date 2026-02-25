import { useState, useRef, useEffect } from 'react'
import { useAuth } from '../context/AuthContext' // to get user id

export default function Chat() {
    const [messages, setMessages] = useState([
        { id: 1, from: 'hr', text: 'Welcome to the chat exercise!' },
        { id: 2, from: 'employee', text: 'Hi there, how can I help?' },
    ])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const bottomRef = useRef(null)
    const { user } = useAuth() // assume user_id is stored in user.email or similar

    const sendMessage = async () => {
        if (!input.trim()) return
        // append user message immediately
        const userMsg = { id: Date.now(), from: 'employee', text: input }
        setMessages((msgs) => [...msgs, userMsg])
        setInput('')

        // send to backend
        setLoading(true)
        try {
            const resp = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: user?.email || 'anonymous',
                    message: input,
                }),
            })
            if (resp.ok) {
                const data = await resp.json()
                setMessages((msgs) => [
                    ...msgs,
                    { id: Date.now() + 1, from: 'hr', text: data.response },
                ])
            } else {
                const text = await resp.text()
                setMessages((msgs) => [
                    ...msgs,
                    { id: Date.now() + 2, from: 'hr', text: `Error: ${text}` },
                ])
            }
        } catch (err) {
            setMessages((msgs) => [
                ...msgs,
                { id: Date.now() + 3, from: 'hr', text: `Network error: ${err.message}` },
            ])
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])

    return (
        <div className="container vh-100 d-flex flex-column py-4">
            <div className="card flex-grow-1 shadow">
                <div className="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                    <h5 className="mb-0">Chat</h5>
                    <div className="d-flex align-items-center">
                        <span className="me-2">John Doe</span>
                        <img src="https://via.placeholder.com/32" alt="avatar" className="rounded-circle" />
                    </div>
                </div>
                <div className="card-body overflow-auto flex-grow-1" style={{ maxHeight: '100%' }}>
                    {messages.map((msg) => (
                        <div
                            key={msg.id}
                            className={
                                'mb-2 d-flex ' +
                                (msg.from === 'employee' ? 'justify-content-end' : 'justify-content-start')
                            }
                        >
                            <div
                                className={
                                    'p-2 rounded ' +
                                    (msg.from === 'employee' ? 'bg-primary text-white' : 'bg-light text-dark')
                                }
                                style={{ maxWidth: '75%' }}
                            >
                                {msg.text}
                            </div>
                        </div>
                    ))}
                    <div ref={bottomRef} />
                </div>
                <div className="card-footer">
                    <div className="input-group">
                        <button className="btn btn-outline-secondary" type="button">
                            🎤
                        </button>
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Type your message..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') sendMessage()
                            }}
                            disabled={loading}
                        />
                        <label className="btn btn-outline-secondary m-0">
                            <input
                                type="file"
                                hidden
                                onChange={(e) => {
                                    const file = e.target.files[0]
                                    if (file) {
                                        setMessages((msgs) => [
                                            ...msgs,
                                            { id: Date.now(), from: 'employee', text: `Uploaded: ${file.name}` },
                                        ])
                                    }
                                }}
                            />
                            📎
                        </label>
                        <button className="btn btn-primary" onClick={sendMessage} disabled={loading}>
                            {loading ? '...' : 'Send'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
