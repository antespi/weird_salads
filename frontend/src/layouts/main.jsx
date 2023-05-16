import React from 'react'
import { Link } from 'react-router-dom'
import { logout } from '../auth'

function MainLayout({children}) {
  const doLogout = async() => {
    logout();
  }

  return (
    <div>
    <header>
      <nav className="navbar navbar-light bg-success top-menu">
        <div className="container">
          <Link to="/pos" className="navbar-brand">POS</Link>
          <Link to="/kitchen" className="navbar-brand">Kitchen</Link>
          <Link to="/reception" className="navbar-brand">Reception</Link>
          <Link to="/waste" className="navbar-brand">Waste</Link>
          <Link to="/stock" className="navbar-brand">Stock</Link>
          <button className='btn btn-danger navbar-brand' onClick={doLogout}>Logout</button>
        </div>
      </nav>
    </header>
    <main>
      <div className='container mt-3'>
        {children}
      </div>
    </main>
  </div>
  )
}

export default MainLayout
