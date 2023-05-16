import React from "react";
import Monetary from '../monetary';

export const CartToPrint = React.forwardRef((props, ref) => {
    const {cart, totalAmount, orderId} = props;
    return (
      <div ref={ref} className="p-5">
          <h1>Order: {orderId} </h1>
          <table className='table'>
            <thead>
              <tr>
                <td>Name</td>
                <td>Price</td>
                <td>Qty</td>
                <td>Total</td>
              </tr>
            </thead>
            <tbody>
              { cart ? cart.map((cartProduct, key) =>
                  <tr key={key}>
                    <td>{cartProduct.name}</td>
                    <td><Monetary num={cartProduct.price}/></td>
                    <td>{cartProduct.qty}</td>
                    <td><Monetary num={cartProduct.totalAmount}/></td>
                  </tr>)
                : ''}
            </tbody>
          </table>
          <h2 className='px-2'>Total Amount: <Monetary num={totalAmount}/></h2>
      </div>
    );
});
