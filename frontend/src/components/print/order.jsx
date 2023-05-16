import React from "react";

export const OrderToPrint = React.forwardRef((props, ref) => {
    const {order, } = props;
    return (
      <div ref={ref} className="p-5">
          <h1>Order: {order.id} </h1>
          <table className='table'>
            <thead>
              <tr>
                <td>Qty</td>
                <td>Name</td>
              </tr>
            </thead>
            <tbody>
              { order ? order.items.map((orderProduct, key) =>
                  <tr key={key}>
                    <td>{orderProduct.qty}</td>
                    <td>{orderProduct.name}</td>
                  </tr>)
                : ''}
            </tbody>
          </table>
      </div>
    );
});
