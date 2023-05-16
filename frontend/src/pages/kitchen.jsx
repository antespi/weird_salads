import React, { useState, useEffect } from 'react';
import MainLayout from '../layouts/main';
import API from '../api';
import Order from '../components/order';

const Kitchen = () => {

  const [orders, setOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState();

  const removeOrder = async(order) => {
    const newOrders = orders.filter(orderItem => orderItem.id !== order.id);
    setOrders(newOrders);
  }
  const setOrderStatus = async(order, status) => {
    API.put(`order/${order.id}`, {status: status}).then((response) => {
      removeOrder(order);
    }).catch(error => {
      // TODO: Show the error to the user
    });
  }

  const fetchOrders = async() => {
    setIsLoading(true);
    API.get('order', { params: { status: 'paid' } }).then((response) => {
      setOrders(response.data);
      setIsLoading(false);
      setError(null);
    }).catch(error => {
      setError(error.response.data.detail);
    });
  }

  useEffect(() => {
    fetchOrders();
  },[]);

  return (
    <MainLayout>
      <h2>Kitchen</h2>
      {error ? <div>ERROR: {error}</div> : ''}
      {isLoading ? 'Loading' : <div className="order-list">
        {orders.map((order, i) =>
          <div key={i} className='row'>
            <div className='col p-2 border'>
              <Order order={order} setOrderStatus={setOrderStatus}/>
            </div>
          </div>
        )}
        </div>
      }
    </MainLayout>
  );
}

export default Kitchen;
