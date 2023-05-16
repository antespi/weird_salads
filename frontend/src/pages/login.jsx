import React, {useState, useRef} from 'react'
import Auth from '../auth';

const Login = ({setUserId}) => {
  const [pin, setPin] = useState(0);
  const [error, setError] = useState();

  const refPin = useRef(null);

  const login = async() => {
    if (!pin) return;
    setError(null);
    Auth.post(`login`, {pin: pin}).then((response) => {
      setUserId(response.data.id);
    }).catch(error => {
      setError(error.response.data.detail);
      setPin(null);
      refPin.current.value = null;
    });
  }

  const ifEnterThenLogin = async(event) => {
    if (event.key === "Enter") {
      login();
    }
  }

  return (
    <div className="container mt-3">
      <div className='row'>
        <div className='col'>
          <h1>Enter your PIN</h1>
        </div>
      </div>
      <div className='row'>
        <div className='col-xl-6 p-2'>
          <input ref={refPin} type="password" onChange={(e) => setPin(e.target.value)} onKeyUp={(e) => ifEnterThenLogin(e)}/>
          {error ?
            <div>ERROR: {error}</div>
          : ''}

        </div>
        <div className='col-xl-6 p-2'>
          <button className='btn btn-success' onClick={login}>Submit</button>
        </div>
      </div>
    </div>
  );
}

export default Login;
