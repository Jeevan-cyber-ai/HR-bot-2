// simple fetch wrapper with base URL and error handling
const BASE_URL = 'http://127.0.0.1:8000' // empty uses same origin or proxy configured in Vite

export async function post(path, body) {
    const res = await fetch(`${BASE_URL}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    })
    if (!res.ok) {
        const text = await res.text()
        throw new Error(text || res.statusText)
    }
    return res.json()
}

