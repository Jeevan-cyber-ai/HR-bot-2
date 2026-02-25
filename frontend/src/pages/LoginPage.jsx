import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
    const { login } = useAuth()
    const navigate = useNavigate()
    const [error, setError] = useState('')
    const [role, setRole] = useState('')

    const handleLogin = (role) => {
        // in a real app you'd verify credentials here
        if (!role) {
            setError('Please select a role')
            return
        }
        login({ role, email: `${role}@example.com` })
        navigate(role === 'hr' ? '/hr-dashboard' : '/chat')
    }

    const handleSubmit = () => {
        if (!role) {
            setError('Please select a role')
            return
        }
        handleLogin(role)
    }

    const handleCancel = () => {
        setRole('')
        setError('')
    }

    return (
        <div className="container vh-100 d-flex align-items-center justify-content-center bg-light">
            <div className="card p-4 shadow-sm" style={{ maxWidth: '400px', width: '100%' }}>
                <h1 className="h3 mb-3 text-center">Sign in</h1>
                <p className="text-center text-secondary">Please choose your role and continue</p>

                {error && <div className="alert alert-danger py-1">{error}</div>}

                <div className="form-check">
                    <input
                        className="form-check-input"
                        type="radio"
                        name="role"
                        id="roleEmployee"
                        value="employee"
                        checked={role === 'employee'}
                        onChange={() => {
                            setRole('employee')
                            setError('')
                        }}
                    />
                    <label className="form-check-label" htmlFor="roleEmployee">
                        Employee
                    </label>
                </div>
                <div className="form-check">
                    <input
                        className="form-check-input"
                        type="radio"
                        name="role"
                        id="roleHR"
                        value="hr"
                        checked={role === 'hr'}
                        onChange={() => {
                            setRole('hr')
                            setError('')
                        }}
                    />
                    <label className="form-check-label" htmlFor="roleHR">
                        HR
                    </label>
                </div>

                <div className="d-flex justify-content-end mt-4">
                    <button
                        type="button"
                        className="btn btn-secondary me-2"
                        onClick={handleCancel}
                    >
                        Cancel
                    </button>
                    <button
                        type="button"
                        className="btn btn-primary"
                        onClick={handleSubmit}
                    >
                        Submit
                    </button>
                </div>
            </div>
        </div>
    )
}
