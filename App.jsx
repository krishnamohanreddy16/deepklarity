import React, {useState} from 'react'
import GenerateQuizTab from './components/GenerateQuizTab'
import HistoryTab from './components/HistoryTab'

export default function App(){
  const [tab, setTab] = useState('generate')
  return (
    <div className="container">
      <div className="header">
        <h1>AI Wiki Quiz Generator</h1>
        <div>Remote Test Project</div>
      </div>
      <div className="tabs">
        <div className="tab" onClick={()=>setTab('generate')}>Generate Quiz</div>
        <div className="tab" onClick={()=>setTab('history')}>History</div>
      </div>
      {tab === 'generate' ? <GenerateQuizTab /> : <HistoryTab />}
    </div>
  )
}
