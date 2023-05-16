import React, { useState, useEffect, useRef } from 'react';
import API from '../api';

const Inventory = ({source, submitLabel, refLabel}) => {
  const [ingredients, setIngredients] = useState([]);
  const [shipping, setShipping] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [qty, setQty] = useState(0);
  const [totalQty, setTotalQty] = useState(0);
  const [selectUnit, setSelectUnit] = useState();
  const [selectId, setSelectId] = useState();
  const [selectName, setSelectName] = useState();
  const [shippingRef, setShippingRef] = useState();
  const [error, setError] = useState();

  const refSelect = useRef(null);
  const refQty = useRef(null);
  const refShippingRef = useRef(null);

  const fetchIngredients = async() => {
    setIsLoading(true);
    API.get('ingredient').then((response) => {
      setIngredients(response.data);
      setIsLoading(false);
      setError(null);
    }).catch(error => {
      setError(error.response.data.detail);
    });
  }

  const setSelect = async(el) => {
    setSelectId(parseInt(el.value));
    setSelectName(el.options[el.selectedIndex].text);
    setSelectUnit(el.options[el.selectedIndex].getAttribute('data-unit'));
  }

  const addShipping = async() => {
    if (!selectId || !selectName || !qty) return;
    let qty_signed = qty;
    let findItemInShipping = shipping.find(i => {
      return i.ingredient.id === selectId
    });
    if (source === 'waste') {
      qty_signed = qty_signed * (-1)
    }

    if (findItemInShipping) {
      let newShipping = [];
      let newItem;

      shipping.forEach(shippingItem => {
        if(shippingItem.ingredient.id === selectId){
          newItem = {
            ...shippingItem,
            qty: shippingItem.qty + qty_signed,
          }
          newShipping.push(newItem);
        }else{
          newShipping.push(shippingItem);
        }
      });
      setShipping(newShipping);
    } else {
      let addingItem = {
        'ingredient': {
          'id': selectId,
          'name': selectName,
          'unit': selectUnit,
        },
        'qty': qty_signed,
      }
      setShipping([...shipping, addingItem]);
    }
    refSelect.current.value = '0';
    refQty.current.value = null;
    setSelectUnit(null);
  }

  const ifEnterThenAddShipping = async(event) => {
    if (event.key === "Enter") {
      addShipping();
    }
  }

  const removeItemfromShipping = async(item) => {
    const newShipping = shipping.filter(shippingItem => shippingItem.id !== item.id);
    setShipping(newShipping);
  }

  useEffect(() => {
    let newTotalQty = 0;
    shipping.forEach(shippingItem => {
      newTotalQty = newTotalQty + shippingItem.qty;
    })
    setTotalQty(newTotalQty);
  },[shipping])

  const receiveShipping = async() => {
    API.post('journal/entry', {
      ref: shippingRef,
      source: source,
      items: shipping,
    }).then((response) => {
      shippingCleanUp();
    }).catch(error => {
      setError(error.response.data.detail);
    });
  }

  const ifEnterThenReceiveShipping = async(event) => {
    if (event.key === "Enter") {
      receiveShipping();
    }
  }

  const shippingCleanUp = async() => {
    fetchIngredients();
    setShipping([]);
    setTotalQty(0);
    setShippingRef(null);
    setQty(0);
    setSelectId(null);
    setSelectName(null);
    setSelectUnit(null);
  }

  useEffect(() => {
    fetchIngredients();
  },[]);

  return (
    <>
      {error ? <div>ERROR: {error}</div> : ''}
      {isLoading ? 'Loading' :
        <div className="row">
          <div className="col-xl-6">
            <div className="row">
              <div className="col-xl-4 p-2">
                <label htmlFor="ingredients" className="form-label">Ingredients</label>
                <select ref={refSelect} id="ingredients" className="form-select p-2" aria-label="Ingredients"
                  onChange={(e) => setSelect(e.target)}>
                  <option value='0'>Select an ingredient</option>
                  {ingredients.map((ingredient, key) =>
                    <option key={key} value={ingredient.id} data-unit={ingredient.unit}>{ingredient.name}</option>
                  )}
                </select>
              </div>
              <div className="col-xl-2 p-2">
                <label htmlFor="qty" className="form-label">Qty</label>
                <div className="input-group">
                  <input ref={refQty} id="qty" className="form-control" type='number'
                    onChange={(e) => setQty(parseInt(e.target.value))}
                    onKeyUp={(e) => ifEnterThenAddShipping(e)}/>
                  <span className="input-group-text">{selectUnit}</span>
                </div>
              </div>
              <div className="col-xl-2 p-2 text-end">
                <button className='btn btn-primary' onClick={addShipping}>Add</button>
              </div>
            </div>
          </div>
          <div className="col-xl-6">
            <div className='table-responsive bg-dark mt-2 mb-4'>
              <table className='table table-responsive table-dark table-hover'>
                <thead>
                  <tr>
                    <td>Name</td>
                    <td>Qty</td>
                    <td>Unit</td>
                    <td></td>
                  </tr>
                </thead>
                <tbody>
                  { shipping ? shipping.map((shippingItem, key) =>
                  <tr key={key}>
                    <td>{shippingItem.ingredient.name}</td>
                    <td>{shippingItem.qty}</td>
                    <td>{shippingItem.ingredient.unit}</td>
                    <td><button className='btn btn-danger btn-sm' onClick={() => removeItemfromShipping(shippingItem)}>X</button></td>
                  </tr>)
                  : 'No ingredient in Shipping'}
                </tbody>
              </table>
            </div>
            {refLabel ?
            <div className=''>
              <label htmlFor="shipping-ref" className="form-label">{refLabel}:</label>
              <input ref={refShippingRef} id="shipping-ref" className="form-control" type='text'
                onChange={(e) => setShippingRef(e.target.value)}
                onKeyUp={(e) => ifEnterThenReceiveShipping(e)}/>
            </div>
            : '' }
            <div className='mt-3 text-end'>
              { totalQty !== 0 && (shippingRef || !refLabel) ?
              <div>
                <button className='btn btn-success' onClick={receiveShipping}>
                  {submitLabel}
                </button>
              </div> : ''
              }
            </div>
          </div>
        </div>
      }
    </>
  );
}

export default Inventory;
