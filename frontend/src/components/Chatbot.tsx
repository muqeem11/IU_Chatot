import React, { useState, useEffect, useRef } from 'react'

// Message type with optional meta for intent/confidence
type Message = {
  role: 'user' | 'bot'
  text: string
  meta?: { intent?: string; confidence?: number }
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// Browser speech APIs (guard for SSR/compat)
const SpeechRecognition: any = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
const synth: SpeechSynthesis | null = typeof window !== 'undefined' ? window.speechSynthesis : null

type ChatbotProps = {
  token: string
}

const Chatbot: React.FC<ChatbotProps> = ({ token }) => {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [listening, setListening] = useState(false)
  const [voiceEnabled, setVoiceEnabled] = useState(true) // speak bot replies
  const bottomRef = useRef<HTMLDivElement>(null)
  const recogRef = useRef<any>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Initialize speech recognition once
  useEffect(() => {
    if (!SpeechRecognition) return
    const rec = new SpeechRecognition()
    rec.lang = 'en-IN'
    rec.interimResults = false
    rec.maxAlternatives = 1
    rec.onresult = (e: any) => {
      const transcript = e.results?.[0]?.[0]?.transcript || ''
      if (transcript) {
        setInput(transcript)
        setTimeout(() => send(transcript), 50)
      }
    }
    rec.onend = () => setListening(false)
    rec.onerror = () => setListening(false)
    recogRef.current = rec
  }, [])

  const speak = (text: string) => {
    if (!voiceEnabled || !synth) return
    try {
      const utter = new SpeechSynthesisUtterance(text)
      utter.lang = 'en-IN'
      utter.rate = 1
      synth.cancel() // stop previous
      synth.speak(utter)
    } catch {}
  }

  const send = async (override?: string) => {
    const toSend = (override ?? input).trim()
    if (!toSend) return
    const userMsg: Message = { role: 'user', text: toSend }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ message: userMsg.text })
      })
      if (!res.ok) throw new Error('Request failed')
      const data = await res.json()
      const botMsg: Message = {
        role: 'bot',
        text: data.answer,
        meta: { intent: data.intent, confidence: data.confidence }
      }
      setMessages(prev => [...prev, botMsg])
      speak(botMsg.text)
    } catch (e: any) {
      setMessages(prev => [...prev, { role: 'bot', text: 'Error contacting server.' }])
    } finally {
      setLoading(false)
    }
  }

  const onKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') send()
  }

  const toggleListen = () => {
    if (!recogRef.current) return
    if (!listening) {
      try { recogRef.current.start(); setListening(true) } catch {}
    } else {
      try { recogRef.current.stop(); setListening(false) } catch {}
    }
  }

  const QuickChips = () => (
    <div className="helper">
      Try:
      <span className="tag">BTech fee structure</span>
      <span className="tag">ladkiyon ka hostel fees</span>
      <span className="tag">CSE average package</span>
      <span className="tag">MBA admission process</span>
    </div>
  )

  return (
    <div className="chat-panel">
      <div className="chat-box">
        {messages.length === 0 && (
          <div className="msg bot">
            <div className="avatar" />
            <div>
              <div className="bubble">
                Hi! I can help with fees, hostel, placements and admission process at Integral University. Ask me anything!
              </div>
              <QuickChips />
            </div>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            {m.role === 'bot' && <div className="avatar" />}
            <div>
              <div className="bubble">{m.text}</div>
              {m.meta?.intent && (
                <div className="meta">intent: {m.meta.intent} · conf: {m.meta.confidence?.toFixed(2)}</div>
              )}
            </div>
            {m.role === 'user' && <div className="avatar" />}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <div className="input-row">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={onKey}
          placeholder="Type your question..."
        />
        <button onClick={() => setVoiceEnabled(v => !v)} title="Toggle voice reply">
          {voiceEnabled ? '🔊' : '🔇'}
        </button>
        <button onClick={toggleListen} title="Speak your question" style={{ width: 48 }}>
          {listening ? '🎙️' : '🎤'}
        </button>
        <button
          onClick={() => { try { synth?.cancel() } catch {} ; setMessages([]); setInput('') }}
          title="Clear chat"
          style={{ marginRight: 8 }}
        >
          Clear
        </button>
        <button onClick={() => send()} disabled={loading}>{loading ? 'Sending...' : 'Send'}</button>
      </div>
    </div>
  )
}

export default Chatbot