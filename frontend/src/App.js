import 'bootstrap/dist/css/bootstrap.css'
import './App.css';
import React, {useState} from 'react'
import {
    BrowserRouter as Router,
    Routes,
    Route
} from 'react-router-dom';
import Home from './pages/home';
import Pos from './pages/pos';
import Kitchen from './pages/kitchen';
import Reception from './pages/reception';
import Waste from './pages/waste';
import Stock from './pages/stock';
import Login from './pages/login';
import { setUserIdSession, getUserIdSession } from './auth';


function App() {
  const [userIdState, setUserIdState] = useState(getUserIdSession());

  const setUserId = async(userId) => {
    setUserIdSession(userId);
    setUserIdState(userId);
    window.location.reload();
  }

  if(!userIdState) {
    return <Login setUserId={setUserId} />
  }

  return (
    <Router>
        <Routes>
            <Route path="/" element={<Home/>}/>
            <Route path="/pos" element={<Pos/>}/>
            <Route path="/kitchen" element={<Kitchen/>}/>
            <Route path="/reception" element={<Reception/>}/>
            <Route path="/waste" element={<Waste/>}/>
            <Route path="/stock" element={<Stock/>}/>
        </Routes>
    </Router>
  );
}

export default App;
