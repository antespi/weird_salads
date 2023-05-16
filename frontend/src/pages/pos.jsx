import React, {useEffect, useRef, useState} from 'react'
import MainLayout from '../layouts/main';
import API from '../api';
import { CartToPrint } from '../components/print/cart';
import { useReactToPrint } from 'react-to-print';
import { monetary } from '../utils';
import Monetary from '../components/monetary';

const Pos = () => {

  const [menus, setMenus] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [cart, setCart] = useState([]);
  const [totalAmount, setTotalAmount] = useState(0);
  const [orderId, setOrderId] = useState(0);
  const [error, setError] = useState();

  const fetchMenus = async() => {
    setIsLoading(true);
    API.get('menu').then((response) => {
      setMenus(response.data);
      setIsLoading(false);
      setError(null);
    }).catch(error => {
      setError(error.response.data.detail);
    });
  }

  const cartCleanUp = async() => {
    fetchMenus();
    setCart([]);
    setTotalAmount(0);
    setOrderId(0);
  }

  const reduceMenuStock = async(menu, qty) => {
    menus.forEach(menuItem => {
      if (menuItem.id === menu.id) {
        if (qty === 0) {
          menuItem.stock = 0;
        } else {
          menuItem.stock -= qty;
        }

      }
    });
    setMenus([...menus]);
  }

  const addCart = (menu) => {
    let findMenuInCart = cart.find(i => {
      return i.id === menu.id
    });
    if(findMenuInCart){
      let newCart = [];
      let newItem;

      cart.forEach(cartItem => {
        if(cartItem.id === menu.id){
          newItem = {
            ...cartItem,
            qty: cartItem.qty + 1,
            totalAmount: monetary(cartItem.price * (cartItem.qty + 1))
          }
          newCart.push(newItem);
        }else{
          newCart.push(cartItem);
        }
      });

      setCart(newCart);
    } else {
      let addingMenu = {
        ...menu,
        'qty': 1,
        'totalAmount': monetary(menu.price),
      }
      setCart([...cart, addingMenu]);
    }
  }


  const createOrder = async(menu) => {
    API.post(`order`, {id: menu.id, qty: 1}).then((response) => {
      setOrderId(response.data.id);
      addCart(menu);
      reduceMenuStock(menu, 1)
    }).catch(error => {
      reduceMenuStock(menu, 0);
    });
  }

  const appendOrder = async(menu) => {
    API.post(`order/${orderId}`, {id: menu.id, qty: 1}).then((response) => {
      addCart(menu);
      reduceMenuStock(menu, 1)
    }).catch(error => {
      reduceMenuStock(menu, 0);
    });
  }

  const payOrder = async() => {
    API.put(`order/${orderId}`, {status: 'paid'}).then((response) => {
    }).catch(error => {
    });
  }

  const addMenuToCart = async(menu) => {
    if (menu.stock === 0) return;
    if (orderId === 0) {
      createOrder(menu);
    } else {
      appendOrder(menu);
    }
  }

  const removeMenufromCart = async(menu) =>{
    const newCart = cart.filter(cartItem => cartItem.id !== menu.id);
    reduceMenuStock(menu, menu.qty * -1);
    setCart(newCart);
  }

  const componentRef = useRef();

  const handlePrint = useReactToPrint({
    content: () => componentRef.current,
  });

  const placeOrder = async() => {
    payOrder();
    handlePrint();
    cartCleanUp();
  }

  useEffect(() => {
    API.post('order/cleanup').then((response) => {
      fetchMenus();
    });
  },[]);

  useEffect(() => {
    let newTotalAmount = 0;
    cart.forEach(cartItem => {
      newTotalAmount = newTotalAmount + cartItem.totalAmount;
    })
    setTotalAmount(monetary(newTotalAmount));
  },[cart])

  return (
    <MainLayout>
      <div className='row'>
        <div className='col-xl-6'>
          <h2>POS</h2>
          {error ? <div>ERROR: {error}</div> : ''}
          {isLoading ? 'Loading' : <div className='row'>
              {menus.map((menu, key) =>
                <div key={key} className='col-xl-4 p-2' onClick={() => addMenuToCart(menu)}>
                  <div className={`pos-item p-2 border ${menu.stock !== 0 ? 'pos-item-on': 'pos-item-off'}`}>
                    <div className='pos-item-name text-start fw-bold'>{menu.name}</div>
                    <div className='pos-item-price text-end'>({menu.stock}) <Monetary num={menu.price}/></div>
                  </div>
                </div>
              )}
            </div>}

        </div>
        <div className='col-xl-6'>
              <div style={{display: "none"}}>
                <CartToPrint cart={cart} totalAmount={totalAmount} orderId={orderId} ref={componentRef}/>
              </div>
              <h2>Order: {orderId}</h2>
              <div className='table-responsive bg-dark'>
                <table className='table table-responsive table-dark table-hover'>
                  <thead>
                    <tr>
                      <td>Name</td>
                      <td className="monetary-column">Price</td>
                      <td>Qty</td>
                      <td></td>
                      <td className='text-end monetary-column'>Total</td>
                    </tr>
                  </thead>
                  <tbody>
                    { cart ? cart.map((cartMenu, key) =>
                    <tr key={key}>
                      <td>{cartMenu.name}</td>
                      <td className='monetary-column'><Monetary num={cartMenu.price} /></td>
                      <td>{cartMenu.qty}</td>
                      <td><button className='btn btn-danger btn-sm' onClick={() => removeMenufromCart(cartMenu)}>X</button></td>
                      <td className='text-end monetary-column'><Monetary num={cartMenu.totalAmount} /></td>
                    </tr>)
                    : 'No Item in Cart'}
                  </tbody>
                </table>
                <h2 className='px-2 text-white text-end'><Monetary num={totalAmount}/></h2>
              </div>

              <div className='mt-3 text-end'>
                { totalAmount !== 0 && orderId !== 0 ?
                <div>
                  <button className='btn btn-success' onClick={placeOrder}>
                    Pay Now
                  </button>

                </div> : 'Please add a product to the cart'

                }
              </div>


        </div>
      </div>
    </MainLayout>
  );
}

export default Pos;
