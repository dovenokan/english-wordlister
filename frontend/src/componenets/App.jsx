import { useState } from 'react'
import '../styles/App.css'
import Analysis from './analysis/Analysis'
import Header from './header/Header'
import Input from './input/Input'
import Stats from './stats/Stats'

function App() {
  return (
    <div className="App">
      <div className="main-container">
        <Input />
        <Stats />
        <Analysis />
      </div>
    </div>
  )
}

export default App
