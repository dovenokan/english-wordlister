import { useState } from 'react'
import '../styles/App.css'
import Analysis from './analysis/Analysis'
import Header from './header/Header'
import Input from './input/Input'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <Header />
      <Input />
      <Analysis />
    </div>
  )
}

export default App
