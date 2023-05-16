import React, { useRef } from 'react';
import { useReactToPrint } from 'react-to-print';
import { OrderToPrint } from './print/order';

const Order = ({order, setOrderStatus}) => {
  const componentRef = useRef();
  const handlePrint = useReactToPrint({
    content: () => componentRef.current,
  });

  const cancelOrder = async(order) => {
    setOrderStatus(order, 'cancelled');
  }
  const doOrder = async(order) => {
    setOrderStatus(order, 'done');
    handlePrint();
  }

  return (
    <>
      <div style={{display: "none"}}>
        <OrderToPrint order={order} ref={componentRef}/>
      </div>
      <div className="text-end"><h3>Order ID: {order.id}</h3></div>
      {order.items.map((item, j) =>
        <div key={j} className='row'>
          <div className='col p-3'>
            <h2>{item.qty}x {item.name}</h2>
            <table className='table table-responsive'>
              <thead>
                <tr className='table-primary'>
                  <td>Qty</td>
                  <td>Unit</td>
                  <td>Ingredient</td>
                </tr>
              </thead>
              <tbody>
                {item.ingredients.map((ingredient, k) =>
                  <tr key={k}>
                    <td>{ingredient.qty}</td>
                    <td>{ingredient.unit}</td>
                    <td>{ingredient.name}</td>
                  </tr>
                  )}
              </tbody>
            </table>
          </div>
        </div>
      )}
      <div className='row'>
        <div className='col'>
          <button className='btn btn-danger' onClick={() => cancelOrder(order)}>Cancel</button>
        </div>
        <div className='col text-end'>
          <button className='btn btn-success' onClick={() => doOrder(order)}>Done</button>
        </div>
      </div>
    </>
  );
}

export default Order;
