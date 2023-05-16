import React from 'react';
import {NumericFormat} from 'react-number-format';

const Monetary = ({num}) => {
  return (
    <NumericFormat
      value={num}
      displayType={'text'}
      thousandSeparator={'.'}
      decimalSeparator={','}
      suffix={' €'}
      fixedDecimalScale={true}
      decimalScale={2}
    />
  );
}

export default Monetary;
